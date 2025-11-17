#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
按目标大小导出带水印视频（一次命中体积为主；必要时再微调）
- 支持输入：.mp4/.mov/.mkv/.m4v（更多容器大多也行）
- 输出：.mp4（H.264 + AAC, yuv420p, +faststart）
- 水印：按视频宽度比例缩放，右下角 10px 边距
- 体积：用时长反推目标码率（bitrate），CPU 两遍更稳命中；可切换 NVIDIA GPU (h264_nvenc)

依赖：系统需安装 ffmpeg/ffprobe
  Ubuntu: sudo apt-get install -y ffmpeg
"""

import os
import sys
import json
import math
import argparse
import subprocess
from pathlib import Path

# ---------- ffprobe helpers ----------
def run_cmd(cmd):
    try:
        return subprocess.check_output(cmd, stderr=subprocess.STDOUT).decode("utf-8")
    except FileNotFoundError:
        print("❌ 未找到 ffmpeg/ffprobe，请先安装（Ubuntu: sudo apt-get install -y ffmpeg）")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(e.output.decode("utf-8"))

def probe_duration_sec(input_path: str) -> float:
    out = run_cmd([
        "ffprobe", "-v", "error",
        "-select_streams", "v:0",
        "-show_entries", "format=duration",
        "-of", "json", input_path
    ])
    data = json.loads(out)
    return float(data["format"]["duration"])

def probe_width_height(input_path: str):
    out = run_cmd([
        "ffprobe","-v","error","-select_streams","v:0",
        "-show_entries","stream=width,height","-of","json", input_path
    ])
    data = json.loads(out)
    w = int(data["streams"][0]["width"])
    h = int(data["streams"][0]["height"])
    return w, h

# ---------- core ----------
def add_watermark_ffmpeg(
    input_video_path: str,
    watermark_image_path: str,
    output_video_path: str,
    max_size_mb: int = 250,
    wm_scale_ratio: float = 0.12,      # 水印宽度占视频宽度比例
    audio_bitrate_k: int = 128,        # AAC kbps
    use_gpu: bool = False,             # True 走 h264_nvenc
    preset: str = "slow",              # libx264 预设：ultrafast..placebo；nvenc 可用 p1..p7
    max_bitrate_headroom: float = 0.97 # 给容器/索引留一点冗余
):
    input_path = Path(input_video_path)
    output_path = Path(output_video_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # 1) 基础信息
    duration = probe_duration_sec(str(input_path))
    if duration <= 0:
        raise ValueError("无法从输入视频获取有效时长。")
    video_w, video_h = probe_width_height(str(input_path))

    # 2) 反推目标视频码率（kbps）
    total_bits = max_size_mb * 1024 * 1024 * 8 * max_bitrate_headroom
    v_kbps = max(250, int(total_bits / duration / 1000) - audio_bitrate_k)
    v_kbps = min(v_kbps, 25_000)

    # 3) 计算水印目标宽度（偶数）
    wm_target_w = max(2, int(video_w * wm_scale_ratio))
    if wm_target_w % 2 == 1:
        wm_target_w += 1

    # 4) 滤镜：scale + overlay（右下角）
    vf = f"[1:v]scale={wm_target_w}:-1[wm];[0:v][wm]overlay=W-w-10:H-h-10:format=auto"

    common = [
        "-y","-hide_banner",
        "-i", str(input_path),
        "-i", str(watermark_image_path),
        "-filter_complex", vf,
        "-movflags","+faststart",
        "-pix_fmt","yuv420p",
        "-map","0:v:0","-map","0:a?:0",           # 没音频也不报错
        "-c:a","aac","-b:a", f"{audio_bitrate_k}k",
    ]

    if use_gpu:
        # ---------- NVIDIA GPU (h264_nvenc) ----------
        maxrate = max(int(v_kbps * 1.1), v_kbps + 100)
        bufsize = max(v_kbps * 2, 2000)
        cmd = [
            "ffmpeg",
            *common,
            "-c:v", "h264_nvenc",
            "-preset", "p5" if preset == "slow" else preset,  # 可改 p1..p7
            "-b:v", f"{v_kbps}k",
            "-maxrate", f"{maxrate}k",
            "-bufsize", f"{bufsize}k",
            "-rc", "vbr",
            "-tune", "hq",
            "-profile:v", "high",
            "-rc-lookahead", "20",
            str(output_path),
        ]
        print("▶ ffmpeg (GPU) =", " ".join(cmd))
        run_cmd(cmd)
    else:
        # ---------- CPU (libx264，两遍更稳命中体积) ----------
        maxrate = max(int(v_kbps * 1.1), v_kbps + 100)
        bufsize = max(v_kbps * 2, 2000)
        passlog = str(output_path.with_suffix(""))  # passlog 前缀

        # pass 1（无音频以提速）
        cmd1 = [
            "ffmpeg",
            *common,
            "-c:v","libx264",
            "-preset", preset,
            "-b:v", f"{v_kbps}k",
            "-maxrate", f"{maxrate}k",
            "-bufsize", f"{bufsize}k",
            "-pass","1","-passlogfile", passlog,
            "-an","-f","mp4","/dev/null"
        ]
        print("▶ ffmpeg (CPU pass1) =", " ".join(cmd1))
        run_cmd(cmd1)

        # pass 2
        cmd2 = [
            "ffmpeg",
            *common,
            "-c:v","libx264",
            "-preset", preset,
            "-b:v", f"{v_kbps}k",
            "-maxrate", f"{maxrate}k",
            "-bufsize", f"{bufsize}k",
            "-pass","2","-passlogfile", passlog,
            "-profile:v","high",
            str(output_path),
        ]
        print("▶ ffmpeg (CPU pass2) =", " ".join(cmd2))
        run_cmd(cmd2)

        # 清理 passlog（可选，不影响播放）
        for ext in (".log", ".log.mbtree"):
            fp = Path(passlog + ext)
            if fp.exists():
                try: fp.unlink()
                except: pass

    # 报告结果
    size_mb = os.path.getsize(output_path)/(1024*1024)
    print(f"✅ 导出完成：{output_path}\n   目标 {max_size_mb}MB | 实际 {size_mb:.2f}MB | v_bitrate≈{v_kbps}kbps")

# ---------- batch ----------
def process_folder(
    input_folder: str,
    watermark_path: str,
    output_folder: str,
    max_size_mb: int = 250,
    wm_scale_ratio: float = 0.12,
    audio_bitrate_k: int = 128,
    use_gpu: bool = False,
    preset: str = "slow",
):
    exts = (".mp4", ".mov", ".mkv", ".m4v")
    for root, _, files in os.walk(input_folder):
        for f in files:
            if f.lower().endswith(exts):
                in_path = os.path.join(root, f)
                rel = os.path.relpath(root, input_folder)
                out_dir = os.path.join(output_folder, rel)
                os.makedirs(out_dir, exist_ok=True)
                out_name = Path(f).with_suffix(".mp4").name
                out_path = os.path.join(out_dir, out_name)

                print(f"\n=== 处理 {in_path} -> {out_path} ===")
                add_watermark_ffmpeg(
                    in_path, watermark_path, out_path,
                    max_size_mb=max_size_mb,
                    wm_scale_ratio=wm_scale_ratio,
                    audio_bitrate_k=audio_bitrate_k,
                    use_gpu=use_gpu,
                    preset=preset,
                )

# ---------- cli ----------
def parse_args():
    p = argparse.ArgumentParser(description="按目标体积导出带水印视频（FFmpeg版）")
    p.add_argument("--input", "-i", type=str, required=True,
                   help="输入文件或文件夹（文件夹将递归处理）")
    p.add_argument("--watermark", "-w", type=str, required=True,
                   help="水印图片（建议 PNG 带透明通道）")
    p.add_argument("--output", "-o", type=str, required=True,
                   help="输出文件或文件夹（输入是文件则写文件；输入是目录则写目录）")
    p.add_argument("--max-size-mb", type=int, default=250, help="目标上限体积（MB）")
    p.add_argument("--wm-scale", type=float, default=0.12, help="水印宽度占视频宽度比例")
    p.add_argument("--audio-kbps", type=int, default=128, help="音频码率 kbps")
    p.add_argument("--gpu", action="store_true", help="使用 NVIDIA h264_nvenc（更快）")
    p.add_argument("--preset", type=str, default="slow",
                   help="CPU: libx264 预设 ultrafast..placebo；GPU: p1..p7（默认 slow→p5）")
    return p.parse_args()

def main():
    args = parse_args()
    inp = Path(args.input)
    outp = Path(args.output)

    if inp.is_file():
        outp.parent.mkdir(parents=True, exist_ok=True)
        # 单文件强制 .mp4 输出
        if outp.suffix.lower() != ".mp4":
            outp = outp.with_suffix(".mp4")
        add_watermark_ffmpeg(
            str(inp), args.watermark, str(outp),
            max_size_mb=args.max_size_mb,
            wm_scale_ratio=args.wm_scale,
            audio_bitrate_k=args.audio_kbps,
            use_gpu=args.gpu,
            preset=args.preset,
        )
    elif inp.is_dir():
        outp.mkdir(parents=True, exist_ok=True)
        process_folder(
            str(inp), args.watermark, str(outp),
            max_size_mb=args.max_size_mb,
            wm_scale_ratio=args.wm_scale,
            audio_bitrate_k=args.audio_kbps,
            use_gpu=args.gpu,
            preset=args.preset,
        )
    else:
        print("❌ 输入路径不存在")
        sys.exit(1)

if __name__ == "__main__":
    main()


import os
from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip

def add_watermark_to_video(
    input_video_path,
    watermark_image_path,
    output_video_path,
    watermark_scale=0.12
):
    video = VideoFileClip(input_video_path)
    video_w, video_h = video.size

    # 加载水印图并设置持续时间
    watermark = ImageClip(watermark_image_path).set_duration(video.duration)
    wm_width = int(video_w * watermark_scale)
    aspect_ratio = watermark.h / watermark.w
    wm_height = int(wm_width * aspect_ratio)
    watermark = watermark.resize(newsize=(wm_width, wm_height))

    # 设置右下角位置
    position = (video_w - wm_width - 10, video_h - wm_height - 10)
    watermark = watermark.set_pos(position)

    # 合成视频
    final = CompositeVideoClip([video, watermark])
    final.write_videofile(
        output_video_path,
        codec="libx264",
        audio_codec="aac",
        bitrate="5000k",
        audio_bitrate="192k",
        threads=4,
        logger=None  # 静默输出，可改为"bar"
    )
    print(f"✅ 已添加水印: {output_video_path}")

def batch_watermark_videos(input_folder, watermark_path, output_folder, watermark_scale=0.12):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for root, _, files in os.walk(input_folder):
        for file in files:
            if file.lower().endswith(".mp4"):
                input_path = os.path.join(root, file)
                # 保留子目录结构
                relative_path = os.path.relpath(root, input_folder)
                output_dir = os.path.join(output_folder, relative_path)
                os.makedirs(output_dir, exist_ok=True)
                output_path = os.path.join(output_dir, file)
                add_watermark_to_video(input_path, watermark_path, output_path, watermark_scale)

def main():
    input_folder = "/home/heirenlop/workspace/python-tools/watermark/input"
    watermark_path = "/home/heirenlop/workspace/python-tools/watermark/watermark.png"
    output_folder = "/home/heirenlop/workspace/python-tools/watermark/output"

    batch_watermark_videos(input_folder, watermark_path, output_folder, watermark_scale=0.12)

if __name__ == "__main__":
    main()

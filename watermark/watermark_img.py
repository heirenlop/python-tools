# pip install pillow
import os
from PIL import Image, ImageOps

def add_watermark_to_image(
    input_image_path: str,
    watermark_image_path: str,
    output_image_path: str,
    watermark_scale: float = 0.12,   # 水印宽度占原图宽度比例
    margin: int = 10                 # 右下角边距
):
    # 打开原图并处理方向（有些手机照片有旋转EXIF）
    with Image.open(input_image_path) as base_im:
        base_im = ImageOps.exif_transpose(base_im)
        base_w, base_h = base_im.size

        # 统一转 RGBA 便于透明叠加
        base_rgba = base_im.convert("RGBA")

        # 打开水印
        with Image.open(watermark_image_path) as wm:
            wm = wm.convert("RGBA")
            # 计算缩放后的尺寸（按原图宽度比例）
            wm_w = max(1, int(base_w * watermark_scale))
            # 按水印原比例缩放
            ratio = wm_w / wm.width
            wm_h = max(1, int(wm.height * ratio))
            wm_resized = wm.resize((wm_w, wm_h), Image.LANCZOS)

        # 计算位置（右下角）
        pos = (base_w - wm_resized.width - margin, base_h - wm_resized.height - margin)

        # 合成
        composite = Image.new("RGBA", (base_w, base_h))
        composite.paste(base_rgba, (0, 0))
        composite.paste(wm_resized, pos, mask=wm_resized)

        # 保存：PNG 保留透明；JPEG 转回 RGB 并高质量
        ext = os.path.splitext(output_image_path)[1].lower()
        os.makedirs(os.path.dirname(output_image_path), exist_ok=True)
        if ext in [".png", ".webp"]:
            # PNG：尽量压缩但不损质
            composite.save(output_image_path, optimize=True)
        else:
            # JPEG/JPG：去透明通道
            rgb = composite.convert("RGB")
            rgb.save(output_image_path, quality=95, subsampling=0, optimize=True)

        print(f"✅ 已输出：{output_image_path}")

def batch_watermark_images(input_folder, watermark_path, output_folder, watermark_scale=0.12, margin=10):
    if not os.path.isdir(input_folder):
        print(f"❌ 输入目录不存在：{input_folder}")
        return
    if not os.path.isfile(watermark_path):
        print(f"❌ 水印图片不存在：{watermark_path}")
        return
    os.makedirs(output_folder, exist_ok=True)

    exts = {".jpg", ".jpeg", ".png"}  # 需要可再加 ".webp", ".bmp" 等
    todo = []
    for root, _, files in os.walk(input_folder):
        for f in files:
            if os.path.splitext(f)[1].lower() in exts:
                in_path = os.path.join(root, f)
                rel = os.path.relpath(root, input_folder)
                out_dir = os.path.join(output_folder, rel)
                out_path = os.path.join(out_dir, f)  # 保持原始扩展名
                todo.append((in_path, out_path))

    if not todo:
        print("ℹ️ 没找到要处理的图片。")
        return

    print(f"📦 待处理图片数：{len(todo)}")
    for i, (inp, outp) in enumerate(todo, 1):
        try:
            print(f"({i}/{len(todo)}) 处理：{inp}")
            add_watermark_to_image(inp, watermark_path, outp, watermark_scale, margin)
        except Exception as e:
            print(f"⚠️ 失败：{inp}\n   原因：{e}")

def main():
    input_folder = "/home/heirenlop/workspace/python-tools/watermark/input"
    watermark_path = "/home/heirenlop/workspace/python-tools/watermark/watermark.png"
    output_folder = "/home/heirenlop/workspace/python-tools/watermark/output"

    batch_watermark_images(input_folder, watermark_path, output_folder, watermark_scale=0.12, margin=10)

if __name__ == "__main__":
    main()


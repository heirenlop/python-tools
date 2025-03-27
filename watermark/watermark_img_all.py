import os
from PIL import Image

def add_watermark(
    input_image_path, 
    watermark_image_path, 
    output_image_path, 
    watermark_scale=0.2
):
    base_image = Image.open(input_image_path).convert("RGBA")
    watermark = Image.open(watermark_image_path).convert("RGBA")

    base_width, base_height = base_image.size
    wm_width, wm_height = watermark.size

    new_wm_width = int(base_width * watermark_scale)
    aspect_ratio = wm_height / wm_width
    new_wm_height = int(new_wm_width * aspect_ratio)

    watermark_resized = watermark.resize((new_wm_width, new_wm_height), Image.ANTIALIAS)

    position_x = base_width - new_wm_width - 10
    position_y = base_height - new_wm_height - 10

    layer = Image.new("RGBA", base_image.size, (0, 0, 0, 0))
    layer.paste(watermark_resized, (position_x, position_y))

    watermarked_image = Image.alpha_composite(base_image, layer)
    watermarked_image = watermarked_image.convert("RGB")
    watermarked_image.save(output_image_path, quality=95)
    print(f"✅ 已添加水印: {output_image_path}")

def batch_watermark(
    input_folder, 
    watermark_path, 
    output_folder, 
    watermark_scale=0.12
):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    supported_ext = (".jpg", ".jpeg", ".png")
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(supported_ext):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)
            add_watermark(input_path, watermark_path, output_path, watermark_scale)

def main():
    input_folder = "/home/heirenlop/workspace/my_repo/heirenlop.github.io/static/images/work-record"         # 你的原图文件夹
    watermark_path = "watermark.png"         # 水印图
    output_folder = "./output_images1" # 输出文件夹

    batch_watermark(input_folder, watermark_path, output_folder, watermark_scale=0.12)

if __name__ == "__main__":
    main()

from PIL import Image

def add_watermark(
    input_image_path, 
    watermark_image_path, 
    output_image_path, 
    watermark_scale=0.2
):
    """
    在原图右下角添加水印后输出。
    :param input_image_path: 原图路径
    :param watermark_image_path: 水印图路径
    :param output_image_path: 输出图路径
    :param watermark_scale: 水印相对于原图宽度所占的比例(默认 0.2 = 20%)
    """
    # 打开原图和水印图
    base_image = Image.open(input_image_path).convert("RGBA")
    watermark = Image.open(watermark_image_path).convert("RGBA")

    # 获取原图大小
    base_width, base_height = base_image.size
    wm_width, wm_height = watermark.size
    
    # 将水印等比例缩放到原图宽度的 watermark_scale（默认 20%）
    new_wm_width = int(base_width * watermark_scale)
    # 按照原水印的长宽比进行等比缩放
    aspect_ratio = wm_height / wm_width
    new_wm_height = int(new_wm_width * aspect_ratio)

    # 缩放水印
    watermark_resized = watermark.resize((new_wm_width, new_wm_height), Image.Resampling.LANCZOS)

    # 计算水印要贴到的位置（右下角）
    position_x = base_width - new_wm_width - 10  # 右边留 10 像素边距
    position_y = base_height - new_wm_height - 10  # 底部留 10 像素边距
    
    # 创建一个与原图一样大的透明图层，用于叠加水印
    layer = Image.new("RGBA", base_image.size, (0, 0, 0, 0))
    layer.paste(watermark_resized, (position_x, position_y))

    # 将水印图层与原图合并
    watermarked_image = Image.alpha_composite(base_image, layer)

    # 如果要输出 JPEG 等不含透明通道的格式，可转回 RGB
    watermarked_image = watermarked_image.convert("RGB")
    watermarked_image.save(output_image_path, quality=95)
    print(f"水印添加完成: {output_image_path}")

def main():
    # 在这里修改需要的文件路径
    input_path = "./changchun1.jpg"        # 原图
    watermark_path = "watermark.png"  # 水印图（建议带透明通道）
    output_path = "./changchun1.png"      # 输出图

    # 水印缩放比例 (相对于原图宽度)
    add_watermark(input_path, watermark_path, output_path, watermark_scale=0.2)

if __name__ == "__main__":
    main()

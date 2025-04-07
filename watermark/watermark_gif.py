from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip

def add_watermark_to_gif(
    input_gif_path, 
    watermark_image_path, 
    output_gif_path, 
    watermark_scale=0.12
):
    # 加载 GIF 文件
    gif = VideoFileClip(input_gif_path)
    gif_w, gif_h = gif.size

    # 加载水印图像并调整大小
    watermark = ImageClip(watermark_image_path).set_duration(gif.duration)
    wm_width = int(gif_w * watermark_scale)
    aspect_ratio = watermark.h / watermark.w
    wm_height = int(wm_width * aspect_ratio)
    watermark = watermark.resize(newsize=(wm_width, wm_height))

    # 设置水印位置（右下角，留10px边距）
    position = (gif_w - wm_width - 10, gif_h - wm_height - 10)
    watermark = watermark.set_pos(position)

    # 合成 GIF 和水印
    final = CompositeVideoClip([gif, watermark])

    # 输出为 GIF 格式
    final.write_gif(output_gif_path, fps=gif.fps)

    print(f"✅ GIF 处理完成: {output_gif_path}")

def main():
    input_gif = "./weihai3.gif"       # 原始 GIF 路径
    watermark = "./watermark.png"   # 水印图路径
    output_gif = "./output3.gif"     # 输出 GIF 路径

    add_watermark_to_gif(input_gif, watermark, output_gif, watermark_scale=0.12)

if __name__ == "__main__":
    main()

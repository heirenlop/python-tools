import os
from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip
"为单个视频添加水印"
def add_watermark_to_video(
    input_video_path, 
    watermark_image_path, 
    output_video_path, 
    watermark_scale=0.12
):
    # 加载视频和水印
    video = VideoFileClip(input_video_path)
    video_w, video_h = video.size

    # 加载水印并缩放
    watermark = ImageClip(watermark_image_path).set_duration(video.duration)
    wm_width = int(video_w * watermark_scale)
    aspect_ratio = watermark.h / watermark.w
    wm_height = int(wm_width * aspect_ratio)
    watermark = watermark.resize(newsize=(wm_width, wm_height))

    # 设置水印位置（右下角，留10px边距）
    position = (video_w - wm_width - 10, video_h - wm_height - 10)
    watermark = watermark.set_pos(position)

    # 合成视频
    final = CompositeVideoClip([video, watermark])
    final.write_videofile(output_video_path, codec="libx264", audio_codec="aac")

    print(f"✅ 视频处理完成: {output_video_path}")

def main():
    input_video = "./maanshan1.mp4"       # 原始视频路径
    watermark = "./watermark.png"              # 水印图路径（PNG，最好带透明）
    output_video = "./sample_watermarked.mp4"  # 输出路径

    add_watermark_to_video(input_video, watermark, output_video, watermark_scale=0.12)

if __name__ == "__main__":
    main()

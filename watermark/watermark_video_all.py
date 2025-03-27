import os
from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip
"遍历某文件夹内所有子文件夹的所有.mp4文件，"
"为每个视频添加水印，并输出到同目录下，文件名前缀为'watermarked_'"
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

    # 输出视频，调整质量和比特率
    final.write_videofile(output_video_path, codec="libx264", audio_codec="aac", bitrate="5000k", audio_bitrate="192k")

    print(f"✅ 视频处理完成: {output_video_path}")

def process_all_videos(input_dir, watermark_image_path, watermark_scale=0.12):
    # 遍历文件夹下的所有子文件夹，找到所有.mp4文件
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.endswith(".mp4"):
                input_video_path = os.path.join(root, file)
                output_video_path = os.path.join(root, f"watermarked_{file}")
                print(f"Found video: {input_video_path}")  # 调试输出，检查文件是否被找到
                
                # 处理视频
                add_watermark_to_video(input_video_path, watermark_image_path, output_video_path, watermark_scale)

def main():
    input_dir = "/home/heirenlop/workspace/my_repo/heirenlop.github.io/static/videos"      # 输入视频所在文件夹路径
    watermark = "./watermark.png"  # 水印图路径（PNG，最好带透明）

    # 处理所有视频
    process_all_videos(input_dir, watermark, watermark_scale=0.12)

if __name__ == "__main__":
    main()

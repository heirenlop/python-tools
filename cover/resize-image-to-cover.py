from PIL import Image
import os

# === 配置 ===
input_folder = './'  # 原始图片路径
output_folder = os.path.join(input_folder, 'resized')  # 输出路径
target_size = (1200, 675)  # 推荐封面图尺寸（16:9）

os.makedirs(output_folder, exist_ok=True)

# 支持的图片扩展名
valid_ext = ['.jpg', '.jpeg', '.png']

for filename in os.listdir(input_folder):
    name, ext = os.path.splitext(filename)
    if ext.lower() not in valid_ext:
        continue

    input_path = os.path.join(input_folder, filename)
    output_path = os.path.join(output_folder, f"{name}.jpg")  # 输出统一为jpg

    try:
        with Image.open(input_path) as img:
            # 若原图尺寸小于目标尺寸，跳过
            if img.width < target_size[0] or img.height < target_size[1]:
                print(f"⏭️ 跳过尺寸过小：{filename}")
                continue

            # 中心裁剪成目标比例
            img_ratio = img.width / img.height
            target_ratio = target_size[0] / target_size[1]

            if img_ratio > target_ratio:
                # 图片太宽，裁左右
                new_width = int(target_ratio * img.height)
                left = (img.width - new_width) // 2
                box = (left, 0, left + new_width, img.height)
            else:
                # 图片太高，裁上下
                new_height = int(img.width / target_ratio)
                top = (img.height - new_height) // 2
                box = (0, top, img.width, top + new_height)

            cropped = img.crop(box)
            resized = cropped.resize(target_size, Image.LANCZOS)

            # 转换透明图层为RGB（PNG透明通道问题）
            if resized.mode in ('RGBA', 'LA'):
                resized = resized.convert('RGB')

            resized.save(output_path, quality=85)
            print(f"✅ 已处理：{filename} → {output_path}")
    except Exception as e:
        print(f"❌ 处理失败：{filename}，错误：{e}")


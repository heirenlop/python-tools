import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# 显式加载支持中文的字体
font_path = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
chinese_font = fm.FontProperties(fname=font_path)

fig, ax = plt.subplots(figsize=(14, 10))
ax.axis('off')

# 定义模块内容
modules = {
    "数据预处理": ["COLMAP/SfM重建", "初始化高斯点（位置、颜色、透明度等）"],
    "训练前设置": ["初始化参数组 l", "构建优化器 Adam", "设置学习率调度器"],
    "训练主循环": [
        "图像采样 + 投影",
        "高斯渲染（合成图像）",
        "计算损失（与GT图像对比）",
        "loss.backward() 反向传播",
        "optimizer.step() 更新参数",
        "学习率调度器更新",
        "动态加点 densify / 剪枝 prune"
    ],
    "输出与评估": ["保存模型参数", "评估 PSNR / 可视化", "生成视频 / mesh"]
}

colors = {
    "数据预处理": "#d0e1f9",
    "训练前设置": "#f9d0d0",
    "训练主循环": "#d0f9d6",
    "输出与评估": "#f9f2d0"
}

# 绘制流程结构图
y = 0
for group, steps in modules.items():
    ax.text(0.02, y, group, fontsize=18, weight='bold', va='top',
            bbox=dict(boxstyle="round,pad=0.3", facecolor=colors[group]),
            fontproperties=chinese_font)
    y -= 0.12
    for step in steps:
        ax.text(0.07, y, f"• {step}", fontsize=15, va='top', fontproperties=chinese_font)
        y -= 0.08
    y -= 0.07

# 设置标题字体
plt.title("3D Gaussian Splatting（3DGS）训练流程图", fontsize=22, weight='bold', fontproperties=chinese_font)

# 显示区域控制
ax.set_xlim(0, 1)
ax.set_ylim(y - 0.1, 0.1)

plt.tight_layout()
plt.show()

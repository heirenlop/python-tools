# 重新执行代码（因内核已重置）

import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# 设置中文字体（如有）
font_path = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
chinese_font = fm.FontProperties(fname=font_path)

fig, ax = plt.subplots(figsize=(12, 8), dpi=300)
ax.axis("off")

# 定义模块及关系
modules = {
    "主进程": ["创建参数（config, queues, gaussians）", "创建 FrontEnd 实例", "创建 BackEnd 实例", "创建 GUI 参数容器", "启动 BackEnd 子进程", "（可选）启动 GUI 子进程", "同步等待（如 time.sleep）", "运行 FrontEnd.run() 作为同步主循环"],
    "BackEnd 子进程": ["通过 start() 启动", "执行 run() 内的优化逻辑", "从 frontend_queue 接收数据", "更新 gaussians"],
    "FrontEnd（主线程中）": ["执行 run()", "图像处理、SLAM、帧管理", "通过 frontend_queue 向后端发数据", "通过 q_main2vis 向 GUI 发送图像"],
    "GUI 子进程（可选）": ["通过 start() 启动", "执行 run(params_gui)", "监听 q_main2vis 获取图像", "发送控制信息到 q_vis2main"]
}

colors = {
    "主进程": "#d0e1f9",
    "BackEnd 子进程": "#f9d0d0",
    "FrontEnd（主线程中）": "#d0f9d6",
    "GUI 子进程（可选）": "#f9f2d0"
}

y = 1.0
for module, steps in modules.items():
    ax.text(0.02, y, module, fontsize=14, weight='bold', va='top',
            bbox=dict(boxstyle="round,pad=0.3", facecolor=colors[module]),
            fontproperties=chinese_font)
    y -= 0.08
    for step in steps:
        ax.text(0.06, y, f"• {step}", fontsize=12, va='top', fontproperties=chinese_font)
        y -= 0.06
    y -= 0.05

plt.title("3DGS 简化版进程结构与逻辑关系图", fontsize=16, fontproperties=chinese_font)
plt.tight_layout()
plt.show()

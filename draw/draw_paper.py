import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.font_manager as fm

# 使用用户上传的中文字体
font_path = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
chinese_font = fm.FontProperties(fname=font_path, size=14)  # 增大基础字体大小

# 设置画布（尺寸增大到24x12）
fig, ax = plt.subplots(figsize=(24, 12), dpi=150)  # 原20x10改为24x12，DPI提升到150
ax.axis('off')

# 文章0的基础模块（调整垂直间距）
base_modules = [
    ("多视角图像", 0.9),
    ("SfM初始化点云", 0.8),
    ("高斯参数初始化", 0.7),
    ("可微渲染器", 0.6),
    ("高斯优化", 0.5),
    ("实时渲染", 0.4)
]

# ... [保持原有的extensions定义不变] ...

# 扩展模块定义（相对于文章0的创新点为True）
extensions = {
    "文章1\nDrivingGaussian": [
        ("LiDAR辅助输入", 0.9, True),
        ("动态/静态高斯分离", 0.8, True),
        ("Composite结构", 0.7, True),
        ("遮挡感知渲染", 0.6, False),
        ("增量建图", 0.5, True),
        ("多视角街景渲染", 0.4, False)
    ],
    "文章2\nS3Gaussian": [
        ("自监督轨迹估计", 0.9, True),
        ("动态目标分离", 0.8, True),
        ("时空高斯MLP", 0.7, True),
        ("可微深度监督", 0.6, False),
        ("语义分解（隐式）", 0.5, True),
        ("无标注建图", 0.4, True)
    ],
    "文章3\nStreet Gaussians": [
        ("显式目标检测框", 0.9, False),
        ("目标级高斯建模", 0.8, True),
        ("4D位姿优化", 0.7, True),
        ("语义logits渲染", 0.6, True),
        ("语义可编辑性", 0.5, True),
        ("实时街景展示", 0.4, False)
    ],
    "文章4\nGaussianPro": [
        ("深度+法线图辅助", 0.9, True),
        ("错误传播补点", 0.8, True),
        ("平面约束损失", 0.7, True),
        ("无需语义", 0.6, False),
        ("稀疏区域修复", 0.5, True),
        ("提高细节保留", 0.4, False)
    ],
    "文章5\nSplatAD": [
        ("LiDAR渲染增强", 0.9, True),
        ("多模态输入融合", 0.8, True),
        ("高斯模糊+扩张建模", 0.7, True),
        ("激光雷达深度仿真", 0.6, True),
        ("传感器物理一致性", 0.5, True),
        ("自动驾驶仿真可用性", 0.4, False)
    ]
}
# 绘制文章0模块（调整模块高度和文字位置）
x0 = 0
# 文章标题字号增大到16
ax.text(x0 + 0.3, 1.03, "文章0\n原始3DGS", fontsize=16, ha='center', weight='bold', fontproperties=chinese_font)
for text, y in base_modules:
    # 增大模块高度到0.12
    rect = patches.FancyBboxPatch((x0, y), 0.6, 0.12,  # 高度从0.09→0.12
                                  boxstyle="round,pad=0.05", linewidth=1.5,  # 圆角增大
                                  facecolor='lightgray', edgecolor='black')
    ax.add_patch(rect)
    # 文字字号增大到13
    ax.text(x0 + 0.3, y + 0.06, text, va='center', ha='center', 
            fontsize=13, fontproperties=chinese_font)  # 字号11→13

# 绘制文章1~5的模块和创新点（调整水平间距）
x_shift = 2.5  # 水平间距从2.0→2.5
for i, (paper, mods) in enumerate(extensions.items()):
    x = x0 + (i + 1) * x_shift
    # 文章标题字号增大到16
    ax.text(x + 0.3, 1.03, paper, fontsize=16, ha='center', 
            weight='bold', fontproperties=chinese_font)
    for text, y, is_new in mods:
        color = 'salmon' if is_new else 'whitesmoke'
        # 增大模块高度到0.12
        rect = patches.FancyBboxPatch((x, y), 0.6, 0.12,  # 高度从0.09→0.12
                                      boxstyle="round,pad=0.05", linewidth=1.5,
                                      facecolor=color, edgecolor='black')
        ax.add_patch(rect)
        # 文字字号增大到12
        ax.text(x + 0.3, y + 0.06, text, va='center', ha='center', 
                fontsize=12, fontproperties=chinese_font)  # 字号10.5→12

# 主标题字号增大到22
plt.title("文章0-5 模块结构与扩展创新（红色为相对0的新增/创新点）", 
          fontsize=22, pad=25,  # pad增加标题间距
          fontproperties=chinese_font)

# 使用约束布局代替tight_layout
plt.subplots_adjust(left=0.05, right=0.95, top=0.9, bottom=0.1)  # 调整边距
plt.show()


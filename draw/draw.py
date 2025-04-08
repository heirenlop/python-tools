import matplotlib.pyplot as plt
import networkx as nx

# 创建有向图
G = nx.DiGraph()

# 添加节点和数据流程
modules = {
    "主程序 (slam.py)": ["前端 FrontEnd", "后端 BackEnd", "GUI 界面"],
    "前端 FrontEnd": ["后端 BackEnd", "GUI 界面"],
    "后端 BackEnd": ["GUI 界面"],
    "前端 FrontEnd 图像输入": ["前端 FrontEnd"],
    "配置/数据集加载": ["主程序 (slam.py)"],
    "输出：位姿/地图": ["GUI 界面"],
}

for src, targets in modules.items():
    for tgt in targets:
        G.add_edge(src, tgt)

# 布局设置
pos = nx.spring_layout(G, seed=42)

# 绘图
plt.figure(figsize=(12, 8))
nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray',
        node_size=3000, font_size=10, font_weight='bold', arrows=True)
plt.title("MonoGS 系统模块数据流图", fontsize=14)
plt.show()

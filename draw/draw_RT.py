from graphviz import Digraph

# 创建一个有向图对象
dot = Digraph(format='png')
dot.attr(rankdir='TB', fontsize='10')

# 添加节点
dot.node('A', '世界坐标系下的点\nP_world = [X, Y, Z]')
dot.node('B', '相机坐标系\nP_camera = R * P_world + t = [X\', Y\', Z\']')
dot.node('C', '相机归一化坐标系\nx_n = X\'/Z\', y_n = Y\'/Z\'')
dot.node('D', '图像坐标系 (像素)\nu = fx * x_n + cx\nv = fy * y_n + cy\n→ 投影点为 (u, v)')

# 添加边
dot.edge('A', 'B', label='外参变换 [R|t]')
dot.edge('B', 'C', label='投影除以 Z\'')
dot.edge('C', 'D', label='内参变换 K')

# 渲染图像
dot.render('camera_projection_flow', view=True, cleanup=True)

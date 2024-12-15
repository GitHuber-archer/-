import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx
from itertools import combinations

# 1. 加载数据
df = pd.read_csv('data1.csv')  # 请确保文件路径正确

# 2. 数据清洗：处理缺失值和作者分割
df['Author'] = df['Author'].fillna('')  # 去除空值
df['Authors_list'] = df['Author'].apply(lambda x: x.split(';'))  # 假设多个作者用分号分隔

# 3. 创建合作网络
G = nx.Graph()

# 统计每对作者合作的次数
for authors in df['Authors_list']:
    # 获取所有作者的两两组合
    author_pairs = combinations(authors, 2)
    for pair in author_pairs:
        if G.has_edge(pair[0], pair[1]):
            G[pair[0]][pair[1]]['weight'] += 1  # 增加边的权重
        else:
            G.add_edge(pair[0], pair[1], weight=1)  # 初次添加边

# 4. 计算网络中心性指标：度中心性、介数中心性和紧密度中心性
degree_centrality = nx.degree_centrality(G)
betweenness_centrality = nx.betweenness_centrality(G)
closeness_centrality = nx.closeness_centrality(G)

# 5. 显示度中心性排名前5的作者
top_authors_degree = sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)
print("度中心性排名前5的作者：")
for author, score in top_authors_degree[:]:
    print(f"{author}: {score}")

# 6. 可视化作者合作网络
plt.figure(figsize=(16, 16))

# 使用Spring布局进行可视化
pos = nx.spring_layout(G, k=0.2, iterations=30)  # 使用更大的k值，调整图形布局，使得结点之间距离更大

# 节点大小按度中心性调整
node_size = [v * 2000 for v in degree_centrality.values()]  # 节点大小根据度中心性调整
node_color = [v for v in degree_centrality.values()]  # 节点的颜色按度中心性调整，度中心性高的节点颜色较深

# 边的宽度按合作次数（权重）调整
edge_width = [G[u][v]['weight'] for u, v in G.edges()]

# 绘制网络图
nx.draw_networkx_nodes(G, pos, node_size=node_size, node_color=node_color, cmap=plt.cm.Blues, alpha=0.8)
nx.draw_networkx_edges(G, pos, width=edge_width, alpha=0.5, edge_color='gray')

# 增加节点标签
labels = {author: author for author in G.nodes()}
nx.draw_networkx_labels(G, pos, labels=labels, font_size=10, font_color='black', font_family='sans-serif', verticalalignment='center')

# 增加标签偏移量，避免标签重叠
for label, (x, y) in pos.items():
    plt.text(x, y + 0.05, label, fontsize=10, ha='center', color='black')

# 设置图形标题和隐藏坐标轴
plt.title('作者合作网络', fontsize=20)
plt.axis('off')  # 关闭坐标轴

# 保存图像
plt.savefig("author_collaboration_network.png", format="PNG", dpi=300)

# 显示图形
plt.show()

# 7. 期刊发文偏好分析（可选）
journal_count = df.groupby('SrcDatabase').size().reset_index(name='论文发表数量')
print("期刊发文偏好分析：")
journal_count

# 绘制各期刊的发文数量
plt.figure(figsize=(14, 8))
sns.barplot(data=journal_count, x='SrcDatabase', y='论文发表数量', palette='Set2')
plt.title('“纺织科学与工程”领域中文期刊发文偏好分析', fontsize=16)
plt.xlabel('期刊名称', fontsize=14)
plt.ylabel('论文发表数量', fontsize=14)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

# 保存发文偏好分析图
plt.savefig("journal_publication_preference.png", format="PNG", dpi=300)

# 显示图形
plt.show()

# 保存作者合作网络的度中心性数据到CSV
degree_centrality_df = pd.DataFrame(degree_centrality.items(), columns=['Author', 'Degree Centrality'])
degree_centrality_df.to_csv("degree_centrality.csv", index=False)
journal_count
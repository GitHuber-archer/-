import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import ticker
from matplotlib.ticker import MaxNLocator

# 读取CNKI的文献数据
df = pd.read_csv('data.csv')  # 替换为你的文件路径

# 学校名称列表
schools = [
    '东华大学', '天津工业大学', '苏州大学', '浙江理工大学', '江南大学', '武汉纺织大学', 
    '西安工程大学', '大连工业大学', '青岛大学', '四川大学', '北京服装学院', '中原工学院', 
    '南通大学', '五邑大学', '嘉兴学院', '闽江学院', '河北科技大学', '安徽工程大学', 
    '江西服装学院', '成都纺织高等专科学校'
]

# 处理缺失值：将NaN或缺失的Organ值替换为空字符串
df['Organ'] = df['Organ'].fillna('')

# 确保Organ列的类型为字符串，便于匹配学校名称
df['Organ'] = df['Organ'].astype(str)

# 创建一个新的列，用于标记文献属于哪个学校
def match_school(organ_name):
    # 遍历学校名称，进行部分匹配（不区分大小写）
    for school in schools:
        if school in organ_name:  # 如果Organ中包含学校名
            return school
    return None  # 如果没有匹配到任何学校，返回None

# 创建新的列，标记每篇文献的学校
df['学校'] = df['Organ'].apply(match_school)

# 只保留那些匹配到学校的文献
school_papers = df[df['学校'].notnull()]

# 确保年份为整数类型，避免月份或其他格式干扰
school_papers['Year'] = school_papers['Year'].astype(int)

# 按照院校和年份统计论文发表数量
school_paper_count = school_papers.groupby(['学校', 'Year']).size().reset_index(name='论文发表数量')

# 设置Seaborn的样式
sns.set(style="whitegrid")

# 自定义颜色和线型，增加区分度
palette = sns.color_palette("Set2", len(school_paper_count['学校'].unique()))  # 使用Set2调色板
line_styles = ['-', '--', '-.', ':']  # 线型列表

# 创建一个画布
plt.figure(figsize=(14, 8))

# 绘制不同学校的论文数量随年份变化的曲线
for i, (school, data) in enumerate(school_paper_count.groupby('学校')):
    sns.lineplot(data=data, x='Year', y='论文发表数量', label=school, 
                 linestyle=line_styles[i % len(line_styles)],  # 循环使用线型
                 marker='o', markersize=7, color=palette[i])  # 通过调色板指定颜色

# 设置图表标题和标签
plt.title('不同院校“纺织科学与工程”专业论文发表量随时间演化特征', fontsize=16)
plt.xlabel('年份', fontsize=14)
plt.ylabel('论文发表数量', fontsize=14)

# 设置 y 轴为整数格式，并限定显示刻度范围为 [1, 2, 3, 4, 5]
plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True, prune='upper', nbins=5))  # 5个刻度

# 设置中文字体，防止方框问题（适用于 Windows）
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # Windows 用户可以使用 'Microsoft YaHei'
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# 确保x轴只显示年份，不显示月份
plt.xticks(ticks=range(2004, 2025), rotation=45)  # 只显示 2004 到 2024 年

# 添加图例，调整位置和大小
plt.legend(title='院校名称', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=12)

# 显示图表
plt.tight_layout()
plt.savefig('纺织论文.png') 
plt.show()

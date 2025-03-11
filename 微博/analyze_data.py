import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']  # 对于 macOS
plt.rcParams['axes.unicode_minus'] = False

# 读取数据
df = pd.read_csv('weibo_elderly_care_data.csv')

# 1. 基本统计信息
print("\n=== 基本统计信息 ===")
print(f"总数据条数: {len(df)}")
print("\n每个关键词的数据条数:")
print(df['keyword'].value_counts())

# 2. 互动数据统计
print("\n=== 互动数据统计 ===")
print("\n点赞数统计:")
print(df['likes'].describe())
print("\n评论数统计:")
print(df['comments'].describe())
print("\n转发数统计:")
print(df['reposts'].describe())

# 3. 生成互动数据箱线图
plt.figure(figsize=(12, 6))
df.boxplot(column=['likes', 'comments', 'reposts'])
plt.title('微博互动数据分布')
plt.ylabel('数量')
plt.savefig('interaction_stats.png')
plt.close()

# 4. 生成关键词分布图
plt.figure(figsize=(12, 6))
df['keyword'].value_counts().plot(kind='bar')
plt.title('关键词分布')
plt.xlabel('关键词')
plt.ylabel('数量')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('keyword_distribution.png')
plt.close()

# 5. 找出最受欢迎的帖子
print("\n=== 最受欢迎的帖子 ===")
print("\n点赞数最多的5条帖子:")
top_likes = df.nlargest(5, 'likes')[['username', 'content', 'likes', 'comments', 'reposts']]
print(top_likes)

print("\n评论数最多的5条帖子:")
top_comments = df.nlargest(5, 'comments')[['username', 'content', 'likes', 'comments', 'reposts']]
print(top_comments)

print("\n转发数最多的5条帖子:")
top_reposts = df.nlargest(5, 'reposts')[['username', 'content', 'likes', 'comments', 'reposts']]
print(top_reposts)

# 6. 生成时间分布图
df['publish_time'] = pd.to_datetime(df['publish_time'])
plt.figure(figsize=(12, 6))
df['publish_time'].dt.hour.hist(bins=24)
plt.title('发布时间分布')
plt.xlabel('小时')
plt.ylabel('数量')
plt.savefig('time_distribution.png')
plt.close()

print("\n分析完成！已生成以下图表：")
print("1. interaction_stats.png - 互动数据分布图")
print("2. keyword_distribution.png - 关键词分布图")
print("3. time_distribution.png - 发布时间分布图") 
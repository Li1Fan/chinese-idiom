import csv
import sqlite3

# 连接到 SQLite 数据库
conn = sqlite3.connect('idiom.db')
cursor = conn.cursor()

# 查询数据（去掉 id 列）
cursor.execute(
    'SELECT derivation, example, explanation, pinyin, word, abbreviation, pinyin_r, first, last FROM idiom')

# 获取列名
columns = [description[0] for description in cursor.description]

# 将数据写入 CSV 文件
with open('idiom.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(columns)  # 写入列名
    writer.writerows(cursor.fetchall())  # 写入数据

# 关闭连接
conn.close()

import sqlite3
import json

# 连接到 SQLite 数据库
conn = sqlite3.connect('idiom.db')
cursor = conn.cursor()

# 查询数据（去掉 id 列）
cursor.execute('SELECT derivation, example, explanation, pinyin, word, abbreviation, pinyin_r, first, last FROM idiom')

# 获取列名
columns = [description[0] for description in cursor.description]

# 将数据转换为字典列表
rows = [dict(zip(columns, row)) for row in cursor.fetchall()]

# 写入 JSON 文件
with open('idiom.json', 'w', encoding='utf-8') as jsonfile:
    json.dump(rows, jsonfile, ensure_ascii=False, indent=4)

# 关闭连接
conn.close()

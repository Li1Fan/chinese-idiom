import csv
import sqlite3

# 连接到 SQLite 数据库（如果数据库不存在，则会自动创建）
conn = sqlite3.connect('idiom.db')
cursor = conn.cursor()

# 创建表（如果表不存在），添加自增主键 id 和唯一约束 word
cursor.execute('''
CREATE TABLE IF NOT EXISTS idiom (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    derivation TEXT,
    example TEXT,
    explanation TEXT,
    pinyin TEXT,
    word TEXT UNIQUE,
    abbreviation TEXT,
    pinyin_r TEXT,
    first TEXT,
    last TEXT
)
''')

# 读取 CSV 文件并写入数据库
csv_file_path = 'data.csv'  # 请替换为你的 CSV 文件路径
with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
    csv_reader = csv.reader(csvfile)
    # 跳过表头
    next(csv_reader)
    # 将每一行数据插入到数据库中
    for row in csv_reader:
        try:
            cursor.execute('''
            INSERT INTO idiom (derivation, example, explanation, pinyin, word, abbreviation, pinyin_r, first, last)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', row)
        except sqlite3.IntegrityError:
            print(f"插入失败，word '{row[4]}' 已存在。")  # 提示唯一约束失败
            print(row)

# 提交事务并关闭连接
conn.commit()
conn.close()

print("数据已成功写入数据库！")

# 写一个sqlite3的测试程序
import sqlite3

# 连接到SQLite数据库
# 数据库文件是test.db
# 如果文件不存在，会自动在当前目录创建
conn = sqlite3.connect(r'D:\PyPrj\GitHub\chinese-idiom\data\idiom.db')
# 创建一个Cursor
cursor = conn.cursor()
# 执行一条SQL查询语句
cursor.execute('select * from idiom where derivation = "没有找到 cite 标签。"')
# 获得查询结果
values = cursor.fetchall()
print(len(values))

# 关闭Cursor
cursor.close()

# 提交事务
conn.commit()
# 关闭Connection
conn.close()

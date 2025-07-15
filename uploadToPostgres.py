# PostgreSQL 
# 字段：时间、链接、生成、主题

import psycopg2


# 数据库连接参数，请根据实际情况修改
DB_HOST = '192.168.31.129'
DB_PORT = '5431'
DB_NAME = 'knowledge'
DB_USER = 'handy'
DB_PASSWORD = 'hyh520888'

def connect():
    return psycopg2.connect(
                host=DB_HOST,
                port=DB_PORT,
                dbname=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD
            )

def initDB(conn):
    try:
        cur = conn.cursor()
        cur.execute('''
CREATE TABLE IF NOT EXISTS knowledge.knowledge (
    id SERIAL PRIMARY KEY,
    time TIMESTAMP NOT NULL,
    link TEXT NOT NULL,
    content TEXT,
    topic TEXT,
    CONSTRAINT unique_time_link UNIQUE (time, link)
);
''')
        conn.commit()
        print('建表成功')
        cur.close()
        conn.close()
    except Exception as e:
        print('数据库操作失败:', e)

def uploadlink(link, time, content=None, topic=None):
    """
    上传一条链接及相关信息到数据库
    :param link: 链接
    :param time: 时间（datetime对象或字符串）
    :param content: 内容（可选）
    :param topic: 主题（可选）
    """
    try:
        conn = connect()
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO knowledge.knowledge (time, link, content, topic)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT ON CONSTRAINT unique_time_link DO NOTHING;
        ''', (time, link, content, topic))
        conn.commit()
        cur.close()
        conn.close()
        print(f'插入成功: {link}')
    except Exception as e:
        print('插入失败:', e)

def updateContentTopic(link, time, content, topic):
    """
    根据链接和时间更新内容和主题
    :param link: 链接
    :param time: 时间（datetime对象或字符串）
    :param content: 内容
    :param topic: 主题
    """
    try:
        conn = connect()
        cur = conn.cursor()
        cur.execute('''
            UPDATE knowledge.knowledge
            SET content = %s, topic = %s
            WHERE link = %s AND time = %s
        ''', (content, topic, link, time))
        conn.commit()
        cur.close()
        conn.close()
        print(f'更新成功: {link}')
    except Exception as e:
        print('更新失败:', e)

"""
多角色聊天机器人 - 数据库层
使用 SQLite 存储对话历史
"""

import sqlite3
import os
from datetime import datetime


# 数据库文件路径（存放在项目根目录）
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "chat_history.db")


def get_connection():
    """获取数据库连接"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """初始化数据库，创建必要的表"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            character TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


def save_message(role, content, character):
    """保存一条消息到数据库"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO messages (role, content, character) VALUES (?, ?, ?)",
        (role, content, character)
    )
    conn.commit()
    conn.close()


def load_history(character=None, limit=50):
    """加载对话历史，可按角色筛选"""
    conn = get_connection()
    cursor = conn.cursor()
    if character:
        cursor.execute(
            "SELECT * FROM messages WHERE character = ? ORDER BY timestamp ASC LIMIT ?",
            (character, limit)
        )
    else:
        cursor.execute(
            "SELECT * FROM messages ORDER BY timestamp ASC LIMIT ?",
            (limit,)
        )
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def clear_history(character=None):
    """清空对话历史，可按角色清空"""
    conn = get_connection()
    cursor = conn.cursor()
    if character:
        cursor.execute("DELETE FROM messages WHERE character = ?", (character,))
    else:
        cursor.execute("DELETE FROM messages")
    conn.commit()
    conn.close()

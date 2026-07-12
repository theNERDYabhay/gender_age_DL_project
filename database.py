
import sqlite3
from config import DATABASE

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def insert_scan(image_path, age, gender, compliment, confidence, consent):
    conn = get_db()
    conn.execute(
        '''INSERT INTO scans
        (image_path, age, gender, compliment, confidence, consent)
        VALUES (?, ?, ?, ?, ?, ?)''',
        (image_path, age, gender, compliment, confidence, int(consent))
    )
    conn.commit()
    conn.close()

def get_all_scans():
    conn = get_db()
    rows = conn.execute("SELECT * FROM scans ORDER BY created_at DESC").fetchall()
    conn.close()
    return rows

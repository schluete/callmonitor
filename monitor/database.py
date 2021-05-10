#  database.py
#  callmonitor
#  Created by Axel Schlueter on 10.05.21.

import sqlite3
from contextlib import contextmanager

@contextmanager
def _database():
    conn = sqlite3.connect("monitor.db")
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS calls (
                        msg_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                        text VARCHAR,
                        created_at DATETIME)""")
    conn.commit()
    try:
        yield conn
    finally:
        conn.close()

def check(msg_id):
    with _database() as db:
        rs = db.cursor().execute(f"SELECT count(*) FROM calls WHERE msg_id = {msg_id}").fetchone()
        return rs[0] > 0

def mark(msg_id, text):
    with _database() as db:
        db.cursor().execute("INSERT INTO calls VALUES(?, ?, datetime('now'))", (msg_id, text))
        db.commit()
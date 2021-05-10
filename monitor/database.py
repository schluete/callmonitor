#  database.py
#  callmonitor
#  Created by Axel Schlueter on 10.05.21.

import sqlite3
from contextlib import contextmanager
from monitor.utils import is_docker

DATABASE_FILE = "monitor.db" if not is_docker() else "/database/monitor.db"

@contextmanager
def _database():
    conn = sqlite3.connect(DATABASE_FILE)
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
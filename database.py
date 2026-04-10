import sqlite3

def setup_db():
    conn = sqlite3.connect("notes.db")
    with conn:
        c = conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            content TEXT
        )""")
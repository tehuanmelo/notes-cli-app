import sqlite3

def setup_db():
    conn = sqlite3.connect("notes.db")
    c = conn.cursor()
    with conn:
        c.execute("""CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            content TEXT
        )""")
        
def create_note(title: str, content: str) -> None:
    conn = sqlite3.connect("notes.db")
    c = conn.cursor()
    with conn:
        c.execute("INSERT INTO notes (title, content) VALUES (?, ?)", (title, content))

def get_all_notes():
    conn = sqlite3.connect("notes.db")
    c = conn.cursor()
    with conn:
        c.execute("SELECT * FROM notes")
        return c.fetchall()
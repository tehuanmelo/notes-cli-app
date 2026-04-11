import sqlite3
from model import Note

def setup_db():
    conn = sqlite3.connect("notes.db")
    c = conn.cursor()
    with conn:
        c.execute("""CREATE TABLE IF NOT EXISTS notes (
            title TEXT,
            content TEXT,
            id INTEGER PRIMARY KEY AUTOINCREMENT
        )""")
        
def create_note(title: str, content: str) -> Note:
    conn = sqlite3.connect("notes.db")
    c = conn.cursor()
    with conn:
        c.execute("INSERT INTO notes (title, content) VALUES (?, ?)", (title, content))
        note_id = c.lastrowid
    return Note(title, content, note_id)

def get_all_notes():
    conn = sqlite3.connect("notes.db")
    c = conn.cursor()
    with conn:
        c.execute("SELECT * FROM notes")
        notes = c.fetchall()
        return [Note(*note) for note in notes] if notes else []

def delete_note(note_id: int):
    conn = sqlite3.connect("notes.db")
    c = conn.cursor()
    with conn:
        c.execute("DELETE FROM notes WHERE id = ?", (note_id, ))
        
def update_note(title, content, note_id):
    if not title: return
    conn = sqlite3.connect("notes.db")
    c = conn.cursor()
    with conn:
        c.execute("UPDATE notes SET title=?, content=? WHERE id=?", (title, content, note_id))
        
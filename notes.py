from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Label, Button, TextArea, Input
from textual.containers import Horizontal, Vertical
from database import setup_db, create_note, get_all_notes

class NotesApp(App):
    
    CSS_PATH = "notes.css"

    def on_mount(self):
        setup_db()
    
    def compose(self):
        yield Header()
        with Horizontal():
            with Vertical(id="sidebar"):
                yield Button("New Note", id="new-note-btn")
            with Vertical(id="main-app"):
                yield Input(placeholder="Enter the note title here...", id="note-title")
                yield TextArea(id="text-area")
        yield Footer()
        
    def on_button_pressed(self, event):
        sidebar = self.query_one("#sidebar")
        content_box = self.query_one("#text-area")
        title_input = self.query_one("#note-title")
        
        note_content = content_box.text
        note_title = title_input.value
        
        create_note(note_title, note_content)
        
        sidebar.mount(Label(note_title))
        content_box.text = ""
        title_input.value = ""
        
        sidebar.mount(Label("Note saved"))
        
        
if __name__ == "__main__":
    app = NotesApp()
    app.run()
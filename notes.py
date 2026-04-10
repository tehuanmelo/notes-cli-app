from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Label, Button, TextArea
from textual.containers import Horizontal, Vertical
from database import setup_db

class NotesApp(App):
    
    CSS_PATH = "notes.css"
    
    def compose(self):
        yield Header()
        with Horizontal():
            with Vertical(id="sidebar"):
                yield Button("New Note", id="new-note-btn")
            yield TextArea(id="text-area")
        yield Footer()
        
    def on_button_pressed(self):
        new_note = self.query_one("#new-note-btn", Button)
        new_note.label = "Hello World!"
        
        
if __name__ == "__main__":
    app = NotesApp()
    app.run()
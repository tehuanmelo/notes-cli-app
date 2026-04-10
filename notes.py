from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Label, Button, TextArea, Input
from textual.containers import Horizontal, Vertical, VerticalScroll
from database import setup_db, create_note, get_all_notes

class NotesApp(App):
    
    CSS_PATH = "notes.css"

    def on_mount(self):
        setup_db()
        self.update_sidebar()
    
    def compose(self):
        yield Header()
        with Horizontal():
            with Vertical(id="sidebar"):
                yield Button("New Note", id="new-note-btn")
                with VerticalScroll(id="notes-list"):
                    pass
            with Vertical(id="main-app"):
                yield Input(placeholder="Enter the note title here...", id="note-title")
                yield TextArea(id="text-area")
        yield Footer()
        
    def on_button_pressed(self, event):
        notes_list = self.query_one("#notes-list")
        content_box = self.query_one("#text-area")
        title_input = self.query_one("#note-title")
        
        note_content = content_box.text
        note_title = title_input.value
        
        create_note(note_title, note_content)
        
        notes_list.mount(Label(note_title))
        content_box.text = ""
        title_input.value = ""
        
        notes_list.mount(Label("Note saved"))
    
    def update_sidebar(self):
        notes_list = self.query_one("#notes-list")
        notes_list.query(Label).remove()
        for note in get_all_notes():
            notes_list.mount(Label(note.title))
        
        
        
if __name__ == "__main__":
    app = NotesApp()
    app.run()
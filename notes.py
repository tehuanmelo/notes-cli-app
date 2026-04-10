from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Label, Button, TextArea, Input
from textual.containers import Horizontal, Vertical, VerticalScroll
from database import setup_db, create_note, get_all_notes

class NotesApp(App):
    
    CSS_PATH = "notes.css"
    BINDINGS = [("ctrl+s", "save_note", "Save the current note")]

    def on_mount(self):
        setup_db()
        self.update_sidebar()


    def compose(self):
        yield Header()
        with Horizontal():
            with VerticalScroll(id="sidebar"):
                pass
            with Vertical(id="main-app"):
                yield Input(placeholder="Enter the note title here...", id="note-title")
                yield TextArea(id="text-area")
        yield Footer()
 
    
    def update_sidebar(self):
        sidebar = self.query_one("#sidebar")
        sidebar.query(Label).remove()
        for note in get_all_notes():
            sidebar.mount(Label(note.title))

       
    def action_save_note(self):
        title_input = self.query_one("#note-title")
        content_input = self.query_one("#text-area")
        create_note(title_input.value, content_input.text)
        self.update_sidebar()
        title_input.value = ""
        content_input.text = ""
        
        
        
if __name__ == "__main__":
    app = NotesApp()
    app.run()
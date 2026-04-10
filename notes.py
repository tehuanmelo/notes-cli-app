from textual.app import App
from textual.widgets import Header, Footer, Label, TextArea, Input, ListView, ListItem
from textual.containers import Horizontal, Vertical, VerticalScroll
from database import setup_db, create_note, get_all_notes, delete_note
from model import Note

class NotesApp(App):
    def __init__(self):
        super().__init__()
        self.current_note = None
    
    CSS_PATH = "notes.css"
    BINDINGS = [
        ("ctrl+s", "save_note", "Save the current note"),
        ("ctrl+n", "new_note", "Create new note"),
    ]

    def on_mount(self):
        setup_db()
        self.update_sidebar()
        self.query_one("#note-title").focus()


    def compose(self):
        yield Header()
        with Horizontal():
            with ListView(id="sidebar"):
                pass
            with Vertical(id="main-app"):
                yield Input(placeholder="Enter the note title here...", id="note-title")
                yield TextArea(id="text-area")
        yield Footer()
 
    def append_item_to_sidebar(self, note: Note):
        sidebar = self.query_one("#sidebar")
        item = ListItem(Label(note.title))
        item.note = note
        sidebar.append(item)
    
    def update_sidebar(self):
        sidebar = self.query_one("#sidebar")
        sidebar.clear()
        for note in get_all_notes():
            self.append_item_to_sidebar(note)


    def action_new_note(self):
        self.current_note = None
        title_input = self.query_one("#note-title").focus()
        content_input = self.query_one("#text-area")
        title_input.value = ""
        content_input.text = ""

       
    def action_save_note(self):
        title_input = self.query_one("#note-title")
        content_input = self.query_one("#text-area")
        sidebar = self.query_one("#sidebar")
        if not title_input.value:
            return
        if self.current_note is None:
            note = create_note(title_input.value, content_input.text)
            self.current_note = note
            self.append_item_to_sidebar(note)
            sidebar.index = len(sidebar.children) - 1
            sidebar.focus()
            return
        else:
            pass
        self.update_sidebar()


    def on_list_view_selected(self, event: ListView.Selected):
        sidebar = self.query_one("#sidebar")
        self.current_note = event.item.note
        title_input = self.query_one("#note-title")
        content_input = self.query_one("#text-area")
        title_input.value = self.current_note.title
        content_input.text = self.current_note.content


    def on_list_view_highlighted(self, event: ListView.Highlighted):
        if event.item is None:
            return
        self.current_note = event.item.note
        title_input = self.query_one("#note-title")
        content_input = self.query_one("#text-area")
        title_input.value = self.current_note.title
        content_input.text = self.current_note.content
        
        
if __name__ == "__main__":
    app = NotesApp()
    app.run()
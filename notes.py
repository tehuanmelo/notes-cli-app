from textual.app import App
from textual.widgets import Header, Footer, Label, TextArea, Input, ListView, ListItem
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
            with ListView(id="sidebar"):
                pass
            with Vertical(id="main-app"):
                yield Input(placeholder="Enter the note title here...", id="note-title")
                yield TextArea(id="text-area")
        yield Footer()
 
    
    def update_sidebar(self):
        sidebar = self.query_one("#sidebar")
        sidebar.clear()
        for note in get_all_notes():
            item = ListItem(Label(note.title))
            item.note = note
            sidebar.mount(item)

       
    def action_save_note(self):
        title_input = self.query_one("#note-title")
        content_input = self.query_one("#text-area")
        create_note(title_input.value, content_input.text)
        self.update_sidebar()
        title_input.value = ""
        content_input.text = ""


    def on_list_view_selected(self, event: ListView.Selected):
        selected_note = event.item.note
        title_input = self.query_one("#note-title")
        content_input = self.query_one("#text-area")
        title_input.value = selected_note.title
        content_input.text = selected_note.content


    def on_list_view_highlighted(self, event: ListView.Highlighted):
        selected_note = event.item.note
        title_input = self.query_one("#note-title")
        content_input = self.query_one("#text-area")
        title_input.value = selected_note.title
        content_input.text = selected_note.content
        
        
if __name__ == "__main__":
    app = NotesApp()
    app.run()
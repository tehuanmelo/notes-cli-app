from textual.app import App
from textual.widgets import Label, TextArea, Input, ListView, ListItem, Static
from textual.containers import Horizontal, Vertical
from database import setup_db, create_note, get_all_notes, delete_note, update_note
from model import Note
from textual.binding import Binding

class NotesApp(App):
    def __init__(self):
        super().__init__()
        self.current_note = None
        
    
    CSS_PATH = "notes.css"
    BINDINGS = [
        Binding("ctrl+s", "save_note", "Save the current note", priority=True),
        Binding("ctrl+n", "new_note", "Create new note", priority=True),
        Binding("ctrl+d", "delete_note", "Delete current note", priority=True),
        Binding("ctrl+q", "do_nothing", "Disabled", priority=True),
        Binding("ctrl+e", "quit", "Quit", priority=True),
    ]
    
    def _select_note(self, index: int) -> None:
        self.notes_list.index = index
        self.notes_list.focus()

    def on_mount(self):
        setup_db()
        self.note_title_input = self.query_one("#note-title").focus()
        self.note_content_area = self.query_one("#text-area")
        self.notes_list = self.query_one("#notes-list")
        self.search_input = self.query_one("#search")

        self.update_notes_list()

    def compose(self):
        yield Static("Notes App", id="header")
        with Horizontal():
            with Vertical(id="sidebar"):
                yield Input(placeholder="Search...", id="search", classes="box")
                yield ListView(id="notes-list", classes="box")
            with Vertical(id="main-app"):
                yield Input(placeholder="Enter the note title...", id="note-title", classes="box")
                yield TextArea(placeholder="Enter the note content...", id="text-area", classes="box")
        yield Static("[orange]^s[/orange] Save the current note   [orange]^n[/orange] Create new note   [orange]^d[/orange] Delete current note   [orange]^e[/orange] Exit the app" , id="keybar")
 
    def append_item_to_notes_list(self, note: Note):
        self.notes_list
        item = ListItem(Label(note.title))
        item.note = note
        self.notes_list.append(item)
    
    def update_notes_list(self):
        self.notes_list.clear()
        selected_note = None
        for idx, note in enumerate(get_all_notes()):
                self.append_item_to_notes_list(note)
                if self.current_note and self.current_note.note_id == note.note_id:
                    selected_note = idx
        if selected_note is not None:
            self.set_timer(0.01, lambda idx=selected_note: self._select_note(idx))


    def action_new_note(self):
        self.current_note = None
        self.note_title_input.focus()
        self.note_content_area
        self.note_title_input.value = ""
        self.note_content_area.text = ""

 
    def action_delete_note(self):
        # delete the current note from the database if is not None
        if self.current_note is not None:
            delete_note(self.current_note.note_id)
            # set the current note to None
            self.current_note = None
        # update the notes_list
        self.update_notes_list()
        self.action_new_note()
        self.search_input.focus()


    def action_save_note(self):
        if not self.note_title_input.value:
            return
        if self.current_note is None:
            note = create_note(self.note_title_input.value, self.note_content_area.text)
            self.current_note = note
        else:
            update_note(self.note_title_input.value, self.note_content_area.text, self.current_note.note_id)
        self.search_input.value = ""
        self.update_notes_list()
        self.notify(f"Note saved")


    def on_list_view_selected(self, event: ListView.Selected):
        self.current_note = event.item.note
        self.note_title_input.value = self.current_note.title
        self.note_content_area.text = self.current_note.content


    def on_list_view_highlighted(self, event: ListView.Highlighted):
        if event.item is None:
            return
        self.current_note = event.item.note
        self.note_title_input.value = self.current_note.title
        self.note_content_area.text = self.current_note.content


    def on_input_changed(self, event: Input.Changed):
        if event.input.id == self.search_input.id:
            self.notes_list.clear()
            for note in get_all_notes():
                if self.search_input.value:
                    if self.search_input.value.lower() in note.title.lower():
                        self.append_item_to_notes_list(note)
                else:
                    self.append_item_to_notes_list(note)


if __name__ == "__main__":
    app = NotesApp()
    app.run()

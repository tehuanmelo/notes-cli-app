from textual.app import App
from textual.widgets import Label, TextArea, Input, ListView, ListItem, Static
from textual.containers import Horizontal, Vertical
from src.data.database import setup_db, create_note, get_all_notes, delete_note, update_note
from src.models.model import Note
from textual.binding import Binding
from datetime import datetime

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
        self.note_content_area = self.query_one("#text-area").focus()
        self.notes_list = self.query_one("#notes-list")
        self.search_input = self.query_one("#search")
        self.header_dates = self.query_one("#header-dates")

        self.update_notes_list()
        self.header_dates.update("[orange]New Note[/orange]")


    def compose(self):
        with Horizontal(id="header"):
            yield Label("Notes App", id="header-title")
            yield Label("", id="header-dates")
        with Horizontal():
            with Vertical(id="sidebar"):
                yield Input(placeholder="Search...", id="search", classes="box")
                yield ListView(id="notes-list", classes="box")
            with Vertical(id="main-app"):
                yield TextArea(placeholder="Enter the note content...", id="text-area", classes="box", language="python")
        yield Static("[orange]^s[/orange] Save the current note   [orange]^n[/orange] Create new note   [orange]^d[/orange] Delete current note   [orange]^e[/orange] Exit the app" , id="keybar")
 
 
    def append_item_to_notes_list(self, note: Note):
        note_date = datetime.fromisoformat(note.updated_at).strftime("%d-%m-%Y")
        item = ListItem(
            Horizontal(
                Label(note.title, classes="note-title"),
                Label(note_date, classes="note-date"),
                classes="list-item"
            )
        )
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
        self.note_content_area.focus()
        self.header_dates.update("[orange]New Note[/orange]")
        self.note_content_area.text = ""

 
    def action_delete_note(self):
        # delete the current note from the database if is not None
        if self.current_note is not None:
            delete_note(self.current_note.note_id)
            # set the current note to None
            self.notify(f"{self.current_note.title} deleted.", severity="error")
            self.current_note = None
        # update the notes_list
        self.update_notes_list()
        self.action_new_note()
        self.search_input.focus()
        
    
    def get_note_title(self):
        first_line = self.note_content_area.text.strip().split("\n")[0].split()
        if len(first_line) > 3:
            title = " ".join(first_line[:3]) + "..."
        else:
            title = " ".join(first_line)
        return title or "New Note"


    def action_save_note(self):
        title = self.get_note_title()
        if self.current_note is None:
            note = create_note(title, self.note_content_area.text)
            self.current_note = note
            self.notify(f"{title} saved")
        else:
            update_note(title, self.note_content_area.text, self.current_note.note_id)
            self.notify(f"{title} updated", severity="warning")
        self.update_notes_list()


    def update_header(self):
        if self.current_note is not None:
            str_format = "%d %B, %Y %H:%M"
            date_created = datetime.fromisoformat(self.current_note.created_at).strftime(str_format)
            date_updated = datetime.fromisoformat(self.current_note.updated_at).strftime(str_format)
            if date_created == date_updated:
                self.header_dates.update(f"[orange]Date created:[/orange] {date_created}")
            else:
                self.header_dates.update(f"[orange]Date created:[/orange] {date_created} [orange]Last update:[/orange] {date_updated}")
        else:
            self.header_dates.update("")
            

    def on_list_view_selected(self, event: ListView.Selected):
        self.current_note = event.item.note
        self.note_content_area.text = self.current_note.content
        self.update_header()


    def on_list_view_highlighted(self, event: ListView.Highlighted):
        if event.item is None:
            return
        self.current_note = event.item.note
        self.note_content_area.text = self.current_note.content
        self.update_header()


    def on_input_changed(self, event: Input.Changed):
        if event.input.id == self.search_input.id:
            self.notes_list.clear()
            for note in get_all_notes():
                if self.search_input.value:
                    if self.search_input.value.lower() in note.title.lower() or \
                    self.search_input.value.lower() in note.content.lower():
                        self.append_item_to_notes_list(note)
                else:
                    self.append_item_to_notes_list(note)

def main():
    app = NotesApp()
    app.run()
    
if __name__ == "__main__":
    main()
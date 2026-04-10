from textual.widgets import Static

class Note(Static):
    def __init__(self, title="New Note", content=None, note_id=None):
        super().__init__(title)
        self.content = content
        self.id = note_id
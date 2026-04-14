from textual.widgets import Static

class Note(Static):
    def __init__(self, title="New Note", content=None,
                 created_at=None, updated_at=None, note_id=None):
        super().__init__(title)
        self.title = title
        self.content = content
        self.created_at = created_at
        self.updated_at = updated_at
        self.note_id = note_id
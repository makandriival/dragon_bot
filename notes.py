class Notes:
    """Class for managing notes."""

    def __init__(self):
        self.notes = []

    def add_note(self, note: str):
        """Add a new note."""
        self.notes.append(note)
        return "Note added."

    def get_notes(self) -> list[str]:
        return self.notes

    def delete_note(self, index: int):
        if 0 <= index < len(self.notes):
            return self.notes.pop(index)
        return None

    def edit_note(self, index: int, new_note: str):
        if 0 <= index < len(self.notes):
            self.notes[index] = new_note
            return True
        return False

    def search_notes(self, keyword: str) -> list[str]:
        return [note for note in self.notes if keyword.lower() in note.lower()]
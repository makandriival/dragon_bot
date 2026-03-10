class Notes:
    """Class for managing notes."""

    def __init__(self):
        self.notes = []

    # will make all the methods private
    def __add_note(self, note: str):
        """Add a new note."""
        self.notes.append(note)
        return "Note added."

    def __get_notes(self) -> list[str]:
        return self.notes

    def __delete_note(self, index: int):
        if 0 <= index < len(self.notes):
            return self.notes.pop(index)
        return None

    def __edit_note(self, index: int, new_note: str):
        if 0 <= index < len(self.notes):
            self.notes[index] = new_note
            return True
        return False

    def __search_notes(self, keyword: str) -> list[str]:
        return [note for note in self.notes if keyword.lower() in note.lower()]
    
    # public methods will be nothing returning
    # and will get arguments like command string words
    # and will call the private methods
    # method print message for user to console
    # method raise extensions 
    # if arguments don't match the expected format
    def add_note(self, *args):
        pass
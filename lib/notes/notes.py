import pickle

class Notes:
    """Class for managing notes."""

    def __init__(self):
        self.notes = []

    # example of public methods that will be called by the interface
    # public methods will be nothing returning
    # and will get arguments like command string words
    def add_note(self, *args):
        if len(args) != 1:
            # method raise exceptions 
            # if arguments don't match the expected format
            raise ValueError("add_note command requires exactly one argument.")
        note = args[0]
        # and will call the private methods
        # method print message for user to console
        print(self.__add_note(note))
        with open("notes.pkl", "wb") as f:
            pickle.dump(self.notes, f)

    def get_notes(self, *args):
        pass

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

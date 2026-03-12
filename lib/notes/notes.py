import pickle
from pathlib import Path
from ..writer import write_message


class Notes:
    """Class for managing notes."""

    def __init__(self):
        self.notes = []
        self.file_path = Path("notes.pkl")
        self.__load_notes()

    # public methods (called by interface)

    def add_note(self, *args):
        if len(args) != 1:
            raise ValueError("add_note command requires exactly one argument.")

        note = args[0]

        write_message(self.__add_note(note), "info")
        self.__save_notes()

    def get_notes(self, *args):
        if len(args) != 0:
            raise ValueError("get_notes command does not take arguments.")

        notes = self.__get_notes()

        if not notes:
            write_message("No notes found.", "info")
            return

        message = "\n".join(
            f"{i+1}. {note}" for i, note in enumerate(notes)
        )

        write_message(message, "info")

    def delete_note(self, *args):
        if len(args) != 1:
            raise ValueError("delete_note command requires exactly one argument.")

        if not args[0].isdigit():
            raise ValueError("delete_note argument must be a note number.")

        index = int(args[0]) - 1
        deleted = self.__delete_note(index)

        if deleted is None:
            raise ValueError("Note with this number does not exist.")

        write_message("Note deleted.", "info")
        self.__save_notes()

    def edit_note(self, *args):
        if len(args) < 2:
            raise ValueError("edit_note command requires note number and new text.")

        if not args[0].isdigit():
            raise ValueError("First argument must be a note number.")

        index = int(args[0]) - 1
        new_note = " ".join(args[1:])

        success = self.__edit_note(index, new_note)

        if not success:
            raise ValueError("Note with this number does not exist.")

        write_message("Note updated.", "info")
        self.__save_notes()

    def search_notes(self, *args):
        if len(args) != 1:
            raise ValueError("search_notes command requires exactly one argument.")

        keyword = args[0]

        results = self.__search_notes(keyword)

        if not results:
            write_message("No matching notes.", "info")
            return

        message = "\n".join(
            f"{i+1}. {note}" for i, note in enumerate(results)
        )

        write_message(message, "info")

    # private methods

    def __add_note(self, note: str):
        self.notes.append(note)
        return "Note added."

    def __get_notes(self):
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

    def __search_notes(self, keyword: str):
        return [note for note in self.notes if keyword.lower() in note.lower()]

    def __save_notes(self):
        with open(self.file_path, "wb") as f:
            pickle.dump(self.notes, f)

    def __load_notes(self):
        if not self.file_path.exists():
            return

        try:
            with open(self.file_path, "rb") as f:
                self.notes = pickle.load(f)
        except Exception:
            self.notes = []
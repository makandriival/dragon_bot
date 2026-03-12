from ..writer import write_message
from ..bot_exceptions import NotEnoughArgumentsError
from ..data_source.actions import write_to_file, read_from_file


class Notes:
    """Class for managing notes."""

    def __init__(self):
        self.notes = read_from_file("notes")

    def add_note(self, *args):
        if len(args) < 1:
            # method raise not enough arguments exception if the number
            # of arguments is less than the expected number
            raise NotEnoughArgumentsError
        elif len(args) > 1:
            # method print message for user to console if the number of
            # arguments is more than the expected number
            write_message(
                "Too many arguments provided. Some arguments were not used",
                "warning")
        note = args[0]

        write_message(self.__add_note(note), "info")
        # save changes to file after adding a note
        write_to_file(self.notes, "notes")

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
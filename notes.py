import pickle
from pathlib import Path
from ..writer import write_message


class Notes:
    """Class for managing notes and note tags."""

    def __init__(self):
        self.notes = []
        self.file_path = Path(__file__).resolve().parents[2] / "notes.pkl"
        self.__load_notes()

    # =========================
    # Public command handlers
    # =========================

    def add_note(self, *args):
        """
        Command format:
        add_note "note text"
        """
        if len(args) != 1:
            raise ValueError('add_note command requires exactly one argument: "note text".')

        note_text = args[0].strip()
        if not note_text:
            raise ValueError("Note text cannot be empty.")

        message = self.__add_note(note_text)
        self.__save_notes()
        write_message(message, "info")

    def get_notes(self, *args):
        """
        Command format:
        get_notes
        """
        if len(args) != 0:
            raise ValueError("get_notes command does not take arguments.")

        notes = self.__get_notes()

        if not notes:
            write_message("No notes found.", "info")
            return

        for index, note in enumerate(notes, start=1):
            tags = ", ".join(note["tags"]) if note["tags"] else "no tags"
            write_message(f'{index}. {note["text"]} | tags: {tags}', "info")

    def edit_note(self, *args):
        """
        Command format:
        edit_note <index> "new note text"
        """
        if len(args) != 2:
            raise ValueError('edit_note command requires exactly two arguments: <index> "new note text".')

        index = self.__parse_index(args[0])
        new_text = args[1].strip()

        if not new_text:
            raise ValueError("New note text cannot be empty.")

        message = self.__edit_note(index, new_text)
        self.__save_notes()
        write_message(message, "info")

    def delete_note(self, *args):
        """
        Command format:
        delete_note <index>
        """
        if len(args) != 1:
            raise ValueError("delete_note command requires exactly one argument: <index>.")

        index = self.__parse_index(args[0])

        message = self.__delete_note(index)
        self.__save_notes()
        write_message(message, "info")

    def search_notes(self, *args):
        """
        Command format:
        search_notes "keyword"
        """
        if len(args) != 1:
            raise ValueError('search_notes command requires exactly one argument: "keyword".')

        keyword = args[0].strip()
        if not keyword:
            raise ValueError("Search keyword cannot be empty.")

        results = self.__search_notes(keyword)

        if not results:
            write_message("No matching notes found.", "info")
            return

        for index, note in results:
            tags = ", ".join(note["tags"]) if note["tags"] else "no tags"
            write_message(f'{index + 1}. {note["text"]} | tags: {tags}', "info")

    def add_tag(self, *args):
        """
        Command format:
        add_tag <index> "tag"
        """
        if len(args) != 2:
            raise ValueError('add_tag command requires exactly two arguments: <index> "tag".')

        index = self.__parse_index(args[0])
        tag = args[1].strip().lower()

        if not tag:
            raise ValueError("Tag cannot be empty.")

        message = self.__add_tag(index, tag)
        self.__save_notes()
        write_message(message, "info")

    def search_by_tag(self, *args):
        """
        Command format:
        search_by_tag "tag"
        """
        if len(args) != 1:
            raise ValueError('search_by_tag command requires exactly one argument: "tag".')

        tag = args[0].strip().lower()
        if not tag:
            raise ValueError("Tag cannot be empty.")

        results = self.__search_by_tag(tag)

        if not results:
            write_message("No notes found for this tag.", "info")
            return

        for index, note in results:
            tags = ", ".join(note["tags"]) if note["tags"] else "no tags"
            write_message(f'{index + 1}. {note["text"]} | tags: {tags}', "info")

    def sort_by_tags(self, *args):
        """
        Command format:
        sort_by_tags
        """
        if len(args) != 0:
            raise ValueError("sort_by_tags command does not take arguments.")

        sorted_notes = self.__sort_by_tags()

        if not sorted_notes:
            write_message("No notes found.", "info")
            return

        for index, note in enumerate(sorted_notes, start=1):
            tags = ", ".join(note["tags"]) if note["tags"] else "no tags"
            write_message(f'{index}. {note["text"]} | tags: {tags}', "info")

    # =========================
    # Private helpers
    # =========================

    def __add_note(self, note_text: str) -> str:
        self.notes.append({"text": note_text, "tags": []})
        return "Note added."

    def __get_notes(self) -> list:
        return self.notes

    def __delete_note(self, index: int) -> str:
        note = self.notes.pop(index)
        return f'Note deleted: "{note["text"]}"'

    def __edit_note(self, index: int, new_text: str) -> str:
        old_text = self.notes[index]["text"]
        self.notes[index]["text"] = new_text
        return f'Note updated: "{old_text}" -> "{new_text}"'

    def __search_notes(self, keyword: str) -> list:
        keyword = keyword.lower()
        return [
            (index, note)
            for index, note in enumerate(self.notes)
            if keyword in note["text"].lower()
        ]

    def __add_tag(self, index: int, tag: str) -> str:
        if tag in self.notes[index]["tags"]:
            raise ValueError("This tag already exists for the selected note.")

        self.notes[index]["tags"].append(tag)
        self.notes[index]["tags"].sort()
        return f'Tag "{tag}" added to note.'

    def __search_by_tag(self, tag: str) -> list:
        return [
            (index, note)
            for index, note in enumerate(self.notes)
            if tag in note["tags"]
        ]

    def __sort_by_tags(self) -> list:
        return sorted(
            self.notes,
            key=lambda note: (note["tags"], note["text"].lower())
        )

    def __parse_index(self, raw_index) -> int:
        try:
            index = int(raw_index)
        except (TypeError, ValueError):
            raise ValueError("Index must be a positive integer.")

        if index < 1:
            raise ValueError("Index must be greater than 0.")

        real_index = index - 1

        if real_index >= len(self.notes):
            raise ValueError("Note with this index does not exist.")

        return real_index

    def __save_notes(self):
        with open(self.file_path, "wb") as file:
            pickle.dump(self.notes, file)

    def __load_notes(self):
        if not self.file_path.exists():
            self.notes = []
            return

        try:
            with open(self.file_path, "rb") as file:
                loaded_notes = pickle.load(file)

            self.notes = self.__normalize_loaded_notes(loaded_notes)
        except (pickle.PickleError, EOFError, FileNotFoundError):
            self.notes = []

    def __normalize_loaded_notes(self, loaded_notes):
        """
        Supports both:
        - new format: [{"text": "...", "tags": [...]}]
        - old format: ["note 1", "note 2"]
        """
        normalized = []

        if not isinstance(loaded_notes, list):
            return normalized

        for item in loaded_notes:
            if isinstance(item, str):
                normalized.append({"text": item, "tags": []})
            elif isinstance(item, dict):
                text = str(item.get("text", "")).strip()
                tags = item.get("tags", [])

                if not text:
                    continue

                if not isinstance(tags, list):
                    tags = []

                clean_tags = sorted(
                    {str(tag).strip().lower() for tag in tags if str(tag).strip()}
                )

                normalized.append({"text": text, "tags": clean_tags})

        return normalized
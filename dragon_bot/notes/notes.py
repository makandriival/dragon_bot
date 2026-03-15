from dragon_bot.writer import write_message
from dragon_bot.bot_exceptions import (
    NotEnoughArgumentsError,
    NoteNotFoundError,
    InvalidCommandError,
)
from dragon_bot.data_source.actions import write_to_file, read_from_file


class Notes:
    """Class for managing notes."""

    def __init__(self):
        stored_data = read_from_file("notes")

        if isinstance(stored_data, dict):
            self.notes = stored_data.get("notes", [])
            self.next_id = stored_data.get("next_id", 1)
        else:
            self.notes = []
            self.next_id = 1

    def add_note(self, *args):
        if len(args) < 1:
            raise NotEnoughArgumentsError(
                "add-note command requires note text.")

        if len(args) > 1:
            write_message(
                "Warning: extra arguments detected."
                " They were joined into one note text.",
                "warning",
            )

        note_text = " ".join(args).strip()

        if not note_text:
            raise InvalidCommandError("Note text cannot be empty.")

        note = self.__add_note(note_text)
        self.__save()

        write_message(f"Note added: [{note['id']}] {note['text']}", "info")

    def get_notes(self, *args):
        if len(args) > 0:
            write_message(
                "Warning: get-notes does not need arguments."
                " Extra arguments were ignored.",
                "warning",
            )

        notes = self.__get_notes()

        if not notes:
            write_message("No notes found.", "info")
            return

        for note in notes:
            self.__print_note(note)

    def delete_note(self, *args):
        if len(args) < 1:
            raise NotEnoughArgumentsError(
                "delete-note command requires note id.")

        if len(args) > 1:
            write_message(
                "Warning: extra arguments detected."
                " Only the first argument was used as note id.",
                "warning",
            )

        note_id = self.__parse_note_id(args[0])
        deleted_note = self.__delete_note(note_id)

        if deleted_note is None:
            raise NoteNotFoundError(f"Note with id {note_id} not found.")

        self.__save()
        write_message(f"Note deleted: [{deleted_note['id']}]"
                      f" {deleted_note['text']}", "info")

    def search_notes(self, *args):
        if len(args) < 1:
            raise NotEnoughArgumentsError(
                "search-notes command requires a keyword.")

        if len(args) > 1:
            write_message(
                "Warning: extra arguments detected."
                " They were joined into one search query.",
                "warning",
            )

        keyword = " ".join(args).strip()

        if not keyword:
            raise InvalidCommandError("Search keyword cannot be empty.")

        found_notes = self.__search_notes(keyword)

        if not found_notes:
            write_message("No matching notes found.", "info")
            return

        for note in found_notes:
            self.__print_note(note)

    def add_tag(self, *args):
        if len(args) < 2:
            raise NotEnoughArgumentsError(
                "add-tag command requires note id and at least one tag."
            )

        note_id = self.__parse_note_id(args[0])
        tags = [tag.strip().lower() for tag in args[1:] if tag.strip()]

        if not tags:
            raise InvalidCommandError("At least one valid tag is required.")

        note = self.__add_tag(note_id, tags)

        if note is None:
            raise NoteNotFoundError(f"Note with id {note_id} not found.")

        self.__save()
        write_message(f"Tags added to note [{note_id}].", "info")
        self.__print_note(note)

    def remove_tag(self, *args):
        if len(args) < 2:
            raise NotEnoughArgumentsError(
                "remove-tag command requires note id and tag."
            )

        if len(args) > 2:
            write_message(
                "Warning: extra arguments detected."
                " Only the first tag was used.",
                "warning",
            )

        note_id = self.__parse_note_id(args[0])
        tag = args[1].strip().lower()

        if not tag:
            raise InvalidCommandError("Tag cannot be empty.")

        result = self.__remove_tag(note_id, tag)

        if result is None:
            raise NoteNotFoundError(f"Note with id {note_id} not found.")

        self.__save()
        write_message(f"Tag '{tag}' removed from note [{note_id}].", "info")
        self.__print_note(result)

    def search_by_tag(self, *args):
        if len(args) < 1:
            raise NotEnoughArgumentsError(
                "search-by-tag command requires at least one tag.")

        tags = [tag.strip().lower() for tag in args if tag.strip()]

        if not tags:
            raise InvalidCommandError("At least one valid tag is required.")

        found_notes = self.__search_by_tags(tags)

        if not found_notes:
            write_message("No notes found for given tag(s).", "info")
            return

        for note in found_notes:
            self.__print_note(note)

    def sort_notes_by_tags(self, *args):
        if len(args) > 0:
            write_message(
                "Warning: sort-notes-by-tags does not need arguments."
                " Extra arguments were ignored.",
                "warning",
            )

        notes = self.__sort_notes_by_tags()

        if not notes:
            write_message("No notes found.", "info")
            return

        for note in notes:
            self.__print_note(note)

    def edit_note(self, *args):
        if len(args) < 2:
            raise NotEnoughArgumentsError
        if len(args) > 2:
            write_message(
                "Warning: extra arguments detected."
                " They were joined into one new note text.",
                "warning",
            )

        note_id = self.__parse_note_id(args[0])
        new_text = " ".join(args[1:]).strip()

        if not new_text:
            raise ValueError("New note text cannot be empty.")

        note = self.__find_note_by_id(note_id)

        if note is None:
            raise NoteNotFoundError

        note["text"] = new_text
        self.__save()
        write_message(f"Note with id {note_id} updated.", "info")
        self.__print_note(note)

    def __save(self):
        write_to_file(
            {
                "notes": self.notes,
                "next_id": self.next_id,
            },
            "notes",
        )

    def __parse_note_id(self, raw_id):
        try:
            return int(raw_id)
        except (TypeError, ValueError):
            raise InvalidCommandError("Note id must be an integer.")

    def __add_note(self, text: str):
        note = {
            "id": self.next_id,
            "text": text,
            "tags": [],
        }
        self.notes.append(note)
        self.next_id += 1
        return note

    def __get_notes(self):
        return self.notes

    def __delete_note(self, note_id: int):
        for index, note in enumerate(self.notes):
            if note["id"] == note_id:
                return self.notes.pop(index)
        return None

    def __search_notes(self, keyword: str):
        keyword = keyword.lower()
        return [
            note for note in self.notes
            if keyword in note["text"].lower()
        ]

    def __add_tag(self, note_id: int, tags: list[str]):
        note = self.__find_note_by_id(note_id)
        if note is None:
            return None

        for tag in tags:
            if tag not in note["tags"]:
                note["tags"].append(tag)

        note["tags"].sort()
        return note

    def __remove_tag(self, note_id: int, tag: str):
        note = self.__find_note_by_id(note_id)
        if note is None:
            return None

        if tag in note["tags"]:
            note["tags"].remove(tag)

        return note

    def __search_by_tags(self, tags: list[str]):
        return [
            note for note in self.notes
            if all(tag in note["tags"] for tag in tags)
        ]

    def __sort_notes_by_tags(self):
        return sorted(
            self.notes,
            key=lambda note: (", ".join(note["tags"]), note["id"])
        )

    def __find_note_by_id(self, note_id: int):
        for note in self.notes:
            if note["id"] == note_id:
                return note
        return None

    def __print_note(self, note: dict):
        tags = ", ".join(note["tags"]) if note["tags"] else "no tags"
        write_message(f"[{note['id']}] {note['text']} | tags: {tags}", "info")

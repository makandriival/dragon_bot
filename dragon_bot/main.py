import os
import sys


if __package__ in (None, ""):
    # Support running this file directly: `python dragon_bot/main.py`.
    sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))


from colorama import init
from dragon_bot.interface import Interface
from dragon_bot.contacts import Contacts
from dragon_bot.notes import Notes


# Initialize colorama for colored output in the old terminal
init(autoreset=True)


def main():
    contacts = Contacts()
    notes = Notes()

    # Create a dictionary of commands and their corresponding functions
    commands = {
        "add-contact": contacts.add_contact,
        "add-phone": contacts.add_phone,
        "set-address": contacts.set_address,
        "set-email": contacts.set_email,
        "set-birthday": contacts.set_birthday,
        "all-contacts": contacts.all_contacts,
        "find-contact": contacts.find_contact,
        "birthdays": contacts.birthdays,
        "edit-name": contacts.edit_name,
        "del-phone": contacts.del_phone,
        "del-email": contacts.del_email,
        "del-birthday": contacts.del_birthday,
        "del-contact": contacts.del_contact,
        "del-address": contacts.del_address,
        "add-note": notes.add_note,
        "all-notes": notes.get_notes,
        "del-note": notes.delete_note,
        "find-notes-by-tag": notes.search_by_tag,
        "add-tag": notes.add_tag,
        "edit-note": notes.edit_note,
        "find-notes-by-keyword": notes.search_notes,
        "sort-notes": notes.sort_notes_by_tags,
        "del-tag": notes.remove_tag,
    }

    # Create an instance of the Interface class with the commands
    interface = Interface(commands)
    interface.command_loop()


if __name__ == "__main__":
    main()

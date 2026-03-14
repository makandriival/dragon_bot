from interface import Interface
from contacts import (
    add_contact, add_phone, set_address, set_email, set_birthday,
    all_contacts, find_contact, birthdays, edit_name, del_phone,
    del_email, del_birthday, del_contact, del_address,
)
from notes import Notes


def main():

    notes = Notes()

    # Create a dictionary of commands and their corresponding functions
    commands = {
        "add-contact": add_contact,
        "add-phone": add_phone,
        "set-address": set_address,
        "set-email": set_email,
        "set-birthday": set_birthday,
        "all-contacts": all_contacts,
        "find-contact": find_contact,
        "birthdays": birthdays,
        "edit-name": edit_name,
        "del-phone": del_phone,
        "del-email": del_email,
        "del-birthday": del_birthday,
        "del-contact": del_contact,
        "del-address": del_address,
        "add-note": notes.add_note,
        "all-notes": notes.get_notes,
        "del-note": notes.delete_note,
        "find-notes": notes.search_by_tag,
        "add-tag": notes.add_tag,
    }

    # Create an instance of the Interface class with the commands
    interface = Interface(commands)
    interface.command_loop()


if __name__ == "__main__":
    main()

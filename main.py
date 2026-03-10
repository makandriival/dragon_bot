from lib.contacts.contacts import Contacts
from lib.notes.notes import Notes
from lib.interface.interface import Interface

def main():
    # Create an instance of the Notes class
    notes = Notes()

    # Create an instance of the Contacts class
    contacts = Contacts()

    # Create a dictionary of commands and their corresponding functions
    commands = {
        "add_note": notes.add_note,
        "get_notes": notes.get_notes,
        "add_contact": contacts.add_contact,
        "remove_contact": contacts.remove_contact,
        "get_contact": contacts.get_contact,
        # Add more commands as needed
    }

    # Create an instance of the Interface class with the commands
    interface = Interface(commands)
    interface.command_loop()


if __name__ == "__main__":
    main()
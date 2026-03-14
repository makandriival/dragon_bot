from interface import Interface
from contacts import *


def main():

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
    }

    # Create an instance of the Interface class with the commands
    interface = Interface(commands)
    interface.command_loop()


if __name__ == "__main__":
    main()
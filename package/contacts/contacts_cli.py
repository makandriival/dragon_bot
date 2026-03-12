from writer import write_message
from contacts.contact_storage import ContactStorage
from contacts.contacts_service import ContactsService
from contacts.contact import Contact

class Contacts:
    """Commands for managing contacts."""

    def __init__(self):
        storage = ContactStorage()
        self.service = ContactsService(storage)

    def _print_contacts(self, contacts):
        if not contacts:
            write_message("No contacts found.", "info")
            return
        for c in contacts:
            write_message(Contact(**c).format(), "info")

    # --- commands ---
    def add_contact(self, *args):
        if len(args) < 2:
            write_message("Usage: add_contact <name> <phone> [address] [email] [birthday]", "error")
            return
        name, phone, *rest = args
        address = rest[0] if len(rest) > 0 else ""
        email = rest[1] if len(rest) > 1 else ""
        birthday = rest[2] if len(rest) > 2 else ""
        contact = self.service.add_contact(name, phone, address, email, birthday)
        write_message(f"Contact added: {Contact(**contact).format()}", "info")

    def get_contact(self, name: str):
        contacts = self.service.get_contact(name)
        self._print_contacts(contacts)

    def edit_contact(self, name: str, field: str, value: str):
        updated = self.service.edit_contact(name, field, value)
        if updated:
            write_message(f"Updated contact: {Contact(**updated).format()}", "info")
        else:
            write_message(f"No contact found with name {name}", "info")

    def remove_contact(self, name: str):
        removed = self.service.remove_contact(name)
        if removed:
            write_message(f"Removed contact {name}", "info")
        else:
            write_message(f"No contact found with name {name}", "info")

    def search_contacts(self, query: str):
        results = self.service.search_contacts(query)
        self._print_contacts(results)

    def list_contacts(self):
        contacts = self.service.list_contacts()
        self._print_contacts(contacts)

    def upcoming_birthdays(self):
        data = self.service.upcoming_birthdays()
        if not data:
            write_message("No upcoming birthdays.", "info")
            return
        for item in data:
            write_message(f"{item['name']} -> {item['congratulation_date']}", "info")

    def birthdays_in(self, days: int):
        results = self.service.birthdays_in(days)
        self._print_contacts(results)
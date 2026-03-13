from collections import UserDict
from datetime import datetime, timedelta
from writer import write_message
from data_source.actions import read_from_file, write_to_file
from interface.constants import INFO, ERROR

DATE_FORMAT = "%d.%m.%Y"


# FIELDS
class FieldValueError(Exception):
    pass


class Field:
    def __init__(self, value):
        self.value = value

    def _validate(self, value):
        if not value:
            raise FieldValueError("Field cannot be empty")

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._validate(value)
        self._value = value


class Name(Field):
    pass


class Phone(Field):
    def _validate(self, value):
        if not value.isdigit() or len(value) != 10:
            raise FieldValueError("Phone must contain 10 digits")


class Email(Field):
    def _validate(self, value):
        if "@" not in value:
            raise FieldValueError("Invalid email")


class Birthday(Field):
    def _validate(self, value):
        try:
            datetime.strptime(value, DATE_FORMAT)
        except ValueError:
            raise FieldValueError(f"Birthday must be in {DATE_FORMAT} format")

    def get_date(self):
        return datetime.strptime(self.value, DATE_FORMAT).date()


# RECORD
class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.email = None
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                return
        raise FieldValueError("Phone not found")

    def set_email(self, email):
        self.email = Email(email)

    def del_email(self):
        self.email = None

    def set_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def del_birthday(self):
        self.birthday = None

    def __str__(self):
        phones = ", ".join(p.value for p in self.phones) if self.phones else "-"
        email = self.email.value if self.email else "-"
        birthday = self.birthday.value if self.birthday else "-"
        return f"{self.name.value} | phones: {phones} | email: {email} | birthday: {birthday}"

    def to_dict(self):
        return {
            "name": self.name.value,
            "phones": [p.value for p in self.phones],
            "email": self.email.value if self.email else None,
            "birthday": self.birthday.value if self.birthday else None,
        }

    @staticmethod
    def from_dict(data):
        record = Record(data["name"])
        for phone in data.get("phones", []):
            record.add_phone(phone)
        if data.get("email"):
            record.set_email(data["email"])
        if data.get("birthday"):
            record.set_birthday(data["birthday"])
        return record


# ADDRESS BOOK
class Contacts(UserDict):
    def __init__(self):
        super().__init__()
        records = read_from_file("contacts")
        for record_data in records:
            if isinstance(record_data, dict):
                record = Record.from_dict(record_data)
            else:
                record = record_data
            self.data[record.name.value] = record

    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def upcoming_birthdays(self, days):
        today = datetime.today().date()
        end_date = today + timedelta(days=int(days))
        result = []

        for record in self.data.values():
            if not record.birthday:
                continue
            birthday = record.birthday.get_date()
            birthday_this_year = birthday.replace(year=today.year)
            if birthday_this_year < today:
                birthday_this_year = birthday_this_year.replace(year=today.year + 1)

            if today <= birthday_this_year <= end_date:
                congrat_day = birthday_this_year
                if congrat_day.weekday() == 5:
                    congrat_day += timedelta(days=2)
                elif congrat_day.weekday() == 6:
                    congrat_day += timedelta(days=1)
                result.append(f"{record.name.value}: {congrat_day.strftime(DATE_FORMAT)}")
        return result

    def save_data(self):
        data_to_save = [r.to_dict() for r in self.data.values()]
        write_to_file(data_to_save, "contacts")


# GLOBAL INSTANCE
contacts = Contacts()


# COMMANDS
def add_contact(*args):
    if len(args) < 2:
        write_message("Usage: add-contact <name> <phone>", ERROR)
        return
    name, phone = args[0], args[1]
    record = contacts.find(name)
    if not record:
        record = Record(name)
        contacts.add_record(record)
    record.add_phone(phone)
    contacts.save_data()
    write_message("Contact added", INFO)


def add_phone(*args):
    if len(args) < 2:
        write_message("Usage: add-phone <name> <phone>", ERROR)
        return
    name, phone = args[0], args[1]
    record = contacts.find(name)
    if not record:
        write_message("Contact not found", ERROR)
        return
    record.add_phone(phone)
    contacts.save_data()
    write_message("Phone added", INFO)


def set_email(*args):
    if len(args) < 2:
        write_message("Usage: set-email <name> <email>", ERROR)
        return
    name, email = args[0], args[1]
    record = contacts.find(name)
    if not record:
        write_message("Contact not found", ERROR)
        return
    record.set_email(email)
    contacts.save_data()
    write_message("Email set", INFO)


def set_birthday(*args):
    if len(args) < 2:
        write_message("Usage: set-birthday <name> <DD.MM.YYYY>", ERROR)
        return
    name, birthday = args[0], args[1]
    record = contacts.find(name)
    if not record:
        write_message("Contact not found", ERROR)
        return
    record.set_birthday(birthday)
    contacts.save_data()
    write_message("Birthday set", INFO)


def all_contacts(*args):
    if not contacts.data:
        write_message("Address book is empty", INFO)
        return
    for record in contacts.data.values():
        write_message(record, INFO)


def find_contact(*args):
    if len(args) < 1:
        write_message("Usage: find-contact <name>", ERROR)
        return
    name = args[0]
    record = contacts.find(name)
    if not record:
        write_message("Contact not found", ERROR)
        return
    write_message(record, INFO)


def birthdays(*args):
    if len(args) < 1:
        write_message("Usage: birthdays <days>", ERROR)
        return
    try:
        days = int(args[0])
    except ValueError:
        write_message("Days must be an integer", ERROR)
        return
    result = contacts.upcoming_birthdays(days)
    if not result:
        write_message("No upcoming birthdays", INFO)
        return
    for line in result:
        write_message(line, INFO)


def edit_name(*args):
    if len(args) < 2:
        write_message("Usage: edit-name <old_name> <new_name>", ERROR)
        return
    old_name, new_name = args[0], args[1]
    record = contacts.find(old_name)
    if not record:
        write_message("Contact not found", ERROR)
        return
    contacts.delete(old_name)
    record.name.value = new_name
    contacts.add_record(record)
    contacts.save_data()
    write_message("Name updated", INFO)


def del_phone(*args):
    if len(args) < 2:
        write_message("Usage: del-phone <name> <phone>", ERROR)
        return
    name, phone = args[0], args[1]
    record = contacts.find(name)
    if not record:
        write_message("Contact not found", ERROR)
        return
    record.remove_phone(phone)
    contacts.save_data()
    write_message("Phone deleted", INFO)


def del_email(*args):
    if len(args) < 1:
        write_message("Usage: del-email <name>", ERROR)
        return
    name = args[0]
    record = contacts.find(name)
    if not record:
        write_message("Contact not found", ERROR)
        return
    record.del_email()
    contacts.save_data()
    write_message("Email deleted", INFO)


def del_birthday(*args):
    if len(args) < 1:
        write_message("Usage: del-birthday <name>", ERROR)
        return
    name = args[0]
    record = contacts.find(name)
    if not record:
        write_message("Contact not found", ERROR)
        return
    record.del_birthday()
    contacts.save_data()
    write_message("Birthday deleted", INFO)


def del_contact(*args):
    if len(args) < 1:
        write_message("Usage: del-contact <name>", ERROR)
        return
    name = args[0]
    if not contacts.find(name):
        write_message("Contact not found", ERROR)
        return
    contacts.delete(name)
    contacts.save_data()
    write_message("Contact deleted", INFO)
from collections import UserDict
from datetime import datetime, timedelta
from writer import write_message
from data_source.actions import read_from_file, write_to_file
from interface.constants import INFO, ERROR
from bot_exceptions import (
    ContactNotFoundError,
    DuplicateContactError,
    InvalidPhoneNumberError,
    InvalidEmailError,
    InvalidDateError
)

DATE_FORMAT = "%d.%m.%Y"

# FIELDS
class Field:
    def __init__(self, value):
        self.value = value

    def _validate(self, value):
        if not value:
            raise ValueError("Field cannot be empty")

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
            raise InvalidPhoneNumberError()


class Email(Field):
    def _validate(self, value):
        if "@" not in value:
            raise InvalidEmailError()


class Birthday(Field):
    def _validate(self, value):
        try:
            datetime.strptime(value, DATE_FORMAT)
        except ValueError:
            raise InvalidDateError()

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
        raise ContactNotFoundError("Phone not found")

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


# CONTACTS
class Contacts(UserDict):
    def __init__(self):
        super().__init__()
        records = read_from_file("contacts")
        for rec in records:
            if isinstance(rec, dict):
                record = Record.from_dict(rec)
            else:
                record = rec
            self.data[record.name.value] = record

    def add_record(self, record):
        if record.name.value in self.data:
            raise DuplicateContactError()
        self.data[record.name.value] = record
        self.save_data()

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name not in self.data:
            raise ContactNotFoundError()
        del self.data[name]
        self.save_data()

    def save_data(self):
        data_to_save = [r.to_dict() for r in self.data.values()]
        write_to_file(data_to_save, "contacts")

    def upcoming_birthdays(self, days):
        today = datetime.today().date()
        end_date = today + timedelta(days=days)
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


# GLOBAL INSTANCE
contacts = Contacts()


# COMMANDS
def add_contact(name, phone):
    record = contacts.find(name)
    if record:
        raise DuplicateContactError()
    record = Record(name)
    record.add_phone(phone)
    contacts.add_record(record)
    write_message("Contact added", INFO)


def add_phone(name, phone):
    record = contacts.find(name)
    if not record:
        raise ContactNotFoundError()
    record.add_phone(phone)
    contacts.save_data()
    write_message("Phone added", INFO)


def set_email(name, email):
    record = contacts.find(name)
    if not record:
        raise ContactNotFoundError()
    record.set_email(email)
    contacts.save_data()
    write_message("Email set", INFO)


def set_birthday(name, birthday):
    record = contacts.find(name)
    if not record:
        raise ContactNotFoundError()
    record.set_birthday(birthday)
    contacts.save_data()
    write_message("Birthday set", INFO)


def all_contacts():
    if not contacts.data:
        write_message("Address book is empty", INFO)
        return
    for rec in contacts.data.values():
        write_message(rec, INFO)


def find_contact(name):
    record = contacts.find(name)
    if not record:
        raise ContactNotFoundError()
    write_message(record, INFO)


def birthdays(days):
    result = contacts.upcoming_birthdays(int(days))
    if not result:
        write_message("No upcoming birthdays", INFO)
        return
    for line in result:
        write_message(line, INFO)


def edit_name(old_name, new_name):
    record = contacts.find(old_name)
    if not record:
        raise ContactNotFoundError()
    contacts.delete(old_name)
    record.name.value = new_name
    contacts.add_record(record)
    write_message("Name updated", INFO)


def del_phone(name, phone):
    record = contacts.find(name)
    if not record:
        raise ContactNotFoundError()
    record.remove_phone(phone)
    contacts.save_data()
    write_message("Phone deleted", INFO)


def del_email(name):
    record = contacts.find(name)
    if not record:
        raise ContactNotFoundError()
    record.del_email()
    contacts.save_data()
    write_message("Email deleted", INFO)


def del_birthday(name):
    record = contacts.find(name)
    if not record:
        raise ContactNotFoundError()
    record.del_birthday()
    contacts.save_data()
    write_message("Birthday deleted", INFO)


def del_contact(name):
    contacts.delete(name)
    write_message("Contact deleted", INFO)
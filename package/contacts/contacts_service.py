from typing import Any, Dict, List, Optional
from datetime import date, datetime, timedelta

from contacts.contact_storage import ContactStorage
from contacts.validators import validate_email, validate_phone, validate_birthday
from contacts.contact import Contact
from bot_exceptions import DuplicateContactError

DATE_FORMAT = "%d.%m.%Y"

class ContactsService:

    def __init__(self, storage: ContactStorage):
        self.storage = storage

    # --- CRUD ---
    def add_contact(
        self, name: str, phone: str, address: str = "", email: str = "", birthday: str = ""
    ) -> Dict[str, Any]:
        validate_phone(phone)
        validate_email(email)
        birthday = validate_birthday(birthday)

        if self.storage.find_by_name(name):
            raise DuplicateContactError(f"Contact already exists: {name}")

        contact = self.storage.add({
            "name": name,
            "phone": phone,
            "address": address,
            "email": email,
            "birthday": birthday,
        })
        self.storage.save()
        return contact

    def edit_contact(
        self, name: str, field: str, value: str
    ) -> Optional[Dict[str, Any]]:
        allowed_fields = {"name", "phone", "email", "birthday", "address"}
        field = field.lower()
        if field not in allowed_fields:
            raise ValueError(f"Editable fields: {', '.join(allowed_fields)}")

        contact = self.storage.get_by_name(name)
        if not contact:
            return None

        if field == "phone":
            validate_phone(value)
        elif field == "email":
            validate_email(value)
        elif field == "birthday":
            value = validate_birthday(value)
        elif field == "name" and self.storage.find_by_name(value):
            raise DuplicateContactError(f"Contact already exists with name: {value}")

        updated = self.storage.update_by_name(name, {field: value})
        if updated:
            self.storage.save()
        return updated

    def remove_contact(self, name: str) -> Optional[Dict[str, Any]]:
        removed = self.storage.remove_by_name(name)
        if removed:
            self.storage.save()
        return removed

    # --- Find/Lists ---
    def get_contact(self, name: str) -> List[Dict[str, Any]]:
        return [c for c in self.storage.get_all() if name.lower() in c.get("name", "").lower()]

    def search_contacts(self, query: str) -> List[Dict[str, Any]]:
        return self.storage.search(query)

    def list_contacts(self) -> List[Dict[str, Any]]:
        return self.storage.get_all()

    # --- Upcoming Birthdays ---
    def upcoming_birthdays(self) -> List[Dict[str, str]]:
        """Возвращает контакты с днями рождения в ближайшие 7 дней."""
        today = date.today()
        upcoming: List[Dict[str, str]] = []

        for contact in self.storage.get_all():
            bday = contact.get("birthday")
            if not bday:
                continue
            try:
                bd = datetime.strptime(bday, DATE_FORMAT).date()
                bd_this_year = bd.replace(year=today.year)
                if bd_this_year < today:
                    bd_this_year = bd_this_year.replace(year=today.year + 1)
                delta = (bd_this_year - today).days
                if 0 <= delta <= 7:
                    if bd_this_year.weekday() == 5:
                        bd_this_year += timedelta(days=2)
                    elif bd_this_year.weekday() == 6:
                        bd_this_year += timedelta(days=1)
                    upcoming.append({
                        "name": contact.get("name", ""),
                        "congratulation_date": bd_this_year.strftime(DATE_FORMAT)
                    })
            except ValueError:
                continue

        return upcoming

    def birthdays_in(self, days: int) -> List[Dict[str, Any]]:
        today = date.today()
        target_date = today + timedelta(days=days)
        results: List[Dict[str, Any]] = []

        for contact in self.storage.get_all():
            bday = contact.get("birthday")
            if not bday:
                continue
            try:
                bd = datetime.strptime(bday, DATE_FORMAT).date()
                try:
                    bd_this_year = date(today.year, bd.month, bd.day)
                except ValueError:
                    continue
                if bd_this_year < today:
                    try:
                        bd_this_year = date(today.year + 1, bd.month, bd.day)
                    except ValueError:
                        continue
                if bd_this_year == target_date:
                    results.append(contact)
            except ValueError:
                continue

        return results
from __future__ import annotations

import pickle
import re
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

from lib.bot_exceptions import (
    DuplicateContactError,
    InvalidDateError,
    InvalidEmailError,
    InvalidPhoneNumberError,
)


class Contacts:
    """Simple contact book persisted to disk using pickle."""

    def __init__(self, storage_path: str | Path = "contacts.pkl"):
        # Where contacts are stored on disk.
        self._storage_path = Path(storage_path)

        # Store contacts as a list of dicts. Each contact has a unique 'id'.
        self._contacts: List[Dict[str, Any]] = []
        self._next_id = 1

        self._load()

    # --- Validators ---
    @staticmethod
    def _validate_email(email: str) -> None:
        # Simple email validation; not RFC perfect but good enough for basic use.
        if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
            raise InvalidEmailError(f"Invalid email: {email}")

    @staticmethod
    def _validate_phone(phone: str) -> None:
        # Accept digits, spaces, dashes, parentheses, plus sign.
        cleaned = re.sub(r"[^0-9]", "", phone)
        if len(cleaned) < 7 or len(cleaned) > 15:
            raise InvalidPhoneNumberError(f"Invalid phone number: {phone}")

    @staticmethod
    def _validate_birthday(birthday: str) -> date:
        # Accept either ISO (YYYY-MM-DD) or common local format (DD.MM.YYYY).
        for fmt in ("%Y-%m-%d", "%d.%m.%Y"):
            try:
                return datetime.strptime(birthday, fmt).date()
            except ValueError:
                continue
        raise InvalidDateError(
            "Birthday must be in format YYYY-MM-DD or DD.MM.YYYY (e.g. 1990-12-31)."
        )

    # --- Internal helpers ---
    def _find_by_id(self, contact_id: int) -> Optional[Dict[str, Any]]:
        for contact in self._contacts:
            if contact["id"] == contact_id:
                return contact
        return None

    def _find_by_name(self, name: str) -> List[Dict[str, Any]]:
        return [c for c in self._contacts if c["name"].lower() == name.lower()]

    def _search(self, query: str) -> List[Dict[str, Any]]:
        q = query.lower()
        return [
            c
            for c in self._contacts
            if q in c["name"].lower()
               or q in c["address"].lower()
               or q in c["email"].lower()
               or q in c["phone"].lower()
        ]

    def _load(self) -> None:
        """Load contacts from disk. If the storage file is missing, start empty."""
        if not self._storage_path.exists():
            return

        try:
            with self._storage_path.open("rb") as f:
                data = pickle.load(f)

            if isinstance(data, dict):
                self._contacts = data.get("contacts", []) or []
                self._next_id = data.get("next_id", 1) or 1
            elif isinstance(data, list):
                self._contacts = data
                self._next_id = max((c.get("id", 0) for c in self._contacts), default=0) + 1
            else:
                # Unknown format; start fresh
                self._contacts = []
                self._next_id = 1

            # Ensure next_id is always ahead of existing ids.
            self._next_id = max(self._next_id, max((c.get("id", 0) for c in self._contacts), default=0) + 1)
        except Exception as e:
            print(f"Warning: could not load contacts: {e}")
            self._contacts = []
            self._next_id = 1

    def _save(self) -> None:
        """Persist contacts to disk."""
        try:
            self._storage_path.parent.mkdir(parents=True, exist_ok=True)
            with self._storage_path.open("wb") as f:
                pickle.dump({"contacts": self._contacts, "next_id": self._next_id}, f)
        except Exception as e:
            print(f"Error saving contacts: {e}")

    def _format_contact(self, contact: Dict[str, Any]) -> str:
        return (
            f"[{contact['id']}] {contact['name']} | {contact['address']} | "
            f"{contact['phone']} | {contact['email']} | {contact['birthday']}"
        )

    def _print_contacts(self, contacts: List[Dict[str, Any]]) -> None:
        if not contacts:
            print("No contacts found.")
            return
        for c in contacts:
            print(self._format_contact(c))

    # --- Public command methods ---
    def add_contact(
        self,
        name: str,
        address: str,
        phone: str,
        email: str,
        birthday: str,
    ) -> None:
        """add_contact <name> <address> <phone> <email> <birthday:YYYY-MM-DD>"""
        # Reload from disk before mutating to avoid overwriting concurrent changes.
        self._load()

        self._validate_phone(phone)
        self._validate_email(email)
        birthday_date = self._validate_birthday(birthday)

        # Prevent duplicate contacts by name (case-insensitive).
        if any(c["name"].lower() == name.lower() for c in self._contacts):
            raise DuplicateContactError(f"Contact already exists: {name}")

        contact = {
            "id": self._next_id,
            "name": name,
            "address": address,
            "phone": phone,
            "email": email,
            "birthday": birthday_date.isoformat(),
        }
        self._contacts.append(contact)
        self._next_id += 1

        self._save()
        print(f"Contact added: {self._format_contact(contact)}")

    def get_contact(self, name_or_id: str) -> None:
        """get_contact <name_or_id>"""
        self._load()

        results: List[Dict[str, Any]] = []
        if name_or_id.isdigit():
            contact = self._find_by_id(int(name_or_id))
            if contact:
                results = [contact]
        else:
            results = [
                c for c in self._contacts if name_or_id.lower() in c["name"].lower()
            ]

        self._print_contacts(results)

    def remove_contact(self, contact_id: str) -> None:
        """remove_contact <id>"""
        self._load()

        if not contact_id.isdigit():
            raise ValueError("Contact id must be a number.")

        contact_id_int = int(contact_id)
        contact = self._find_by_id(contact_id_int)
        if not contact:
            print(f"No contact found with id {contact_id_int}.")
            return

        self._contacts = [c for c in self._contacts if c["id"] != contact_id_int]
        self._save()
        print(f"Removed contact {contact_id_int}: {contact['name']}")

    def edit_contact(self, contact_id: str, field: str, *new_value_parts: str) -> None:
        """edit_contact <id> <field> <new_value>"""
        self._load()

        if not contact_id.isdigit():
            raise ValueError("Contact id must be a number.")

        if not new_value_parts:
            raise ValueError("Usage: edit_contact <id> <field> <new_value>")

        contact_id_int = int(contact_id)
        field = field.lower()
        new_value = " ".join(new_value_parts)

        contact = self._find_by_id(contact_id_int)
        if not contact:
            print(f"No contact found with id {contact_id_int}.")
            return

        if field not in {"name", "address", "phone", "email", "birthday"}:
            raise ValueError(
                "Editable fields: name, address, phone, email, birthday"
            )

        if field == "phone":
            self._validate_phone(new_value)
        elif field == "email":
            self._validate_email(new_value)
        elif field == "birthday":
            birthday_date = self._validate_birthday(new_value)
            new_value = birthday_date.isoformat()
        elif field == "name":
            # Prevent changing name to an existing contact's name.
            if any(
                c["id"] != contact_id_int and c["name"].lower() == new_value.lower()
                for c in self._contacts
            ):
                raise DuplicateContactError(
                    f"Contact already exists with name: {new_value}"
                )

        contact[field] = new_value
        self._save()
        print(f"Updated contact: {self._format_contact(contact)}")

    def search_contacts(self, query: str) -> None:
        """search_contacts <query>"""
        self._load()

        results = self._search(query)
        self._print_contacts(results)

    def list_contacts(self) -> None:
        """list_contacts"""
        self._load()
        self._print_contacts(self._contacts)

    def _get_upcoming_birthdays(self) -> List[Dict[str, str]]:
        """Return upcoming birthdays (next 7 days), shifting weekend dates to Monday."""
        today = date.today()
        upcoming: List[Dict[str, str]] = []

        for contact in self._contacts:
            birthday = contact.get("birthday")
            if not birthday:
                continue

            try:
                bday = datetime.strptime(birthday, "%Y-%m-%d").date()
            except ValueError:
                continue

            # Compare the birthday date for this year (or next if already passed).
            try:
                bday_this_year = bday.replace(year=today.year)
            except ValueError:
                # Skip invalid dates for the current year (e.g. Feb 29 on a non-leap year).
                continue

            if bday_this_year < today:
                try:
                    bday_this_year = bday_this_year.replace(year=today.year + 1)
                except ValueError:
                    continue

            delta = (bday_this_year - today).days
            if 0 <= delta <= 7:
                congrat_date = bday_this_year
                if congrat_date.weekday() == 5:
                    congrat_date += timedelta(days=2)
                elif congrat_date.weekday() == 6:
                    congrat_date += timedelta(days=1)

                upcoming.append(
                    {
                        "name": contact.get("name", ""),
                        "congratulation_date": congrat_date.strftime("%d.%m.%Y"),
                    }
                )

        return upcoming

    def upcoming_birthdays(self) -> None:
        """upcoming_birthdays

        Prints upcoming birthdays in the next 7 days (weekend birthdays shift to Monday).
        """
        self._load()

        data = self._get_upcoming_birthdays()
        if not data:
            print("No upcoming birthdays.")
            return

        for item in data:
            print(f"{item['name']} -> {item['congratulation_date']}")

    def birthdays_in(self, days: str) -> None:
        """birthdays_in <days>"""
        self._load()

        try:
            days_int = int(days)
        except ValueError:
            raise ValueError("Days must be an integer.")

        if days_int < 0:
            raise ValueError("Days must be non-negative.")

        today = date.today()
        target_date = today + timedelta(days=days_int)

        results: List[Dict[str, Any]] = []
        for contact in self._contacts:
            birthday = contact.get("birthday")
            if not birthday:
                continue

            try:
                bday = datetime.strptime(birthday, "%Y-%m-%d").date()
            except ValueError:
                continue

            bday_this_year = date(today.year, bday.month, bday.day)
            if bday_this_year < today:
                bday_this_year = date(today.year + 1, bday.month, bday.day)

            if bday_this_year == target_date:
                results.append(contact)

        self._print_contacts(results)
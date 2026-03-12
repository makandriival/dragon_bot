from typing import Any, Dict, List, Optional
from package.data_source.actions import read_from_file, write_to_file

class ContactStorage:
    """Хранение и управление контактами."""

    def __init__(self, data_type: str = "contacts"):
        self._data_type = data_type
        self._data = self._load()

    def _load(self) -> Dict[str, Any]:
        raw = read_from_file(self._data_type)
        if isinstance(raw, dict):
            contacts = raw.get("contacts", [])
        elif isinstance(raw, list):
            contacts = raw
        else:
            contacts = []
        return {"contacts": contacts}

    def save(self) -> None:
        write_to_file(self._data["contacts"], self._data_type)

    def get_all(self) -> List[Dict[str, Any]]:
        return list(self._data["contacts"])

    def get_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        lower = name.lower()
        return next((c for c in self._data["contacts"] if c.get("name", "").lower() == lower), None)

    def find_by_name(self, name: str) -> List[Dict[str, Any]]:
        lower = name.lower()
        return [c for c in self._data["contacts"] if c.get("name", "").lower() == lower]

    def search(self, query: str) -> List[Dict[str, Any]]:
        q = query.lower()
        return [c for c in self._data["contacts"] if q in c.get("name","").lower()
                or q in c.get("address","").lower()
                or q in c.get("phone","").lower()
                or q in c.get("email","").lower()]

    def add(self, contact: Dict[str, Any]) -> Dict[str, Any]:
        self._data["contacts"].append(contact)
        return contact

    def update_by_name(self, name: str, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        contact = self.get_by_name(name)
        if not contact:
            return None
        contact.update(updates)
        return contact

    def remove_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        contact = self.get_by_name(name)
        if not contact:
            return None
        self._data["contacts"] = [c for c in self._data["contacts"] if c.get("name","").lower() != name.lower()]
        return contact
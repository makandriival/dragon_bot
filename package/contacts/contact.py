from dataclasses import dataclass
from typing import Optional

@dataclass
class Contact:
    id: Optional[int] = None
    name: str = ""
    address: str = ""
    phone: str = ""
    email: str = ""
    birthday: str = ""

    def format(self) -> str:
        return f"{self.name} | {self.address} | {self.phone} | {self.email} | {self.birthday}"
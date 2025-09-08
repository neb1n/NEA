from dataclasses import dataclass
from typing import Optional

#!Dataclass for the user model
@dataclass
class User:
    id: Optional[int] = None
    username: str = ""
    password_hash: str = ""
    role: str = "admin"
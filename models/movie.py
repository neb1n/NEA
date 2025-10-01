from dataclasses import dataclass
from typing import List, Optional

#!Dataclasses made for the movie model
@dataclass
class Movie:
    id: Optional[int] = None
    title: str = ""
    genre: str = ""
    description: str = ""
    duration: int = 0  #!Changed from hours to minutes
    showtimes: List[str] = None
    screen: int = 1
    
    def __post_init__(self):
        if self.showtimes is None:
            self.showtimes = []
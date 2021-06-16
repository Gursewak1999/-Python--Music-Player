from dataclasses import dataclass
from typing import List


@dataclass
class Ar:
    name: str
    cover: str
    url: str


@dataclass
class BasicSongsData:
    error: bool
    ar: List[Ar]

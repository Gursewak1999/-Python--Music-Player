from dataclasses import dataclass
from typing import Optional, List, Dict


@dataclass
class Detail:
    singers: Optional[str] = None
    lyricist: Optional[str] = None
    composer: Optional[str] = None


@dataclass
class SongDetailsData:
    name: str
    cover: str
    details: List[Detail]
    download_links: List[Dict[str, str]]

from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import List, Optional

from PIL import Image

class IMG:
    def __init__(self):
        ...
    
    def make(self, id: str, data: List[str]) -> bytes:
        # TODO: return bytes from made image
        ...
    
    def get_cache(self, id: str) -> Optional[bytes]:
        # TODO: return bytes for id from Cache
        ...
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import List, Optional

from PIL import Image
from io import BytesIO

class IMG:
    def __init__(self):
        ...

    def make(self, id: str, data: List[str]) -> bytes:
        # TODO: return bytes from made image
        base_canvas = Image.new(mode = "RGB", size = (20, 20))

        bytes_io = BytesIO()

        base_canvas.save(bytes_io, format = "webp")

        bytes_io.seek(0)

        return bytes_io.read()

    def get_cache(self, id: str) -> Optional[bytes]:
        # TODO: return bytes for id from Cache
        ...
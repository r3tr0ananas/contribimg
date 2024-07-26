from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import List

from . import __version__
from .constants import GH_API_KEY

import httpx

__all__ = ("HTTPClient",)

class HTTPClient:
    def __init__(self):
        self.client = httpx.AsyncClient(
            headers = {
                "User-Agent": f"ContribIMG ({__version__})",
                "Authorization": f"BEARER {GH_API_KEY}"
            }
        )

    async def contributor_images(
        self,
        owner: str,
        repo: str
    ) -> List[str]:
        images = []

        api_request = await self.client.get(f"https://api.github.com/repos/{owner}/{repo}/contributors")

        json_data = api_request.json()

        if "status" in json_data:
            return int(json_data["status"])

        for user in json_data:
            if user["type"] == "User":
                images.append(
                    user["avatar_url"]
                )

        return images
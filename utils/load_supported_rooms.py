import httpx
from typing import Optional
from .github_links import GitHubLinks

def load_supported_rooms() -> Optional[dict]:
    """
    Try installing new supported rooms
    """
    
    resp = httpx.get(GitHubLinks.SUPPORTED_ROOMS)
    if resp.status_code == 200:
        supported_rooms = resp.json()
    else:
        supported_rooms = {}

    return supported_rooms
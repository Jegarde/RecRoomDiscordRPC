import json
import httpx
from typing import Optional
from .github_links import GitHubLinks

def load_supported_rooms() -> Optional[dict]:
    try:
        with open("supported_rooms.json", "r") as supported_rooms_json:
            supported_rooms = json.load(supported_rooms_json)
    except FileNotFoundError:
        resp = httpx.get(GitHubLinks.SUPPORTED_ROOMS)
        if resp.status_code == 200:
            with open("supported_rooms.json", "w") as cfg_json:
                json.dump(resp.json(), cfg_json, indent=4)
                
            supported_rooms = resp.json()
        else:
            return None
        
    return supported_rooms
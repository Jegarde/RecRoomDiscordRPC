import json
import httpx
from typing import Optional
from .github_links import GitHubLinks

def load_platforms() -> Optional[dict]:
    try:
        with open("platforms.json", "r") as platforms_json:
            platforms = json.load(platforms_json)
    except FileNotFoundError:
        resp = httpx.get(GitHubLinks.PLATFORMS)
        if resp.status_code == 200:
            with open("platforms.json", "w") as cfg_json:
                json.dump(resp.json(), cfg_json, indent=4)
                
            platforms = resp.json()
        else:
            return None
        
    return platforms
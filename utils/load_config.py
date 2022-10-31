import json
import httpx
from typing import Optional
from .github_links import GitHubLinks

def load_config() -> Optional[dict]:
    try:
        with open("config.json", "r") as cfg_json:
            config = json.load(cfg_json)
    except FileNotFoundError:
        resp = httpx.get(GitHubLinks.CONFIG)
        if resp.status_code == 200:
            with open("config.json", "w") as cfg_json:
                json.dump(resp.json(), cfg_json, indent=4)
                
            config = resp.json()
        else:
            return None
        
    return config
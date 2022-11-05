import httpx
from typing import Optional
from .github_links import GitHubLinks

def load_platforms() -> Optional[dict]:
    resp = httpx.get(GitHubLinks.PLATFORMS)
    if resp.status_code == 200:
        platforms = resp.json()
    else:
        platforms = None
        
    return platforms
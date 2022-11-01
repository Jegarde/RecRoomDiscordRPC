import httpx
import os.path
from .github_links import GitHubLinks

def download_env() -> bool:
    if os.path.isfile(".env"):
        return True
    else:
        resp = httpx.get(GitHubLinks.ENV)
        if resp.status_code == 200:
            with open(".env", "w") as env_file:
                env_file.write(resp.text)
            return True
        else:
            return False
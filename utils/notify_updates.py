import httpx
import json
from .github_links import GitHubLinks
      
def notify_latest_update() -> str:
    """
    Fetch the latest updates and notify the user
    """
    
    with open("version.json", "r") as version_json:
        versions = json.load(version_json)
        
    version = list(versions)[-1]
    
    resp = httpx.get(GitHubLinks.VERSION)
    if resp.status_code == 200:
        latest_versions_json = resp.json()
        if version not in latest_versions_json:
            latest_version = list(latest_version)[-1]
            print(f"A new update is available! {version} > {latest_version}")
            print(f"Download at {GitHubLinks.REPO}")
            
            features = latest_version[latest_version]
            feature_list = '\n'.join(features)
            print(f"Feature list: {feature_list}\n")
    else:
        print("Couldn't fetch possible updates.\n")
        
    return version
import httpx
from .github_links import GitHubLinks

def notify_latest_update(version: str) -> str:
    """
    Fetch the latest updates and notify the user
    """
    
    resp = httpx.get(GitHubLinks.VERSION)
    if resp.status_code == 200:
        latest_versions_json = resp.json()
        if version not in latest_versions_json:
            latest_version = list(latest_versions_json)[-1]
            print(f"A new update is available! {version} > {latest_version}")
            print(f"Download at {GitHubLinks.REPO}\n")
            
            features = latest_versions_json.get(latest_version, {})
            
            # Generate feature notes
            if features:
                print(features["title"])
                feature_list = list(map(lambda feature: f"-{feature}", features["feature_list"]))
                feature_list = '\n'.join(feature_list)
                print(feature_list)
                print("\n")
    else:
        print("Couldn't fetch possible updates.\n")
        
    return version
import asyncio
from utils import notify_latest_update, load_config, download_env, prompt_continue
from dotenv import dotenv_values
from client import RecRoomRPC

        
VERSION = "0.0.4"
        
async def main():
    version = notify_latest_update(VERSION)
    
    print(f"Rec Room Discord RPC v{version} made by @Jegarde")
    
    # Load the config
    config = load_config()
    
    # Make sure it loaded
    if not config:
        prompt_continue("Configuration not found and I was unable to install a fresh one! Please reinstall.", "close")
        return
    
    if download_env():
        # Load Rec Room account credentials
        credentials = dotenv_values(".env")
        username = credentials.get("USERNAME")
        password = credentials.get("PASSWORD")
        alt_username = credentials.get("ALT_USERNAME", None)
    else:
        prompt_continue("Couldn't download the .env file from GitHub, please reinstall.", "close")
        return
    
    # Make sure they're filled
    if not any([username, password]):
        prompt_continue("Fill your Rec Room account credentials in a .env file in the same directory.", "close")
        return
    
    RPC = RecRoomRPC(
        username=username,
        password=password,
        client_id=894603419531243590,
        debug=config.get("debug", False),
        delay=config.get("update_delay", 15),
        track_username=alt_username
    )
    await RPC.start()

if __name__ == "__main__":
    asyncio.run(main())
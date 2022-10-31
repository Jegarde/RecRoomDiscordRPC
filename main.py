import asyncio
from utils import notify_latest_update, load_config
from dotenv import dotenv_values
from client import RecRoomRPC
        
async def main():
    version = notify_latest_update()
    
    print(f"Rec Room Discord RPC v{version} made by @Jegarde")
    
    # Load the config
    config = load_config()
    
    # Make sure it loaded
    if not config:
        print("Configuration not found and I was unable to install a fresh one! Please reinstall.")
        return
    
    # Load Rec Room account credentials
    credentials = dotenv_values(".env")
    username = credentials.get("USERNAME")
    password = credentials.get("PASSWORD")
    
    # Make sure they're filled
    if not any([username, password]):
        print("Fill your Rec Room account credentials in a .env file in the same directory.")
        return
    
    RPC = RecRoomRPC(
        username=username,
        password=password,
        client_id=894603419531243590,
        debug=config.get("debug", False),
        delay=config.get("update_delay", 15),
        track_username=config.get("alt_username", None)
    )
    await RPC.start()

if __name__ == "__main__":
    asyncio.run(main())
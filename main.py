import asyncio
import json
from dotenv import dotenv_values
from client import RecRoomRPC
        
async def main():
    with open("config.json", "r") as cfg_json:
        config = json.load(cfg_json)
    
    credentials = dotenv_values(".env")
    
    RPC = RecRoomRPC(
        username=credentials.get("USERNAME"),
        password=credentials.get("PASSWORD"),
        client_id=894603419531243590,
        debug=config["debug"],
        delay=config["update_delay"],
        track_username=config["alt_username"]
    )
    await RPC.start()

if __name__ == "__main__":
    asyncio.run(main())
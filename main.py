import recnetpy
import asyncio
import json
import nest_asyncio
import time
from enum import Enum
from data_classes import MatchmakingResponse, APIEndpoints
from recnetpy.dataclasses.account import Account
from recnetpy.rest import Response
from recnetlogin import RecNetLoginAsync
from pypresence import Presence
from typing import Optional, Tuple
from utils import img_url, room_url, profile_url

nest_asyncio.apply()

class PresenceReturnValue(Enum):
    OK = 1      # All good
    OFFLINE = 2 # If user is offline
    SAME = 3    # If the instance is the same

class RecRoomRPC:
    def __init__(self, username: str, password: str, client_id: int):
        self.username = username
        self.password = password
        self.client_id = client_id
        
        self.RPC = Presence(self.client_id)
        self.rec_net: recnetpy.Client = None
        self.rec_login: RecNetLoginAsync  = None
        self.account: Account = None
            
        with open("platforms.json", "r") as platforms_json:
            self.platforms = json.load(platforms_json)
        
        self.old_matchmaking: Optional[MatchmakingResponse] = {}
        self.delay = 15
        self.debug = True
        
    async def start(self):
        """
        Initialize all modules and start the integration
        """
        
        # Initialize RecNetPy and check if specified account exists
        self.rec_net = recnetpy.Client()
        self.account = await self.rec_net.accounts.get(self.username)
        assert self.account, "Account not found!"
        
        self.debug_print("Found account...")
        
        # Initialize RecNetLogin for authorized calls
        self.rec_login = RecNetLoginAsync(
            username=self.username,
            password=self.password
        )
        
        self.debug_print("Initialized RecNetLogin...")
        
        # Connect to Discord
        self.RPC.connect()
        
        self.debug_print("Connected to RPC...")
        
        while True:
            self.debug_print("Updating RPC...")
            await self.update()
            await asyncio.sleep(self.delay)
            
        
    async def get_presence(self) -> Tuple[PresenceReturnValue, Optional[dict]]:
        """
        Returns the params for updating the RPC
        Returns nothing if the player is offline or nothing has changed
        """
        data: Response[MatchmakingResponse] = await self.rec_net.rec_net.custom(APIEndpoints.matchmaking).player.make_request(
            "post", 
            body={
                "id": self.account.id
            }, 
            headers={
                "Authorization": await self.rec_login.get_token(include_bearer=True)
            }
        )
        matchmaking: MatchmakingResponse = data.data[0]
        instance = matchmaking["roomInstance"] if matchmaking["roomInstance"] else {}
        
        # Check if the player is online
        if not matchmaking["isOnline"]:
            return (PresenceReturnValue.OFFLINE, None)

        # If they haven't changed instances, no updating is needed
        if self.old_matchmaking and self.old_matchmaking.get("roomInstance", {}).get("roomInstanceId") == instance.get("roomInstanceId"):
            return (PresenceReturnValue.SAME, None)
        
        # For comparsion on the next update to see if updating is needed
        self.old_matchmaking = matchmaking if matchmaking else {}
                
        # RecNet link buttons on the RPC
        buttons = [{"label": "View Profile", "url": profile_url(self.account.username)}]
            
        # Show where the user is and the instance status
        room_name = instance.get("name")
        if room_name:
            if not room_name.startswith("^"):
                # Dorm room
                state = room_name
                room_image = img_url("70rpp90levsypggpzn6c4xqqs.jpg")
                
            else:
                room_name = room_name.replace("^", "")
                room = await self.rec_net.rooms.get(room_name)
                
                if room:
                    # A public room
                    state = f"^{room.name}"
                    room_image = img_url(room.image_name)
                    
                    if instance["isPrivate"]:
                        state += " • PRIVATE"
                        
                    # Add RecNet room button link
                    buttons.append(
                        {"label": "View Room", "url": room_url(room_name)}
                    )
                        
                else:
                    # A Private room
                    state = "Private Room"
                    room_image = img_url("DefaultRoomImage.jpg")
                
            if instance["isFull"]:
                state += " • FULL"

            
        else:
            state = "Login Menu"
            room_image = img_url("DefaultRoomImage.jpg")
        
        # Get platform
        if matchmaking["deviceClass"] > len(self.platforms) - 1:  # If it's some new platform
            platform = self.platforms[0]
        else:
            platform = self.platforms[matchmaking["deviceClass"]]
        
        return (
            PresenceReturnValue.OK,
            {
                # Indicate whether or not the game has started or not
                "details": "Playing a game in progress" if instance.get("isInProgress", False) else "Hanging out",
                
                # Display in which room the user is
                "state": f"in {state}",

                # Set the room thumbnail
                "large_image": room_image,
                
                # When the instance was changed
                "start": int(time.time()),
                
                # Add RecNet link buttons
                "buttons": buttons,
                
                # Add platform
                "small_image": platform["image"],
                "small_text": f"Playing on {platform['name']}"
            }
        )
        
        
    async def update(self) -> bool:
        """
        Updates the RPC based on if the RR account is online or not.
        Returns true if online and successful, false if cleared
        """
        
        status, presence = await self.get_presence()
        match status:
            case PresenceReturnValue.OK:
                self.RPC.update(**presence)
                return True
            
            case PresenceReturnValue.SAME:
                return True
            
            case PresenceReturnValue.OFFLINE:
                self.RPC.clear()
                return False
            

    def debug_print(self, *args):
        if self.debug:
            print(*args)
            
        
async def main():
    RPC = RecRoomRPC(
        username="RealNetBot",
        password="D7roCoFh7psCH6G",
        client_id=894603419531243590
    )
    await RPC.start()

if __name__ == "__main__":
    asyncio.run(main())
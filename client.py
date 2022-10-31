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
from recnetlogin.exceptions import InvalidAccountCredentials, Lockout
from pypresence import Presence
from pypresence.exceptions import DiscordNotFound
from typing import Optional, Tuple
from utils import img_url, room_url, profile_url, load_platforms, load_supported_rooms

nest_asyncio.apply()

class PresenceReturnValue(Enum):
    OK = 1      # All good
    OFFLINE = 2 # If user is offline
    SAME = 3    # If the instance is the same

class RecRoomRPC:
    def __init__(self, username: str, password: str, client_id: int, debug: bool = False, delay: int = 15, track_username: str = None):
        self.username = username
        self.password = password
        self.client_id = client_id
        
        # Who to track for the RPC
        self.track_username = track_username if track_username else self.username
        
        self.RPC: Presence = None
        self.rec_net: recnetpy.Client = None
        self.rec_login: RecNetLoginAsync  = None
        self.account: Account = None
            
        self.platforms = {}
        self.supported_rooms = {}
        
        self.old_matchmaking: Optional[MatchmakingResponse] = {}
        self.delay = delay
        self.debug = debug
        
    async def start(self):
        """
        Initialize all modules and start the integration
        """
        
        # Connect to Discord
        try:
            self.RPC = Presence(self.client_id)
        except DiscordNotFound:
            print("Please have Discord running in the background!")
            return
        self.RPC.connect()
        
        # Load platforms and supported rooms
        self.platforms = load_platforms()
        if not self.platforms:
            print("Couldn't find platforms file and was unable to reinstall! Please reinstall.")
            return
        
        self.supported_rooms = load_supported_rooms()
        if not self.supported_rooms:
            print("Couldn't find platforms file and was unable to reinstall! Please reinstall.")
            return
        
        # Initialize RecNetPy and check if specified account exists
        self.rec_net = recnetpy.Client()
        self.account = await self.rec_net.accounts.get(self.track_username)
        if not self.account:
            print(f"Account named @{self.track_username} doesn't exist!")
            await self.stop()
            return
        
        self.debug_print("Found account...")
        
        # Initialize RecNetLogin for authorized calls
        self.rec_login = RecNetLoginAsync(
            username=self.username,
            password=self.password,
            prompt_2fa=True
        )
        try:
            await self.rec_login.get_token()
        except InvalidAccountCredentials:
            print("Couldn't login, check your Rec Room account credentials in the configuration file!")
            await self.stop()
            return
        except Lockout:
            print("Couldn't login, Rec Room login attempts are being rate limited!")
            await self.stop()
            return
        
        self.debug_print("Initialized RecNetLogin...")
        
        print("Successfully connected to Rec Room and Discord!")
        
        while True:
            self.debug_print("Updating RPC...")
            await self.update()
            await asyncio.sleep(self.delay)
            
    async def stop(self) -> None:
        """
        Closes the instance
        """
        
        if self.rec_net: await self.rec_net.close()
        if self.rec_login: await self.rec_login.close()
        
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
        old_instance = self.old_matchmaking.get("roomInstance", {})
        if old_instance is None:
            old_instance = {}
            
        if self.old_matchmaking and old_instance.get("roomInstanceId") == instance.get("roomInstanceId"):
            return (PresenceReturnValue.SAME, None)
        
        # For comparsion on the next update to see if updating is needed
        self.old_matchmaking = matchmaking
                
        # RecNet link buttons on the RPC
        buttons = [{"label": "View Profile", "url": profile_url(self.account.username)}]
            
        # Show where the user is and the instance status
        raw_room_name = instance.get("name")
        if raw_room_name:
            if not raw_room_name.startswith("^"):
                # Dorm room
                state = raw_room_name
                room_image = img_url("70rpp90levsypggpzn6c4xqqs.jpg")
                
            else:
                room_name = raw_room_name.replace("^", "")
                room = await self.rec_net.rooms.get(room_name, include=8)
                
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
        
        game_state = self.supported_rooms.get(raw_room_name, {
            "pre_game": "Hanging out",
            "in_progress": "Game in progress"
        })
        
        return (
            PresenceReturnValue.OK,
            {
                # Indicate whether or not the game has started or not
                "details": game_state["in_progress"] if instance.get("isInProgress", False) else game_state["pre_game"],
                "state": state,

                # Set the room thumbnail
                "large_image": room_image,
                "large_text": f"Room: {raw_room_name}",
                
                # Only display elapsed on ongoing games
                "start": int(time.time()) if instance.get("isInProgress", False) else None,
                
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
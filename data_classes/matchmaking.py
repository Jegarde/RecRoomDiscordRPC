from typing import Optional, TypedDict
from .room_instance import RoomInstance

class MatchmakingResponse(TypedDict):
    playerId: int
    statusVisibility: int
    deviceClass: int
    vrMovementMode: int
    roomInstance: Optional[RoomInstance]
    lastOnline: str
    isOnline: bool
    appVersion: str
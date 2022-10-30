from typing import TypedDict

class RoomInstance(TypedDict):
    roomInstanceId: int
    roomId: int
    subRoomId: int
    location: str
    roomInstanceType: int
    photonRegionId: str
    photonRoomId: str
    name: str
    maxCapacity: int
    isFull: bool
    isPrivate: bool
    isInProgress: bool
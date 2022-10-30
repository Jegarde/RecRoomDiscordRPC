# So I don't need to write the url's in every use-case.
# Also, it's easier to change if needed

def img_url(image_name: str, crop_square: bool=False, resolution: int=720) -> str:
    """
    https://img.rec.net/{image_name}?width={resolution}&{'cropSquare=true&' if crop_square else ''}
    """
    return f"https://img.rec.net/{image_name}?width={resolution}&{'cropSquare=true&' if crop_square else ''}"

def profile_url(username: str) -> str: 
    """
    https://rec.net/user/{username}
    """
    return f"https://rec.net/user/{username}"

def room_url(room_name: str) -> str:
    """
    https://rec.net/room/{room_name}
    """
    return f"https://rec.net/room/{room_name}"

def event_url(event_id: int) -> str:
    """
    https://rec.net/event/{event_id}
    """
    return f"https://rec.net/event/{event_id}"
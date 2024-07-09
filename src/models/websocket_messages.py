
class ActionBase:
    name: str
    payload: dict

    def __init__(self):
        pass

    def as_dict(self):
        self_dict = dict()
        self_dict["name"] = self.name
        self_dict["payload"] = self.payload


class WebsocketMessageBase:
    """
    Base class for a websocket server message
    """
    room_id: str
    user_id: str

    action: ActionBase


    def __init__(self):
        pass


    def as_dict(self) -> dict[str, str]:
        self_dict = dict()
        self_dict["action"] = self.action.as_dict()
        return self_dict
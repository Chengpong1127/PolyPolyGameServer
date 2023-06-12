from dataclasses import dataclass, asdict, field
from enum import Enum
import json
from uuid import UUID

class MessageType(Enum):
    RequestRoom = "RequestRoom"
    CancelRequest = "CancelRequest"
    PlayerAction = "PlayerAction"
    PlayerLeave = "PlayerLeave"
    CreateRoom = "CreateRoom"
    TestMessage = "TestMessage"
    JoinMessage = "JoinMessage"
    GameOver = "GameOver"

class TeamID(Enum):
    Blue = "Blue"
    Red = "Red"
    

@dataclass(frozen=True)
class Message:
    DeviceID: str = field(default="")
    MessageType: str = field(default=MessageType.TestMessage.value)
    Content: str = field(default="",repr=False)
    
    
    @property
    def json(self):
        return json.dumps(asdict(self))
    
    
@dataclass(frozen=True)
class HostInfo:
    IP: str
    Port: int

@dataclass(frozen=True)
class RoomInfo:
    RoomID: str
    PlayerInfoMap: dict
    RoomHostInfo: HostInfo
    
    @property
    def json(self):
        return json.dumps(asdict(self))
    
@dataclass(frozen=True)
class CharacterInfo:
    TeamID: str
    CharacterModelID: str
    
    @property
    def json(self):
        return json.dumps(asdict(self))
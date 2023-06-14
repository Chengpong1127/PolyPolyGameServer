# import logger
import logging
from Server.Message import Message, MessageType, HostInfo, RoomInfo, CharacterInfo, TeamID
from Server.SessionManager import SessionManager
from uuid import UUID
import uuid
from Server.BaseMessageHandler import BaseMessageHandler
from Basic.Event import Event

class RoomManager(BaseMessageHandler):
    def __init__(self,roomID: UUID , deviceIDHostMap: dict, hostInfo: HostInfo) -> None:
        self.RoomID = roomID
        self.sessionManager = SessionManager(hostInfo)
        super().__init__(self.sessionManager, deviceIDHostMap)
        self.RoomInfo = self.GetRoomInfo()
        self.OnCloseRoom = Event()
        
        
    def GetRoomInfo(self):
        info = RoomInfo(
            RoomID=str(self.RoomID),
            PlayerInfoMap=self.GetPlayerInfoDict(),
            RoomHostInfo=self.sessionManager.HostInfo
        )
        return info
    def GetPlayerInfoDict(self):
        info = {}
        for i, deviceID in enumerate(self.GetDeviceList()):
            info[deviceID] = CharacterInfo(TeamID=TeamID.Blue.value if i%2 == 0 else TeamID.Red.value, CharacterModelID=str(uuid.uuid4()))
        return info
    def HandleMessage(self, message: Message):
        if message.MessageType == MessageType.PlayerAction.value:
            self._player_action(message.Content)
        elif message.MessageType == MessageType.JoinMessage.value:
            logging.info("receive join message")
        elif message.MessageType == MessageType.PlayerLeave.value:
            self._player_leave(message.DeviceID, message.Content)
        elif message.MessageType == MessageType.GameOver.value:
            self._gameOver(message.Content)
        else:
            logging.warn("receive unknown message")
        
        
    def _gameOver(self, content):
        logging.info("game over")
        self._send_message_to_all_devices(Message(MessageType=MessageType.GameOver.value, Content=content))
        self.OnCloseRoom.Invoke(self.RoomID)
    def _player_action(self, content:str):
        logging.info("receive player action")
        self._send_message_to_all_devices(Message(MessageType=MessageType.PlayerAction.value, Content=content))
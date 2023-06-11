from Server.SessionManager import SessionManager
from Server.Message import Message, HostInfo, MessageType
import threading
from Server.RoomManager import RoomManager
import uuid
import logging
from Server.BaseMessageHandler import BaseMessageHandler

class ServerManager(BaseMessageHandler):

    def __init__(self, config):
        self.host = config["host"]
        self.playerCount = config["playerCount"]
        self.server_peer = SessionManager(self.host)
        super().__init__(self.server_peer)

        self.waiting_list = []
        self.room_list = dict()
        
        self.room_port_set = set()
        self.room_port_set.add(self.host.Port)
        ServerManager._instance = self
    @staticmethod
    def Instance():
        if ServerManager._instance == None:
            ServerManager._instance = ServerManager()
        return ServerManager._instance
    
    def _player_request_room(self, deviceID:str, content:str):
        assert deviceID in self.GetDeviceList()
        logging.info("player request room")
        self.waiting_list.append(deviceID)
        if len(self.waiting_list) >= self.playerCount:
            self._create_room()
    
    def _player_cancel_request(self, deviceID:str, content:str):
        if deviceID in self.waiting_list:
            self.waiting_list.remove(deviceID)
            logging.info("player cancel request")
    
    def _create_room(self):
        new_room_thread = threading.Thread(target=self._create_new_room_run, args=(self.waiting_list,))
        new_room_thread.start()
        self.waiting_list = []
                
    def Send_device_message(self, message: Message, playerID:str):
        player_message = Message(DeviceID=playerID, MessageType=message.MessageType, Content=message.Content)
        self.server_peer.sendData(player_message.json, self._get_device_host(playerID))
        
    def HandleMessage(self, message: Message):
        if message.MessageType == MessageType.RequestRoom.value:
            self._player_request_room(message.DeviceID, message.Content)
        elif message.MessageType == MessageType.CancelRequest.value:
            self._player_cancel_request(message.DeviceID, message.Content)
        else:
            logging.error("Unknown message type: ", message.MessageType)
        
    def _create_new_room_run(self, deviceList: list):
        
        device_host_map = dict()
        for deviceID in deviceList:
            device_host_map[deviceID] = self._get_device_host(deviceID)
            
        new_room_id = uuid.uuid4()
        new_room_host = self._create_new_room_host()
        
        room = RoomManager(new_room_id, device_host_map, new_room_host)
        self.room_list[new_room_id] = room
        room.run()
        self._send_create_room_message(room)
        logging.info("create new room successfully")
        
    def _create_new_room_host(self):
        while True:
            new_port = uuid.uuid4().int % 10000 + 8000
            if new_port not in self.room_port_set:
                self.room_port_set.add(new_port)
                return HostInfo(self.host.IP, new_port)
    def _send_create_room_message(self, room: RoomManager):
        message = Message(MessageType=MessageType.CreateRoom.value, Content = room.GetRoomInfo().json)
        self._send_message_to_all(message, room.GetDeviceList())

    def close(self):
        self.server_peer.close()
    
   


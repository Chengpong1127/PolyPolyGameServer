
from os import error
from Server.SessionManager import SessionManager
from Server.Message import Message, HostInfo

from Server.utils import String2Message
import logging


class BaseMessageHandler(object):
    def __init__(self, sessionManager: SessionManager, deviceIDHostMap: dict = {}):
        self.sessionManager = sessionManager
        self.sessionManager.OnReceiveMessage += self._handleInputData
        self.DeviceIDHostMap = deviceIDHostMap

    def run(self):
        self.sessionManager.run()

    def GetDeviceList(self):
        return list(self.DeviceIDHostMap.keys())
    
    def _handleInputData(self, message: str, host: HostInfo):
        try:
            data = String2Message(message)
            self.DeviceIDHostMap[data.DeviceID] = host
            self.HandleMessage(data)
        except error:
            logging.error("Error when handleMessage: ", error)
    
    def HandleMessage(self, message: Message):
        raise NotImplementedError
        
    def _send_message_to_all_devices(self, message: Message):
        self._send_message_to_all(message, self.GetDeviceList())
        
    def _send_message_to_all(self, message: Message, deviceList: list):
        for deviceID in deviceList:
            if deviceID in deviceList:
                self._send_message_to_device(deviceID, message)
        
    def _send_message_to_device(self, deviceID:str, message: Message):
        player_message = Message(DeviceID=deviceID, MessageType=message.MessageType, Content=message.Content)
        self.sessionManager.sendData(player_message.json, self._get_device_host(deviceID))
        
    def _get_device_host(self, deviceID:str):
        assert deviceID in self.DeviceIDHostMap
        return self.DeviceIDHostMap[deviceID]
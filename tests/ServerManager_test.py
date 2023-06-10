import pytest
from Server.ServerManager import ServerManager
from Server.Message import Message
import json
# 測試 ServerManager 類別
class TestServerManager:
    def test_str2Message(self):
        server = ServerManager()
        message = Message(DeviceID="player1", MessageType="RequestRoom", Content="room1")
        
        jsondata = message.json
        
        assert server._str2Message(jsondata) == message
    
    


# 執行測試
if __name__ == "__main__":
    pytest.main()

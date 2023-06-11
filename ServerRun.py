from Server.Message import HostInfo
from Server.ServerManager import ServerManager
import logging


logging.basicConfig(level=logging.INFO)
Server_config = {
    "host": HostInfo("169.254.148.197", 8000),
    "playerCount": 1,
}
server = ServerManager(Server_config)
server.run()
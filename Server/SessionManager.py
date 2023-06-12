import socket
import threading
from Server.Message import HostInfo
from Basic.Event import Event
from Server.utils import String2Data, Data2String
from Server.Database import PublicConnectionMap

class SessionManager:
    PACKET_COUNT_SIZE = 4
    PACKET_SIZE = 1024
    def __init__(self, host: HostInfo):
        self.TCPsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        self.TCPsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        self.TCPsock.bind((host.IP, host.Port))
        self.TCPsock.listen(10)
        self.HostInfo = host
        self.OnReceiveMessage = Event()
        self.OnPeerDisconnect = Event()
        
        
        self.connectionMap = PublicConnectionMap
        self.threadList = []
    def run(self):
        run_thread = threading.Thread(target=self._run)
        run_thread.start()
    def _run(self):
        while True:
            tcp_client, addr = self.TCPsock.accept()
            host = HostInfo(addr[0], addr[1])
            self.connectionMap[host] = tcp_client
            tcp_thread = threading.Thread(target=self._tcp_handle, args=(tcp_client,addr))
            tcp_thread.start()
            self.threadList.append(tcp_thread)
            
    def close(self):
        for thread in self.threadList:
            thread.stop()
        self.TCPsock.close()
            
    def _tcp_handle(self,client,addr):
        host = HostInfo(addr[0], addr[1])
        while True:
            try:
                
                data = self._receiveOnePacket(client)
                self._handleMessage(data, host)
            except ConnectionResetError:
                self.OnPeerDisconnect.Invoke(host)
                break
            
    def _receiveOnePacket(self, client: socket.socket):
        data = client.recv(SessionManager.PACKET_COUNT_SIZE)
        packet_count = int.from_bytes(data, byteorder='little')
        packet = b''
        for _ in range(packet_count):
            data = client.recv(SessionManager.PACKET_SIZE)
            packet += data
        packet = Data2String(packet)
        return packet
        
    def _handleMessage(self, message: str, host:HostInfo):
        self.OnReceiveMessage(message, host)
            
    def sendData(self, message:str, host: HostInfo, reliable=True):
        assert host in self.connectionMap
        if reliable:
            self.connectionMap[host].send(String2Data(message))
        else:
            self.UDPsock.sendto(String2Data(message), (host.IP, host.Port))
        
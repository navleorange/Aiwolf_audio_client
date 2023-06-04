import socket
from . import util

class Client:

    def __init__(self, config_path:str) -> None:
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

        inifile = util.check_config(config_path=config_path)
        inifile.read(config_path,"utf-8")
        self.host = inifile.get("connection","host")
        self.port = inifile.getint("connection","port")
        self.buffer = inifile.getint("connection","buffer")

    def connect(self) -> None:
        self.socket.connect((self.host,self.port))
    
    def receive(self) -> str:
        responses = b""

        while not util.is_json_complate(responces=responses):
            response = self.socket.recv(self.buffer)
            
            if response == b"":
                raise RuntimeError("socket connection broken")
            
            responses += response

        return responses.decode("utf-8")
    
    def receive_time_out(self) -> str:
        responses = b""

        while not util.is_json_complate(responces=responses):
            try:
                response = self.socket.recv(self.buffer)
            except:
                return None
            
            if response == b"":
                raise RuntimeError("socket connection broken")
            
            responses += response

        return responses.decode("utf-8")
    
    def set_time_out(self,time) -> None:
        self.socket.settimeout(time)
    
    def restore_time_out(self) -> None:
        self.socket.setblocking(True)
    
    def send(self, message:str) -> None:
        #message += "\n"
        self.socket.send(message.encode("utf-8"))

    def close(self) -> None:
        self.socket.close()
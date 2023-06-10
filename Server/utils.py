from Server.Message import Message
import json

def String2Message(string:str):
    return Message(**json.loads(string))

def Data2String(data):
    return data.decode("utf-8")

def String2Data(string):
    return string.encode("utf-8")
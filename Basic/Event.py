from typing import Callable


class Event(Callable):
    def __init__(self) -> None:
        self.subscribers = []
    
    def __iadd__(self, subscriber):
        if callable(subscriber) == False:
            raise Exception("subscriber must be a function")
        self.subscribers.append(subscriber)
        return self
    
    def __call__(self, *args, **kwargs):
        for subscriber in self.subscribers:
            subscriber(*args, **kwargs)
            
    def __isub__(self, subscriber):
        if callable(subscriber) == False:
            raise Exception("subscriber must be a function")
        self.subscribers.remove(subscriber)
        return self
    
    def __len__(self):
        return len(self.subscribers)
    
    def Invoke(self, *args, **kwargs):
        self.__call__(*args, **kwargs)
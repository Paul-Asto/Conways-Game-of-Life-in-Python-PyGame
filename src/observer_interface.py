from typing import Generic, TypeVar

T = TypeVar("T")



class Observer(Generic[T]):
    __observed: "Observed" = None

    @property
    def observed(self) -> T: 
        if self.__observed == None:
            raise Exception("No se tiene un observed implementado")
        
        return self.__observed

    @observed.setter
    def observed(self, observed: "Observed"):
        self.__observed = observed
        observed.observer = self


    def react_changes(self): ...

    def delete_observed(self):
        self.__observed.delete_observer()
        self.__observed = None



class Observed:
    __observer: "Observer"

    def __init__(self):
        self.__observer = None


    @property
    def observer(self) -> "Observer": 
        return self.__observer

    
    @observer.setter
    def observer(self, value: "Observer"):
        self.__observer = value

    def report_changes(self):
        if self.__observer == None:
            return

        self.observer.react_changes()

    def delete_observer(self):
        self.__observer = None

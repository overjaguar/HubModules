from PySide2.QtCore import QObject, QThread, Signal
from pathlib import Path
import time
from subprocess import Popen, PIPE
from abc import abstractmethod

class Worker(QObject): #класс с родителем qobject, сам будет потом родителем для воркеров(абстрактный)
    connected = Signal() #сигнал о подключении
    working = Signal() #сигнал состояния в работе
    finished = Signal() #для сигнализации окочания работы
    failed = Signal() #сигнал смерти модуля
    message = Signal(str) #для передачи значений
    path = Signal(str, str) #для передачи пути и названия модуля

    def __init__(self): #конструктор
        super().__init__() #наследует методы родительского класса
        self.pathToFile = None #по умолчанию пути нету
        self.isWorking = False #по умолчанию не работает типа
        self.userWannaStop = False #юзер по умолчанию не хочет останавливать

    @abstractmethod
    def stop(self):
        """"Остановка модуля"""
        
    @abstractmethod
    def run(self):
        """Старт модуля"""

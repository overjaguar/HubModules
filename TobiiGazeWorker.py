from PySide2.QtCore import QObject, QThread, Signal
from Worker import Worker
from pathlib import Path
import time, os
from subprocess import Popen, PIPE

class TobiiGazeWorker(Worker): #класс с родителем qobject
    def __init__(self, mode):#конструктор
        super().__init__()#родительский конструктор
        self.mode = mode

    def stop(self): #остановка модуля
        if not self.isWorking:
            self.finished.emit()
            return #если не работает, то выходим
        
        self.userWannaStop = True #пользователь хочет остановить

        if self.mode == '-t': #если была калибровка
            self.process.kill() #то убиваем
        else:
            self.process.communicate(b'\n') #иначе нормального завершаем работу
        self.finished.emit() #имитим завершение работы

    def run(self): #старт
        while not self.userWannaStop: #читаем поток вывода
            pathToTobii = Path.cwd() / 'modules' / 'TobiiGaze' / 'Samples' / 'tracker' #идем от директории проекта к модулю
            pathToTobii = pathToTobii.resolve() #для совместимости штука, преобразовывает в абсолютный
        
            self.process = Popen([pathToTobii, self.mode], stdin=PIPE, stdout=PIPE, stderr=PIPE) #создание сабпроцесса
            
            self.isWorking = True #теперь работает тру

            while True: #читаем поток вывода
                line = self.process.stdout.readline()#прочитать строку
                
                if not line: #читаем пока что-то есть, а если нету ничего то выходим из цикла
                    break
                else:
                    line = str(line.rstrip(), 'utf-8') #читаем строку в кодировке ютф8 и убираем ненужные пробелы

                if self.mode =="-a" and not self.userWannaStop: #если режим записи и пользователь не хочет останавливать
                    if line.startswith("Connected."): #если строка начинается с коннектед
                        self.connected.emit() #то посылаем сигнал о том, что подключен
                
                # if line.startswith("No eye tracker found.") and not self.userWannaStop: #если айтрекер не найден и пользователь не хочет останавливать
                #     self.finished.emit() #отсылает сигнал окончания работы

                if line.startswith("Results are saved in"): #если начинается с этого <-
                    self.pathToFile = line[len("Results are saved in file: "):] #получение названием файла
                    pathToLog = Path.cwd() / 'modules' / 'TobiiGaze' / 'Samples' / 'log' / self.pathToFile #добавление его к другому пути
                    pathToLog = pathToLog.resolve()
                    self.path.emit(str(pathToLog), 'tobii') #передача пути и названия модуля

                    if not self.userWannaStop: #если пользовать не хочет останавливать
                        self.working.emit() #имит состояния работы

                self.message.emit(line)#имитим полученную строку

            self.isWorking = False #флаг о том, что воркер не работает

            if self.mode == '-t': #если режим калибровки
                break #выходил из цикла

            if self.process.poll() and not self.userWannaStop: #исли завершился ошибкой
                self.failed.emit() #имит ошибки
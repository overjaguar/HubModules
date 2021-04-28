from PySide2.QtCore import QObject, QThread, Signal
from Worker import Worker
from pathlib import Path
import time
from subprocess import Popen, PIPE

class EmotivEEGWorker(Worker): #класс с родителем qobject
    def __init__(self, mode): # конструктор
        super().__init__() #конструктор родителя
        self.mode = mode

    def stop(self): #остановка модуля
        if not self.isWorking:
            self.finished.emit()
            return #если не работает, то выходим

        self.userWannaStop = True #флаг того, что пользователь хочет остановить

        if self.mode == '-t': #если была калибровка
            self.process.kill() #то убиваем
        else:
            self.process.communicate(b'\n') #иначе нормального завершаем работу
        self.finished.emit() #имитим завершение работы

    def run(self): #старт
        while not self.userWannaStop: #читаем поток вывода
            pathToModule = Path.cwd() / 'modules' / 'EmotivEEG' / 'EmotivEEG' #идем от директории проекта к модулю
            pathToModule = pathToModule.resolve() #для совместимости штука, преобразовывает в абсолютный
        
            self.process = Popen([pathToModule, self.mode], stdin=PIPE, stdout=PIPE, stderr=PIPE) #создание сабпроцесса
            
            self.isWorking = True #теперь работает тру

            #if self.mode == '-a': #в режиме работы с записью
            #    self.connected.emit() #подача сигнала
            while True: #читаем поток вывода
                line = self.process.stdout.readline() #прочитать строку
                
                if not line: #читаем пока что-то есть, а если нету ничего то выходим из цикла
                    break
                else:
                    line = str(line.rstrip(), 'utf-8') #читаем строку в кодировке ютф8 и убираем ненужные пробелы

                if line.startswith("Results of EEG"): #если начинается с этого
                    self.path.emit(line[len("Results of EEG are saved in: "):], 'eeg') #сохранение пути и передача названия
                    if not self.userWannaStop: #если пользовательне хочет останавливать
                        self.working.emit() #имит того, что модуль работает

                if line.startswith("Results of Facial"):
                    self.path.emit(line[len("Results of Facial are saved in: "):], 'facial') #сохранение пути для эмоций

                # if (line.startswith("EEG") or line.startswith("Facial")) and not self.userWannaStop:  #если пошли данные и пользователь не хочет останавливать
                #     self.working.emit() #имит того, что модуль работает
                
                self.message.emit(line)#имитим полученную строку

            self.isWorking = False #установка того, что модуль не работает

            if self.mode == '-t': #если в режиме калибровки
                break #выход из цикла

            if self.process.poll(): #если ошибка
                self.failed.emit() #подача сигнала ошибки
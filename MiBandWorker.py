from PySide2.QtCore import QObject, QThread, Signal
from Worker import Worker
from pathlib import Path
import time
from subprocess import Popen, PIPE

class MiBandWorker(Worker): #класс с родителем воркер(другой класс такой интересный)
    
    def __init__(self, mode):#уже надоело писать что это конструктор
        super().__init__()#наследование от родителя
        self.mode = mode

    def stop(self): #остановка модуля
        if not self.isWorking: #если модуль не работает
            self.finished.emit() #имит конца
            return #если не работает, то выходим
        
        self.userWannaStop = True #пользователь хочет остановить -- тру))

        if self.mode == '-t': #если была калибровка
            self.process.kill() #то убиваем
        else:
            self.process.communicate(b'\n') #иначе нормального завершаем работу
        self.finished.emit() #имитим завершение работы

    def run(self): #старт
        while not self.userWannaStop: #пока пользователь не захочет остановить
            pathToMiband = Path.cwd() / 'modules' / 'MiBand' / 'miband2.py' #идем от директории проекта к модулю
            pathToMiband = pathToMiband.resolve() #для совместимости шутка, преобразовывает в абсолютный
            
            self.process = Popen(['python3', pathToMiband, self.mode], stdin=PIPE, stdout=PIPE, stderr=PIPE) #создание сабпроцесса

            self.isWorking = True #флаг работы
            while True: #бесконечный цикл
                line = self.process.stdout.readline()#прочитать строку
                
                if not line: #читаем пока что-то есть, а если нету ничего то выходим из цикла
                    break
                else:
                    line = str(line.rstrip(), 'utf-8') #читаем строку в кодировке ютф8 и убираем ненужные пробелы вконце

                if line.startswith("Results are saved in"):#если встречаем строку, которая начинается с этого
                    self.path.emit(line[len("Results are saved in file: "):], 'miband') #то возвращаем путь и названием модуля

                    if not self.userWannaStop: #если пользователь не хочет останавливать (только если пришел путь)
                        self.working.emit() #то отсылаем сигналтого, что работает
                        
                if line == "Connected" and not self.userWannaStop and self.mode == '-a': #если встретил строку коннектед
                    self.connected.emit() #имит состояния подключен

                #if line == "Init OK": #если калибровка прошла успешно
                #    self.finished.emit() #отсылает сигнал окончания работы
                
                self.message.emit(line)#имитим полученную строку
            
            self.isWorking = False #не работает

            if self.mode == '-t': #если режим работы калибровки то брейкаем
                break

            if self.process.poll() and not self.userWannaStop: #если произошла ошибки
                self.failed.emit() #подача сигнала фейла
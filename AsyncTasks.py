from PySide2.QtCore import QObject, QThread, Signal
from MiBandWorker import MiBandWorker
from TobiiGazeWorker import TobiiGazeWorker
from EmotivEEGWorker import EmotivEEGWorker
import time
from MibandPlot import MibandPlot
from TobiiPlot import TobiiPlot
from EmotivPlot import EmotivPlot
from TextEdit import TextEdit
from subprocess import Popen, PIPE
import subprocess


class AsyncTasks(QObject): #класс в котором будет вестись асинхронная работа
    freeze = Signal() #объект для блокировки нажатия кнопки старт
    finished = Signal() #а этот объект нам нужен для блокировки кнопки стоп
    stopping = Signal() #сигнал остановки

    def __init__(self, parent):#конструктор
        super().__init__(parent) #наследование методов родителям
        self.threadDict = dict() #создание словаря потоков
        self.workers = dict() #создание слова воркеров
        self.plots = dict() #словарь графиков
        self.terminals = dict() #словарь терминалов режима калибровки
        self.path = dict() #словарь путей
        self.dbSavings = {'miband' : self.mibandDatabaseSaving, 'tobii' : self.tobiiDatabaseSaving, 'emotiv' : self.emotiveegDatabaseSaving} #словарь методов сохранения в бд
        self.plotsClasses = {'miband' : MibandPlot, 'tobii' : TobiiPlot, "emotiv" : EmotivPlot} #а тут словарь классов графиков)

    def runModules(self, modules, mode): #запуск модулей, сюда передается словарь с какими модулями выполнять и режим работы
        self.freeze.emit() #имитим блокирование кнопочки
        self.path.clear() #чистим словари
        self.workers.clear()
        self.plots.clear()
        self.terminals.clear()
        self.threadDict.clear()

        for module in modules: #для всех модулей
            if not modules[module]: #если модуль фалсе, то прощай 
                continue

            self.threadDict[module], self.workers[module] = self.initThread(module, mode) #добавляем в словари объекты потока и воркера

            if(mode == '-a'): #если режим работы с записью
                self.plots[module] = self.plotsClasses[module](name=module + " plot") #создание виджета с графиком для каждого свой
                self.workers[module].message.connect(self.plots[module].update_plot) #обновление графика при получении сообщения
                self.plots[module].show() #вывод графика
            else: #если калибровка
                self.terminals[module] = TextEdit(module) #создаем окно вывода стандартного потока вывода
                self.workers[module].message.connect(self.terminals[module].insertText)#вставить текст туда
                self.terminals[module].show()#вывод
            
        for thread in self.threadDict:   #запуск потоков
            self.threadDict[thread].start()

    def printProgress(self, string): #вывод строки на экран
        print(string)

    def tobiiDatabaseSaving(self):#запись в бд
        if 'tobii' not in self.path: #если нету такого в пути, то возвращаемся
            return

        subprocess.run('cat {0} | pv | \
           docker run -i --rm --link clickhouse-server:clickhouse-client yandex/clickhouse-client -m --host clickhouse-server \
           --query="INSERT INTO ModulesData.Tobii FORMAT CSV"'.format(self.path['tobii']), shell=True) #запись в бд

        self.path.pop('tobii') #удаление элемента, чтобы не происходила перезапись в ходе ошибки работы модуля

    def emotiveegDatabaseSaving(self):
        if 'eeg' not in self.path or 'facial' not in self.path: #если нету хотя бы одного из путей
            return

        subprocess.run('cat {0} | pv | \
           docker run -i --rm --link clickhouse-server:clickhouse-client yandex/clickhouse-client -m --host clickhouse-server \
           --query="INSERT INTO ModulesData.EmotivEEG FORMAT CSV"'.format(self.path['eeg']), shell=True) #запись в бд
        
        subprocess.run('cat {0} | pv | \
           docker run -i --rm --link clickhouse-server:clickhouse-client yandex/clickhouse-client -m --host clickhouse-server \
           --query="INSERT INTO ModulesData.EmotivFacial FORMAT CSV"'.format(self.path['facial']), shell=True) #запись в бд
        
        self.path.pop('facial') #удаление из словаря
        self.path.pop('eeg')

    def mibandDatabaseSaving(self):
        if 'miband' not in self.path: #если нету такого в словаре, то возврат
            return

        subprocess.run('cat {0} | pv | \
            docker run -i --rm --link clickhouse-server:clickhouse-client yandex/clickhouse-client -m --host clickhouse-server \
            --query="INSERT INTO ModulesData.Miband FORMAT CSV"'.format(self.path['miband']), shell=True) #запись в бд

        self.path.pop('miband')

    def stopAllTasks(self): #остановка всех модулей
        self.stopping.emit() #имитим остановку

        for worker in self.workers: #воркер принимает значение названия воркеров
            self.workers[worker].stop() #вызов метода остановки воркеров

        for plot in self.plots: #для всех графиков:
            self.plots[plot].close() #закрыть график

        for terminal in self.terminals: #для всех терминалов:
            self.terminals[terminal].close() #закрыть терминал

        self.finished.emit() #имитим конец 

    def getWorker(self, nameOfWorker): #получить воркер
        return self.workers[nameOfWorker] #возвращает воркер по его имени

    def savePath(self, path, nameOfModule):
        self.path[nameOfModule] = path #в словарь путей сохраняем полученный путь (для соответствующего модуля)

    def initThread(self, nameOfModule: str, mode: str):
        thread = QThread() #создание потока
        worker = TobiiGazeWorker(mode) if nameOfModule == 'tobii' else EmotivEEGWorker(mode) if nameOfModule == 'emotiv' else MiBandWorker(mode) #короч создаем соответствующий с названием
        worker.moveToThread(thread) #добавляем воркер в поток
        thread.started.connect(worker.run) #запуск воркера
        worker.finished.connect(thread.quit) #завершение работы потока
        worker.finished.connect(self.dbSavings[nameOfModule])#при окончании нужно выполнить сохранение в соответствии с именем модуля
        worker.failed.connect(self.dbSavings[nameOfModule])#при фейле работы модуля нужно выполнить сохранение в соответствии с именем модуля
        worker.finished.connect(worker.deleteLater) #удалем при окончании объект
        worker.path.connect(self.savePath)#сохраняем путь как только он у нас появляется(куда сохранять затем мол в бд)
        thread.finished.connect(thread.deleteLater) #удаляем поток
        return [thread, worker] #возращаем объект потока и воркера

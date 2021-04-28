#!/usr/bin/env python3
import sys

from PySide2.QtCore import QFile, QObject, Signal, Slot, QTimer
from PySide2.QtWidgets import QApplication, QVBoxLayout, QWidget
from PySide2.QtUiTools import QUiLoader

from pytz import utc
from datetime import datetime
from time import mktime

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from PlotWidget import PlotWidget

import random
#импорт 1001 либы)

class MibandPlot(PlotWidget):
    def __init__(self, parent=None, name="Plot"): #конструктор
        super().__init__(parent, name) #наследование (конструктор выполняется тут) 

        self.line, *_ = self.ax.plot([]) #*_ типа используется для игнорирования значение например какого-то, но тут толку не имеет, а сама линия и есть график

        self.ax.legend([self.line], ["HRM"]) #добавление легенды

        self.x = [] #ну это список
        self.y = []

    def update_plot(self, newValue): # для обновления графика, получает новое значение
        if not newValue.startswith('Time'): #если не начинается со слова тайм строка
            return #то ниче не делаем
        time = datetime.strptime(newValue[6:25], '%Y-%m-%d %H:%M:%S') #чтение строку и получение оттуда даты и времени
        heartbeat = int(newValue.split()[5]) #получение ЧСС
        time = mktime(utc.localize(time).utctimetuple()) #преобразование в utc формат времени
        if len(self.x) == 0: #если длинна икса равна 0(то есть если первое значение)
            self.startTime = time #тогда сохраняем начальное время
        
        time = time - self.startTime #от текущего времени отнимается начальное
        self.x.append(time) #добавление времени в конец х
        self.y.append(heartbeat) #добавление времени в конец у
        if len(self.y) >= 16 : #если длинна 16 или более по игрику
            self.x.pop(0) #то убираем первые значения
            self.y.pop(0)

        self.line.set_data(self.x, self.y) #тут уже устнавливаем в сам график

        self.ax.set_xlim(self.x[0], max(self.x)) #длинна по х от 0 до максимального значения
        self.ax.set_ylim(0, 180) #длинна по у от 0 до 180
        self.canvas.draw() #непосрдественное рисование

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

class TobiiPlot(PlotWidget):
    def __init__(self, parent=None, name="Plot"): #конструктор
        super().__init__(parent, name) #наследование

        self.line, *_ = self.ax.plot([], 'o-', markersize=15, markevery=[4]) #*_ типа используется для игнорирования значение например какого-то, но тут толку не имеет, а сама линия и есть график, где последнее значение это точка
        
        self.ax.legend([self.line], ["Sight"]) #легенда
        
        self.x = [0 for i in range(5)] #ну это список с пятью значениями нулями по умолчанию(необходим для оптимизиации в будующем)
        self.y = [0 for i in range(5)]

    def update_plot(self, newValue : str): #обновление графика
        status = newValue[0] #статус это первое значение в стандартном потоке вывода(показывает какие логи вывелись)

        if not status.isdecimal() or status == '0' or status == '4': #если не начинается с цифры, или первая цифра 0 или 4
            return #то ниче не делаем

        newValue = newValue.split() #сплитим строку
        if status == '1': #если статус единица
            x = (float(newValue[8][0:len(newValue[8])-1]) + float(newValue[4][0:len(newValue[4])-1])) / 2 #среднее арифмитическое координа по х левого и права глаза(там из строки вырезает значение и преобразовывается в флоат)
            y = (float(newValue[10][0:len(newValue[10])-1]) + float(newValue[6][0:len(newValue[6])-1])) / 2 #аналогично для у

            self.x.append(x) #добавление в конце х или у
            self.y.append(y)

        if status == '5' or status == '6': #right
            self.x.append(float(newValue[10][0:len(newValue[10])-1])) #строим по х и у правого глаза
            self.y.append(float(newValue[12][0:len(newValue[12])-1]))

        if status == '2' or status == '3': #left
            self.x.append(float(newValue[4][0:len(newValue[4])-1]))#аналогично для левого
            self.y.append(float(newValue[6][0:len(newValue[6])-1]))
        
        self.x.pop(0)
        self.y.pop(0) #удаление первого значения в списке, для того чтобы на графике не была каша

        self.line.set_data(self.x, self.y) #тут уже устнавливаем в сам график

        self.ax.set_xlim(-0.5, 1.5) #длинна по х
        self.ax.set_ylim(1.5, -0.5) #длинна по у 
        self.canvas.draw() #непосрдественное рисование

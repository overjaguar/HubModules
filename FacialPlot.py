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

class FacialPlot(PlotWidget):
    def __init__(self, parent=None, name="Plot"): #конструктор
        super().__init__(parent, name) #наследование

        self.blink, *_ = self.ax.plot([]) #линии графиков
        self.leftWink, *_ = self.ax.plot([])
        self.rightWink, *_ = self.ax.plot([])
        self.eyeBrow, *_ = self.ax.plot([])
        self.furrow, *_ = self.ax.plot([])
        self.smile, *_ = self.ax.plot([])
        self.clench, *_ = self.ax.plot([])

        self.ax.legend([self.blink, self.leftWink, self.rightWink, self.eyeBrow, self.furrow, self.smile, self.clench], ["Blink", "Left Wink", "Right Wink", "Eye Brow", "Furrow", "Smile", "Clench"]) #легенда

        self.time = [] #списки
        self.b = []
        self.lw = []
        self.rw = []
        self.e = []
        self.f = []
        self.s = []
        self.c = []

    def update_plot(self, newValue : str): #обновление графика
        newValue = newValue.split() #сплитим строку
        
        time = datetime.strptime(newValue[2] + " " + newValue[3], '%Y-%m-%d %H:%M:%S') #чтение строку и получение оттуда даты и времени
        time = mktime(utc.localize(time).utctimetuple()) #преобразование в utc формат времени
        if len(self.time) == 0: #если длинна икса равна 0(то есть если первое значение)
            self.startTime = time #тогда сохраняем начальное время

        time = time - self.startTime #от текущего времени отнимается начальное
        self.time.append(time) #добавление времени в список

        self.b.append(float(newValue[5])) #добавление других значений в списки
        self.lw.append(float(newValue[7]))
        self.rw.append(float(newValue[9]))
        self.e.append(float(newValue[11]))
        self.f.append(float(newValue[13]))
        self.s.append(float(newValue[15]))
        self.c.append(float(newValue[17]))

        if len(self.time) >= 50 : #если длинна слишком большая (50) то удаляем первые значения
            self.time.pop(0)
            self.b.pop(0)
            self.lw.pop(0)
            self.rw.pop(0)
            self.e.pop(0)
            self.f.pop(0)
            self.s.pop(0)
            self.c.pop(0)

        self.blink.set_data(self.time, self.b) #тут уже устнавливаем в сам график
        self.leftWink.set_data(self.time, self.lw) #тут уже устнавливаем в сам график
        self.rightWink.set_data(self.time, self.rw) #тут уже устнавливаем в сам график
        self.eyeBrow.set_data(self.time, self.e) #тут уже устнавливаем в сам график
        self.furrow.set_data(self.time, self.f) #тут уже устнавливаем в сам график
        self.smile.set_data(self.time, self.s) #тут уже устнавливаем в сам график
        self.clench.set_data(self.time, self.c) #тут уже устнавливаем в сам график


        self.ax.set_xlim(self.time[0], max(self.time)) #длинна по х
        self.ax.set_ylim(-0.2, 1.25) #длинна по у
        
        self.canvas.draw() #непосрдественное рисование

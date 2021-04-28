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

class EEGPlot(PlotWidget):
    def __init__(self, parent=None, name="Plot"): #конструктор
        super().__init__(parent, name) #наследование

        self.alpha, *_ = self.ax.plot([]) #различие линии графиков
        self.low_beta, *_ = self.ax.plot([])
        self.high_beta, *_ = self.ax.plot([])
        self.theta, *_ = self.ax.plot([])
        self.gamma, *_ = self.ax.plot([])

        self.ax.legend([self.alpha, self.low_beta, self.high_beta, self.theta, self.gamma], ["Alpha", "Low Beta", "High Beta", "Theta", "Gamma"]) #легенда

        self.time = [] #списки
        self.a = []
        self.lb = []
        self.hb = []
        self.g = []
        self.t = []

    def update_plot(self, newValue : str): #обновление графика
        newValue = newValue.split() #сплитим строку

        time = datetime.strptime(newValue[2] + " " + newValue[3], '%Y-%m-%d %H:%M:%S') #чтение строку и получение оттуда даты и времени
        time = mktime(utc.localize(time).utctimetuple()) #преобразование в utc формат времени
        if len(self.time) == 0: #если длинна икса равна 0(то есть если первое значение)
            self.startTime = time #тогда сохраняем начальное время

        time = time - self.startTime #от текущего времени отнимается начальное
        self.time.append(time) #добавление времени в список

        self.t.append(float(newValue[5])) #добавление других значений в списки
        self.a.append(float(newValue[7]))
        self.lb.append(float(newValue[9]))
        self.hb.append(float(newValue[11]))
        self.g.append(float(newValue[13]))

        if len(self.time) >= 50 : #если 50 значений или более начинают удаляться первые значения
            self.time.pop(0)
            self.t.pop(0)
            self.a.pop(0)
            self.lb.pop(0)
            self.hb.pop(0)
            self.g.pop(0)
    
        self.theta.set_data(self.time, self.t) #тут уже устнавливаем в сам график
        self.alpha.set_data(self.time, self.a) #тут уже устнавливаем в сам график
        self.low_beta.set_data(self.time, self.lb) #тут уже устнавливаем в сам график
        self.high_beta.set_data(self.time, self.hb) #тут уже устнавливаем в сам график
        self.gamma.set_data(self.time, self.g) #тут уже устнавливаем в сам график
        
        self.ax.set_xlim(self.time[0], max(self.time)) #длинна по х
        self.ax.set_ylim(-1, max( max(self.t), max(self.a), max(self.lb), max(self.hb), max(self.g) ) + 50) #длинна по у (наибольшее значение + 50)

        self.canvas.draw() #непосрдественное рисование

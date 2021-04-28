#!/usr/bin/env python3
import sys

from PySide2.QtCore import QFile, QObject, Signal, Slot, QTimer, Signal
from PySide2.QtWidgets import QApplication, QVBoxLayout, QWidget
from PySide2.QtUiTools import QUiLoader

from FacialPlot import FacialPlot
from EEGPlot import EEGPlot

import random
#импорт 1001 либы)

class EmotivPlot(QObject): #типа допольный фасад
    def __init__(self, parent=None, name="Plot"): #конструктор
        super().__init__(parent) #наследование
        self.eegPlot = EEGPlot(parent, "EEG plot") #родитель нужен для того, чтобы создавать окно по середине родительского окна (по итоугу не юзаем)
        self.facialPlot = FacialPlot(parent, "Facial plot") #создание еще одного объекта графика

    def update_plot(self, newValue : str): #обновление графика
        if newValue.startswith("EEG"): #если новое значение начинает с еег
            self.eegPlot.update_plot(newValue) #передача значения графиу ээг

        if newValue.startswith("Facial"): #если лицевое
            self.facialPlot.update_plot(newValue) #то другому графику

    def show(self): #вывод обоих графиков
        self.eegPlot.show()
        self.facialPlot.show()

    def close(self): #закрытие окон
        self.eegPlot.close() 
        self.facialPlot.close()
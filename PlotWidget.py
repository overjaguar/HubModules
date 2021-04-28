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

from abc import abstractmethod

import random
#импорт 1001 либы)

class PlotWidget(QWidget):
    def __init__(self, parent=None, name="Plot"): #конструктор
        super().__init__(parent) #наследование методов

        fig = Figure(figsize=(7, 5), dpi=65, facecolor=(1, 1, 1), edgecolor=(0, 0, 0)) #контейнер верхнего уровня графиков. Тип та область в которой рисуется
        self.canvas = FigureCanvas(fig) #создание холста
        self.toolbar = NavigationToolbar(self.canvas, self) #создание навигации
        lay = QVBoxLayout(self) #что-то типа вертикальной сетки
        lay.addWidget(self.toolbar) #добавление в нее тулбара
        lay.addWidget(self.canvas) #добавление на нее графика
        self.ax = fig.add_subplot(111) #создание сетки
        self.setWindowTitle(name) #название окна

    @abstractmethod
    def update_plot(self, newValue):
        """Метод для обновлении данных"""

import sys
from PySide2 import QtWidgets, QtGui
from MainWindow import MainWindow

if __name__ == '__main__': #точка входа в программу и создание окна
    app = QtWidgets.QApplication(sys.argv) #приложение qt widgets
    window = MainWindow() #создание объекта
    window.show() #отображение окна
    sys.exit(app.exec_()) #выполнить
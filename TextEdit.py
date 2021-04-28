from python_ui.textEdit import Ui_Form
from PySide2.QtWidgets import QWidget

class TextEdit(Ui_Form, QWidget):
    def __init__(self, nameOfModule): #конструктор
        super().__init__() #наследование методов родителя
        self.setupUi(self) #создание самого окна
        self.textEdit.setReadOnly(True) #только для чтения
        self.setWindowTitle('Calibration of module: ' + nameOfModule) #название окна

    def insertText(self, text): #метод вставки текста
        self.textEdit.appendPlainText(text) #вставить в конец
        
from python_ui.hubUI import Ui_MainWindow
from PySide2.QtWidgets import QMainWindow, QMessageBox
from AsyncTasks import AsyncTasks
import PySide2


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):  # конструктор
        super().__init__()  # наследование методов родительского классов
        self.setupUi(self)  # создание окна
        # создание объекта для работы с асинхроннстью
        self.asyncTasks = AsyncTasks(self)

        self.pushButtonStart.clicked.connect(
            self.startModules)  # при нажатии запуск
        # притнажатии стоп остановка, кстати внизу тут можно найти под тонной комментов эту функцию
        self.pushButtonStop.clicked.connect(self.stopModules)
        # по умолчанию кнопка выключена остановки
        self.pushButtonStop.setEnabled(False)

        # если модули еще работают, то нельзя нажать кнопку, так как там имитится freeze
        self.asyncTasks.freeze.connect(
            lambda: self.pushButtonStart.setEnabled(False))
        self.asyncTasks.freeze.connect(
            lambda: self.pushButtonStop.setEnabled(True))  # аналогично

        # если завершилось то даем снова нажать кнопку
        self.asyncTasks.finished.connect(
            lambda: self.pushButtonStart.setEnabled(True))
        self.asyncTasks.finished.connect(
            lambda: self.pushButtonStop.setEnabled(False))  # same

        self.nameOfModule = {'miband': "Пульсометр MiBand", 
                             'emotiv': "Электроэнцефалограф Emotiv EPOC",
                             'tobii': "Айтрекер Tobii"}  # словарь названий чекбоксов

    # вывод диалогового окна с просьбой выбрать хоть один модуль
    def showWarningMessage(self, title, text):
        msgBox = QMessageBox(self)
        msgBox.setWindowTitle(title)
        msgBox.setText(text)
        msgBox.setIcon(QMessageBox.Warning)
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.setDefaultButton(QMessageBox.Ok)
        msgBox.exec_()

    def closeEvent(self, event):  # при закрытии окна нужно закрывать все таски
        self.asyncTasks.stopAllTasks()  # остановить все задачи
        event.accept()

    def startModules(self):  # начало запуска модулей
        modulesDict = dict()  # создание словаря
        # добавление модулей и проверка выбранны ли они
        modulesDict['tobii'] = self.checkBoxTobii.isChecked()
        modulesDict['miband'] = self.checkBoxMiband.isChecked()
        modulesDict['emotiv'] = self.checkBoxEmotiv.isChecked()

        if not tuple(modulesDict.values()).count(True):  # если ни один не выбрали
            # вот тут вызывается диалоговое окно и передаются параметры
            self.showWarningMessage(
                title="No one module selected", text="Select at least one module")
            return  # выходим из данной функции

        mode = '-t' if self.radioButtonTest.isChecked() else '-a'  # сохранение режима работы

        # запускаем выбранные модули
        self.asyncTasks.runModules(modulesDict, mode)

        for module in modulesDict:  # для всех модулей
            if not modulesDict[module]:  # если модуля нету, то пропускаем
                continue

            if module == 'miband':  # вызовы функций для всех выбранных преобразования цветов
                self.makeTrafficLights(self.asyncTasks.getWorker(
                    module), self.checkBoxMiband, self.nameOfModule[module])
            if module == 'tobii':
                self.makeTrafficLights(self.asyncTasks.getWorker(
                    module), self.checkBoxTobii, self.nameOfModule[module])
            if module == 'emotiv':
                self.makeTrafficLights(self.asyncTasks.getWorker(
                    module), self.checkBoxEmotiv, self.nameOfModule[module])

    def stopModules(self):  # а вот и она!
        # если остановил, то зачем останавливать -- блокируем нажатие кнопки
        self.pushButtonStop.setEnabled(False)
        self.asyncTasks.stopAllTasks()  # выполнить метод с остановой всех тасков

    def makeTrafficLights(self, worker, checkbox, nameOfModule):  # светофор
        worker.connected.connect(lambda: checkbox.setText(
            '{0} --- Подключен'.format(nameOfModule)))  # если подключился то меняем чебокс
        worker.connected.connect(lambda: checkbox.setStyleSheet(
            "color: rgb(200, 200, 0)"))  # и его цвет на желто-оранжевый

        worker.working.connect(lambda: checkbox.setText(
            '{0} --- Работает'.format(nameOfModule)))  # если работает
        worker.working.connect(lambda: checkbox.setStyleSheet(
            "color: rgb(0, 200, 70)"))  # зеленый цвет

        self.asyncTasks.stopping.connect(lambda: checkbox.setText(
            '{0} --- Останавливается'.format(nameOfModule)))  # в процессе остановки
        self.asyncTasks.stopping.connect(
            lambda: checkbox.setStyleSheet("color: rgb(150, 150, 0)"))

        # если закончил работу и сигнал из воркера, то возвращаем цвета
        worker.finished.connect(
            lambda: checkbox.setText('{0}'.format(nameOfModule)))
        worker.finished.connect(
            lambda: checkbox.setStyleSheet("color: rgb(0, 0, 0)"))

        worker.failed.connect(lambda: checkbox.setText(
            '{0} --- Ошибка'.format(nameOfModule)))  # если неудачная попытка
        worker.failed.connect(
            lambda: checkbox.setStyleSheet("color: rgb(136, 0, 0)"))

        # если поступил сигнал об окончании работы, то возвращаем цвета
        self.asyncTasks.finished.connect(
            lambda: checkbox.setText('{0}'.format(nameOfModule)))
        self.asyncTasks.finished.connect(
            lambda: checkbox.setStyleSheet("color: rgb(0, 0, 0)"))

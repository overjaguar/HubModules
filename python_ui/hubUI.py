# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'hub.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(600, 418)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setEnabled(True)
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.checkBoxMiband = QCheckBox(self.centralwidget)
        self.checkBoxMiband.setObjectName(u"checkBoxMiband")

        self.gridLayout_3.addWidget(self.checkBoxMiband, 0, 0, 1, 1)

        self.checkBoxEmotiv = QCheckBox(self.centralwidget)
        self.checkBoxEmotiv.setObjectName(u"checkBoxEmotiv")

        self.gridLayout_3.addWidget(self.checkBoxEmotiv, 1, 0, 1, 1)

        self.checkBoxTobii = QCheckBox(self.centralwidget)
        self.checkBoxTobii.setObjectName(u"checkBoxTobii")

        self.gridLayout_3.addWidget(self.checkBoxTobii, 2, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 30, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_3.addItem(self.verticalSpacer, 3, 0, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout_3, 0, 0, 1, 1)

        self.gridLayout_6 = QGridLayout()
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_8 = QGridLayout()
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.gridLayout_9 = QGridLayout()
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.gridLayout_12 = QGridLayout()
        self.gridLayout_12.setObjectName(u"gridLayout_12")

        self.gridLayout_9.addLayout(self.gridLayout_12, 0, 0, 1, 1)

        self.gridLayout_13 = QGridLayout()
        self.gridLayout_13.setObjectName(u"gridLayout_13")
        self.pushButtonStop = QPushButton(self.centralwidget)
        self.pushButtonStop.setObjectName(u"pushButtonStop")

        self.gridLayout_13.addWidget(self.pushButtonStop, 1, 0, 1, 1)

        self.pushButtonStart = QPushButton(self.centralwidget)
        self.pushButtonStart.setObjectName(u"pushButtonStart")

        self.gridLayout_13.addWidget(self.pushButtonStart, 0, 0, 1, 1)


        self.gridLayout_9.addLayout(self.gridLayout_13, 0, 1, 1, 1)


        self.gridLayout_8.addLayout(self.gridLayout_9, 0, 0, 1, 1)


        self.gridLayout_6.addLayout(self.gridLayout_8, 0, 0, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout_6, 1, 1, 1, 1)

        self.gridLayout_5 = QGridLayout()
        self.gridLayout_5.setObjectName(u"gridLayout_5")

        self.gridLayout_2.addLayout(self.gridLayout_5, 0, 1, 1, 1)

        self.gridLayout_14 = QGridLayout()
        self.gridLayout_14.setObjectName(u"gridLayout_14")
        self.gridLayout_21 = QGridLayout()
        self.gridLayout_21.setObjectName(u"gridLayout_21")
        self.radioButtonTest = QRadioButton(self.centralwidget)
        self.radioButtonTest.setObjectName(u"radioButtonTest")
        self.radioButtonTest.setChecked(True)

        self.gridLayout_21.addWidget(self.radioButtonTest, 0, 0, 1, 1)

        self.radioButtonSave = QRadioButton(self.centralwidget)
        self.radioButtonSave.setObjectName(u"radioButtonSave")

        self.gridLayout_21.addWidget(self.radioButtonSave, 1, 0, 1, 1)


        self.gridLayout_14.addLayout(self.gridLayout_21, 1, 0, 1, 1)

        self.gridLayout_20 = QGridLayout()
        self.gridLayout_20.setObjectName(u"gridLayout_20")

        self.gridLayout_14.addLayout(self.gridLayout_20, 0, 0, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout_14, 1, 0, 1, 1)


        self.horizontalLayout.addLayout(self.gridLayout_2)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.checkBoxMiband.setText(QCoreApplication.translate("MainWindow", u"\u041f\u0443\u043b\u044c\u0441\u043e\u043c\u0435\u0442\u0440 MiBand", None))
        self.checkBoxEmotiv.setText(QCoreApplication.translate("MainWindow", u"\u042d\u043b\u0435\u043a\u0442\u0440\u043e\u044d\u043d\u0446\u0435\u0444\u0430\u043b\u043e\u0433\u0440\u0430\u0444 Emotiv EPOC", None))
        self.checkBoxTobii.setText(QCoreApplication.translate("MainWindow", u"\u0410\u0439\u0442\u0440\u0435\u043a\u0435\u0440 Tobii", None))
        self.pushButtonStop.setText(QCoreApplication.translate("MainWindow", u"\u0421\u0442\u043e\u043f", None))
        self.pushButtonStart.setText(QCoreApplication.translate("MainWindow", u"\u041d\u0430\u0447\u0430\u0442\u044c", None))
        self.radioButtonTest.setText(QCoreApplication.translate("MainWindow", u"\u0420\u0435\u0436\u0438\u043c \u043a\u0430\u043b\u0438\u0431\u0440\u043e\u0432\u043a\u0438", None))
        self.radioButtonSave.setText(QCoreApplication.translate("MainWindow", u"\u0420\u0435\u0436\u0438\u043c \u0437\u0430\u043f\u0438\u0441\u0438", None))
    # retranslateUi


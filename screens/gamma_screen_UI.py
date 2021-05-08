
from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_GammaScreen(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1850, 1050)
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        MainWindow.setFont(font)
        self.Result = QtWidgets.QWidget(MainWindow)
        self.Result.setStyleSheet("background:black")
        self.Result.setObjectName("Result")
        self.VideoHolder = QtWidgets.QLabel(self.Result)
        self.VideoHolder.setGeometry(QtCore.QRect(100, 100, 1700, 880))
        self.VideoHolder.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"border-style:outset;\n"
"border-radius:10px;\n"
"")
        self.VideoHolder.setText("")
        self.VideoHolder.setObjectName("VideoHolder")
        self.AlertTitle = QtWidgets.QLabel(self.Result)
        self.AlertTitle.setGeometry(QtCore.QRect(960, 30, 251, 51))
        font = QtGui.QFont()
        font.setFamily("\"Arial\"")
        font.setPointSize(14)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.AlertTitle.setFont(font)
        self.AlertTitle.setAutoFillBackground(False)
        self.AlertTitle.setStyleSheet("background-color: rgb(100, 100, 100);\n"
"border-style:outset;\n"
"border-radius:10px;\n"
"color: rgb(250, 255, 255);\n"
"font: 14pt \\\"Arial\\\";")
        self.AlertTitle.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.AlertTitle.setText("")
        self.AlertTitle.setTextFormat(QtCore.Qt.AutoText)
        self.AlertTitle.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.AlertTitle.setObjectName("AlertTitle")
        self.AlertText = QtWidgets.QLabel(self.Result)
        self.AlertText.setGeometry(QtCore.QRect(970, 40, 231, 31))
        font = QtGui.QFont()
        font.setFamily("\"Arial\"")
        font.setPointSize(14)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.AlertText.setFont(font)
        self.AlertText.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"border-style:outset;\n"
"border-radius:10px;\n"
"color: rgb(0, 0, 0);\n"
"font: 14pt \\\"Arial\\\";\n"
"")
        self.AlertText.setText("")
        self.AlertText.setTextFormat(QtCore.Qt.AutoText)
        self.AlertText.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.AlertText.setObjectName("AlertText")

        # MainWindow.setCentralWidget(self.Result)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

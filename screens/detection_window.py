# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'detection_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1221, 724)
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        MainWindow.setFont(font)
        self.Result = QtWidgets.QWidget(MainWindow)
        self.Result.setStyleSheet("background:black")
        self.Result.setObjectName("Result")
        self.VideoHolder = QtWidgets.QLabel(self.Result)
        self.VideoHolder.setGeometry(QtCore.QRect(20, 20, 1181, 681))
        self.VideoHolder.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"border-style:outset;\n"
"border-radius:10px;\n"
"")
        self.VideoHolder.setText("")
        self.VideoHolder.setObjectName("VideoHolder")
        self.AlertTitle = QtWidgets.QLabel(self.Result)
        self.AlertTitle.setGeometry(QtCore.QRect(500, 30, 251, 51))
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
"color: rgba(250, 255, 255, 50%);\n"
"font: 14pt \\\"Arial\\\";")
        self.AlertTitle.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.AlertTitle.setText("")
        self.AlertTitle.setTextFormat(QtCore.Qt.AutoText)
        self.AlertTitle.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.AlertTitle.setObjectName("AlertTitle")
        self.AlertText = QtWidgets.QLabel(self.Result)
        self.AlertText.setGeometry(QtCore.QRect(510, 40, 231, 31))
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
        self.pushButton = QtWidgets.QPushButton(self.Result)
        self.pushButton.setEnabled(False)
        self.pushButton.setGeometry(QtCore.QRect(50, 700, 89, 25))
        self.pushButton.setAutoFillBackground(False)
        self.pushButton.setStyleSheet("background-color:rgb(138, 226, 52);\n"
"color: rgb(46, 52, 54);")
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.Result)
        self.pushButton_2.setEnabled(False)
        self.pushButton_2.setGeometry(QtCore.QRect(540, 700, 89, 25))
        self.pushButton_2.setStyleSheet("background-color: rgb(138, 226, 52);\n"
"color: rgb(46, 52, 54);")
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.Result)
        self.pushButton_3.setEnabled(False)
        self.pushButton_3.setGeometry(QtCore.QRect(1000, 700, 89, 25))
        self.pushButton_3.setAutoFillBackground(False)
        self.pushButton_3.setStyleSheet("background-color: rgb(138, 226, 52);\n"
"color: rgb(46, 52, 54)")
        self.pushButton_3.setObjectName("pushButton_3")
        MainWindow.setCentralWidget(self.Result)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "back"))
        self.pushButton_2.setText(_translate("MainWindow", "phuse"))
        self.pushButton_3.setText(_translate("MainWindow", "next"))


# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI/raw/mainUI.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.width, self.height = 1366, 768

        MainWindow.setObjectName("MainWindow")
        MainWindow.setGeometry(QtCore.QRect(0, 0, self.width, self.height))

        MainWindow.setFixedSize(self.width, self.height)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 10, self.width - 20, 40))

        font = QtGui.QFont()
        font.setFamily("Poppins SemiBold")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(100)

        self.label.setFont(font)
        self.label.setAutoFillBackground(False)
        #self.label.setStyleSheet("QLabel{ background-color: yellow;}")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")

        self.listView = QtWidgets.QListWidget(self.centralwidget)
        self.listView.setGeometry(
            QtCore.QRect(15, 60, int(self.width * 2 / 3) - 30, self.height - self.label.height() - 20))
        self.listView.setObjectName("listView")

        self.player_view = QtWidgets.QWidget(self.centralwidget)
        self.player_view.setGeometry(QtCore.QRect(int(self.width * 2 / 3) - 10, 60, int(self.width * 1 / 3) - 50,
                                                  self.height - self.label.height() - 20))
        self.player_view.setObjectName("player_view")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 953, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Music Player"))

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI/raw/custom_list_songs.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
import urllib.request

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(611, 107)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)

        self.widget_container = QtWidgets.QWidget(Form)
        self.widget_container.setGeometry(QtCore.QRect(10, 10, 591, 91))
        self.widget_container.setObjectName("widget_container")
        self.line_spacer = QtWidgets.QFrame(self.widget_container)
        self.line_spacer.setGeometry(QtCore.QRect(10, 80, 571, 16))
        self.line_spacer.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_spacer.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_spacer.setObjectName("line_spacer")
        self.graphicsView_cover = QtWidgets.QLabel(self.widget_container)
        self.graphicsView_cover.setGeometry(QtCore.QRect(10, 10, 80, 70))
        self.graphicsView_cover.setObjectName("graphicsView_cover")
        self.label_text = QtWidgets.QLabel(self.widget_container)
        self.label_text.setGeometry(QtCore.QRect(120, 20, 451, 51))
        font = QtGui.QFont()
        font.setFamily("Poppins Medium")
        font.setPointSize(10)
        self.label_text.setFont(font)
        self.label_text.setObjectName("label_text")
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_text.setText(_translate("Form", "TextLabel"))

    def setCover(self):
        data = urllib.request.urlopen(self.cover).read()
        pixmap = QPixmap()

        pixmap.loadFromData(data)
        pixmap = pixmap.scaled(self.graphicsView_cover.size(), Qt.KeepAspectRatio,
                               transformMode=Qt.SmoothTransformation)
        self.graphicsView_cover.setPixmap(pixmap)
        self.graphicsView_cover.show()

    def setData(self, name, cover, url=None):
        self.name = name
        self.cover = cover
        self.url = url
        self.label_text.setText(name)
        self.label_text.show()
        pixmap = QPixmap()
        self.graphicsView_cover.setPixmap(pixmap)
        self.graphicsView_cover.show()
        # self.setCover(cover)

    def setDetails(self, details):
        self.details = details
        self.setData(details['name'], details['cover'], "")
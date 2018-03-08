# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainPage.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_mainpage(object):
    def setupUi(self, mainWindow):
        mainWindow.setObjectName("mainWindow")
        mainWindow.resize(606, 280)
        mainWindow.setMinimumSize(QtCore.QSize(606, 280))
        mainWindow.setMaximumSize(QtCore.QSize(606, 280))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(126, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(126, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(126, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(126, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        mainWindow.setPalette(palette)
        mainWindow.setWindowTitle("")
        mainWindow.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        mainWindow.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.centralwidget = QtWidgets.QWidget(mainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.About_label = QtWidgets.QLabel(self.centralwidget)
        self.About_label.setGeometry(QtCore.QRect(220, 240, 161, 31))
        self.About_label.setObjectName("About_label")
        self.tmy3_button = QtWidgets.QPushButton(self.centralwidget)
        self.tmy3_button.setGeometry(QtCore.QRect(75, 9, 211, 103))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.tmy3_button.setFont(font)
        self.tmy3_button.setObjectName("tmy3_button")
        self.mesowest = QtWidgets.QPushButton(self.centralwidget)
        self.mesowest.setGeometry(QtCore.QRect(320, 10, 215, 103))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.mesowest.setFont(font)
        self.mesowest.setObjectName("mesowest")
        self.custom_button = QtWidgets.QPushButton(self.centralwidget)
        self.custom_button.setGeometry(QtCore.QRect(173, 119, 261, 103))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.custom_button.setFont(font)
        self.custom_button.setObjectName("custom_button")
        mainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(mainWindow)
        QtCore.QMetaObject.connectSlotsByName(mainWindow)

    def retranslateUi(self, mainWindow):
        _translate = QtCore.QCoreApplication.translate
        self.About_label.setText(_translate("mainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:18pt; color:#0000ff;\">About LAF</span></p></body></html>"))
        self.tmy3_button.setText(_translate("mainWindow", "Download\n"
"TMY3 Files"))
        self.mesowest.setText(_translate("mainWindow", "Download\n"
" Weather Data\n"
" from MesoWest"))
        self.custom_button.setText(_translate("mainWindow", "Create Customized \n"
" Weather Files"))


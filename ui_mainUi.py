# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainUieDxADM.ui'
##
## Created by: Qt User Interface Compiler version 5.14.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QMetaObject, QObject, QPoint,
    QRect, QSize, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QLinearGradient, QPalette, QPainter, QPixmap,
    QRadialGradient)
from PySide6.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(369, 518)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.regTW = QTableWidget(self.centralwidget)
        if (self.regTW.columnCount() < 3):
            self.regTW.setColumnCount(3)
        __qtablewidgetitem = QTableWidgetItem()
        self.regTW.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.regTW.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.regTW.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        self.regTW.setObjectName(u"regTW")
        self.regTW.setGeometry(QRect(20, 10, 321, 311))
        self.refreshPb = QPushButton(self.centralwidget)
        self.refreshPb.setObjectName(u"refreshPb")
        self.refreshPb.setGeometry(QRect(260, 330, 75, 23))
        self.flowSetDsb = QDoubleSpinBox(self.centralwidget)
        self.flowSetDsb.setObjectName(u"flowSetDsb")
        self.flowSetDsb.setGeometry(QRect(150, 360, 101, 25))
        self.flowSetDsb.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.flowSetDsb.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.flowSetDsb.setMaximum(9999.989999999999782)
        self.flowSetDsb.setSingleStep(50.000000000000000)
        self.flowSetDsb.setValue(9999.989999999999782)
        self.flowSetLbl = QLabel(self.centralwidget)
        self.flowSetLbl.setObjectName(u"flowSetLbl")
        self.flowSetLbl.setGeometry(QRect(100, 360, 47, 25))
        self.sendPb = QPushButton(self.centralwidget)
        self.sendPb.setObjectName(u"sendPb")
        self.sendPb.setGeometry(QRect(260, 360, 75, 23))
        self.flowReadDsb = QDoubleSpinBox(self.centralwidget)
        self.flowReadDsb.setObjectName(u"flowReadDsb")
        self.flowReadDsb.setGeometry(QRect(150, 330, 101, 25))
        self.flowReadDsb.setStyleSheet(u"background-color: rgb(216, 216, 216);")
        self.flowReadDsb.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.flowReadDsb.setReadOnly(True)
        self.flowReadDsb.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.flowReadDsb.setMaximum(9999.989999999999782)
        self.flowReadDsb.setSingleStep(50.000000000000000)
        self.flowReadDsb.setValue(9999.989999999999782)
        self.flowReadLbl = QLabel(self.centralwidget)
        self.flowReadLbl.setObjectName(u"flowReadLbl")
        self.flowReadLbl.setGeometry(QRect(100, 330, 47, 25))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 369, 21))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        ___qtablewidgetitem = self.regTW.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"New Column", None));
        ___qtablewidgetitem1 = self.regTW.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"Registro", None));
        ___qtablewidgetitem2 = self.regTW.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"Valore", None));
        self.refreshPb.setText(QCoreApplication.translate("MainWindow", u"Refresh", None))
        self.flowSetDsb.setSuffix(QCoreApplication.translate("MainWindow", u" NmL/min", None))
        self.flowSetLbl.setText(QCoreApplication.translate("MainWindow", u"Set", None))
        self.sendPb.setText(QCoreApplication.translate("MainWindow", u"Send", None))
        self.flowReadDsb.setSuffix(QCoreApplication.translate("MainWindow", u" NmL/min", None))
        self.flowReadLbl.setText(QCoreApplication.translate("MainWindow", u"Read", None))
    # retranslateUi


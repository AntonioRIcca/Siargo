from .comUi import Ui_comDlg

from PyQt5 import QtWidgets, QtGui, QtCore
from pymodbus.client import ModbusSerialClient  # per pymodbus 3.3.x e Python 3.11
import sys
import serial.tools.list_ports
import yaml
from Utility.variables import instr, folders


class Com(QtWidgets.QDialog):
    def __init__(self):
        super(Com, self).__init__()
        self.ui = Ui_comDlg()
        self.ui.setupUi(self)

        self.ui.confirmPb.setVisible(False)

        self.ui.comCb.clear()
        ports = []
        for port in serial.tools.list_ports.comports():
            ports.append(port.name)
            self.ui.comCb.addItem(port.name)
        self.ui.comCb.setCurrentText(instr['conn']['com'])
        self.ui.slaveSb.setValue(instr['conn']['slave'])

        self.ui.testPb.clicked.connect(self.connn_test)
        self.ui.comCb.currentIndexChanged.connect(self.new_set)
        self.ui.slaveSb.valueChanged.connect(self.new_set)
        self.ui.confirmPb.clicked.connect(self.confirm)

    def connn_test(self):
        comport = self.ui.comCb.currentText()
        slave = self.ui.slaveSb.value()

        client = ModbusSerialClient(
            port=comport,  # TODO: inserire la COM esatta
            startbit=1,
            databits=8,
            parity="N",
            stopbits=2,
            errorcheck="crc",
            baudrate=38400,
            method="RTU",
            timeout=1,
            # unit=31
        )

        try:
            sn = client.read_holding_registers(address=48, count=1, slave=slave).registers[0]
        except:
            sn = 0

        self.ui.confirmPb.setVisible(sn > 0)
        if sn > 0:
            self.ui.logLe.setText('Connessione OK')
        else:
            self.ui.logLe.setText('Connessione FALLITA')

        client.close()

    def new_set(self):
        self.ui.confirmPb.setVisible(False)
        self.ui.logLe.clear()

    def confirm(self):
        instr['conn']['com'] = self.ui.comCb.currentText()
        instr['conn']['slave'] = self.ui.slaveSb.value()

        with open(folders['cfg'] + 'config.yml', 'w') as f:
            yaml.dump(instr, f)
        self.close()

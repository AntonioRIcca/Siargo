import copy

import yaml
from pymodbus.client import ModbusSerialClient  # per pymodbus 3.3.x e Python 3.11
from mainUi import Ui_MainWindow
from PyQt5 import QtWidgets, QtCore, QtGui

from threading import Thread

import sys

import serial.tools.list_ports

from Utility.variables import instr

for port in serial.tools.list_ports.comports():
    print(f'Current port: {port.name}')
# print(list(serial.tools.list_ports.comports()))

mb_conn = True

mb_reg = {
    'Function': {
        'reg': 130,
        'desc': 'Product Address',
        'value': 0,
    },
    'Serial number': {
        'reg': 49,
        'desc': 'Serial number of the product',
        'value': 0,
    },
    'Flow rate 1': {
        'reg': 59,
        'desc': 'Serial number of the product',
        'value': 0,
    },
    'Flow rate 2': {
        'reg': 60,
        'desc': 'Serial number of the product',
        'value': 0,
    },
    'Baud rate': {
        'reg': 131,
        'desc': 'Communication baud rate',
        'value': 0,
    },
    'Set point source': {
        'reg': 187,
        'desc': 'Set the setpoint source',
        'value': 0,
    },
    'Set point Flow Code': {
        'reg': 188,
        'desc': 'Set the flow rate in percentage of the full-scale flow',
        'value': 0,
    },
    'Flow1': {
        'reg': 189,
        'desc': 'Read the current flow rate set by the user',
        'value': 0,
    },
    'Flow2': {
        'reg': 190,
        'desc': 'Read the current flow rate set by the user',
        'value': 0,
    },
    'P gain': {
        'reg': 191,
        'desc': 'PD proportional control of the valve/flow rate',
        'value': 0,
    },
    'D gain': {
        'reg': 192,
        'desc': 'PD differential control of the valve/flow rate',
        'value': 0,
    },
    'Valve preload offset': {
        'reg': 193,
        'desc': 'Default or preloaded valve opening',
        'value': 0,
    },
    'Exhaust mode': {
        'reg': 194,
        'desc': 'Set the exhaust mode',
        'value': 0,
    },
    'Exhaust valve': {
        'reg': 195,
        'desc': 'Percentage of the opened valve (Open loop control)',
        'value': 0,
    },
    'Valve status': {
        'reg': 196,
        'desc': 'Percentage of the opened valve',
        'value': 0,
    },
    # 'Offset calibration': {
    #     'reg': 241,
    #     'desc': 'Offset reset or calibration',
    #     'value': 0,
    # },
    # 'Write protection': {
    #     'reg': 256,
    #     'desc': 'Write protection of selected parameters',
    #     'value': 0,
    # },
    'GCF': {
        'reg': 140,
        'desc': 'Write protection of selected parameters',
        'value': 0,
    },
}


class Main:
    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)
        self.mainwindow = QtWidgets.QMainWindow()

        self.mb_conn_par()

        # self.interface_open()
        f0 = Thread(target=self.interface_open())
        f0.start()
        self.tab_create()

        pass

    def interface_open(self):   # Impostazione e apertuda dell'interfaccia
        self.main = Ui_MainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.mainwindow)

        self.tab_create()

        if not self.mb_check():
            self.com_selection()

        self.mb_connect()

        # -- Definizione delle azioni --------------------------------------------------------------------
        self.ui.refreshPb.clicked.connect(self.tab_refresh)
        self.ui.sendPb.clicked.connect(self.setpoint_set)
        # ------------------------------------------------------------------------------------------------

        timer = QtCore.QTimer()
        timer.timeout.connect(self.tab_refresh)
        timer.start(1000)

        self.mainwindow.show()
        self.app.exec()

    def mb_connect(self):
        self.client = ModbusSerialClient(
            port=instr['conn']['com'],
            startbit=1,
            databits=8,
            parity="N",
            stopbits=2,
            errorcheck="crc",
            baudrate=38400,
            method="RTU",
            timeout=3,
            # unit=31
        )

    def mb_check(self):
        self.mb_connect()
        try:
            test = self.client.read_holding_registers(address=48, count=1, slave=instr['conn']['slave']).registers[0]
        except:
            test = 0
        self.client.close()
        return test > 0

    def mb_conn_par(self):
        with open('_data/config.yml') as f:
            cfg = yaml.safe_load(f)
        for p in cfg:
            instr[p] = copy.deepcopy(cfg[p])

    def mb_reg_read_all(self, lenght=200):
        results = []
        if self.client.connect():  # Connessione al dispositivo
            registers = 250
            addr = 0
            while addr < registers:
                count = min(100, registers-addr)
                results += self.client.read_holding_registers(address=addr,
                                                              count=count,
                                                              slave=instr['conn']['slave']).registers
                addr += count

            for par in mb_reg:
                addr = mb_reg[par]['reg'] - 1
                mb_reg[par]['value'] = results[addr]

                print(par, addr, mb_reg[par]['value'])
        else:
            mb_conn = False

    def tab_create(self):
        for par in mb_reg:
            r = self.ui.regTW.rowCount()
            self.ui.regTW.insertRow(r)
            self.ui.regTW.setItem(r, 0, QtWidgets.QTableWidgetItem(par))
            self.ui.regTW.setItem(r, 1, QtWidgets.QTableWidgetItem(str(mb_reg[par]['reg'])))
            self.ui.regTW.setItem(r, 2, QtWidgets.QTableWidgetItem(str(mb_reg[par]['value'])))

        print(self.ui.regTW.rowCount())

    def tab_refresh(self):
        print('refresh')
        self.mb_reg_read_all()
        # print(self.ui.regTW.item(2, 2).text())
        for i in range(len(list(mb_reg.keys()))):
            par = self.ui.regTW.item(i, 0).text()
            print(i, par, mb_reg[par]['value'])
            self.ui.regTW.item(i, 2).setText(str(mb_reg[par]['value']))

        self.ui.flowRateDsb.setValue((mb_reg['Flow rate 1']['value'] * 65536 + mb_reg['Flow rate 2']['value']) / 1000)
        self.ui.flowReadDsb.setValue((mb_reg['Flow1']['value'] * 65536 + mb_reg['Flow2']['value']) / 1000)

    def setpoint_set(self):
        if self.client.connect():  # Connessione al dispositivo
            value = self.ui.flowSetDsb.value() / 1000 * 64000
            self.client.write_register(slave=instr['conn']['slave'], address=187, value=int(value))

    def com_selection(self):
        self.client.close()

        from Utility.COM.com import Com
        self.comsel = Com()
        self.comsel.show()
        self.comsel.exec_()


    def dopo(self):
        if client.connect():  # Connessione al dispositivo
            registers = 250
            results = []
            addr = 0
            while addr < registers:
                count = min(100, registers-addr)
                results += client.read_holding_registers(address=addr, count=count, slave=1).registers
                addr += count

        else:
            mb_conn = False

        # print(mb_conn)
        # print(results)
        # print(len(results))

        for par in mb_reg:
            addr = mb_reg[par]['reg'] - 1
            mb_reg[par]['value'] = results[addr]

            print(par, addr, mb_reg[par]['value'])


        if client.connect():  # Connessione al dispositivo
            client.write_register(slave=1, address=187, value=int(0.0*64000))

        if client.connect():  # Connessione al dispositivo
            registers = 250
            results = []
            addr = 0
            while addr < registers:
                count = min(100, registers-addr)
                results += client.read_holding_registers(address=addr, count=count, slave=1).registers
                addr += count
        else:
            mb_conn = False

        for par in mb_reg:
            addr = mb_reg[par]['reg'] - 1
            mb_reg[par]['value'] = results[addr]

            print(par, addr, mb_reg[par]['value'])


Main()
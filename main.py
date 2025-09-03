import copy

import yaml
from pymodbus.client import ModbusSerialClient  # per pymodbus 3.3.x e Python 3.11
from ui.mainUi import Ui_MainWindow
from PyQt5 import QtWidgets, QtCore, QtGui

import csv

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

import time

from threading import Thread

import sys
import os
from datetime import datetime as dt

import serial.tools.list_ports

from ui.CustomFlowRate.customFlowRate import CustomFlowRate
from Utility.variables import instr, mb_reg, par, folders
#
# for port in serial.tools.list_ports.comports():
#     print(f'Current port: {port.name}')

mb_conn = True


class Main:
    def __init__(self):
        os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"     # Necessaria per il rescaling

        self.app = QtWidgets.QApplication(sys.argv)

        # -- Necessario per il rescaling --------------
        self.app.setAttribute(QtCore.Qt.ApplicationAttribute.AA_EnableHighDpiScaling)
        self.mainwindow = QtWidgets.QMainWindow()
        # ---------------------------------------------

        self.folders_manager()  # Definizione delle cartelle di salvataggio

        self.mb_conn_par()      # Lettura dei parametri di connessione e di flusso

        # -- Avvio interfaccia principale -------------------------------------------
        f0 = Thread(target=self.interface_open())
        f0.start()
        # ---------------------------------------------------------------------------

    def interface_open(self):   # Impostazione e apertura dell'interfaccia
        self.main = Ui_MainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.mainwindow)

        fake = False
        self.ui.fakeCkb.setVisible(fake)
        self.ui.fake_flowReadDsb.setVisible(fake)

        self.tab_create()       # Inizializzazione tabella parametri MFC
        self.mb_connect()       # Inizializzazione della connessione al MFC

        # -- Verifica della connessione ---------------------------------------------
        connected = self.mb_check()
        if not connected:
            connected = self.com_selection()
        # ---------------------------------------------------------------------------

        if connected:
            # Inserimento immagini nell'interfaccia
            self.ui.topImgLbl.setPixmap(QtGui.QPixmap('img/top_banner_300x50.png'))
            self.ui.mfcImgLbl.setPixmap(QtGui.QPixmap('img/mfc_100x100.png'))

            self.mb_connect()   # Inizializzazione della connessione con il dispositivo

            # -- Lettura del fondoscala del MFC impostato dalla fabbrica ----------------
            try:
                instr['flux']['def'] = self.client.read_holding_registers(address=139,
                                                                          count=1,
                                                                          slave=instr['conn']['slave']
                                                                          ).registers[0]
            except:
                pass
            # ---------------------------------------------------------------------------

            # -- Definizione della capacità dello strumento -----------------------------
            if not instr['flux']['custom']:
                instr['flux']['cap'] = instr['flux']['def']

            self.ui.capLbl.setText('Capacity: %.2f NmL/min' % instr['flux']['cap'])
            self.ui.setFlowDsb.setMaximum(instr['flux']['cap'])
            # ---------------------------------------------------------------------------

            self.start_t = time.perf_counter()      # definizione del tempo 0

            # -- Inizializzazione della tabella di salvataggio dati ---------------------
            fieldnames = ['time [s]', 'Q_set [Nml/min]', 'Q_read [NmL/min]']
            folders['datapath'] = folders['data'] + '/' + dt.now().strftime('%Y%m%d_%H%M%S') + '.csv'
            with open(folders['datapath'], 'a', newline='') as csv_file:
                csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                csv_writer.writeheader()
            # ---------------------------------------------------------------------------

            self.graph_init()       # Inizializzazione del grafico

            # -- Definizione delle azioni -----------------------------------------------
            self.ui.setFlowDsb.lineEdit().returnPressed.connect(self.setpoint_set)
            self.ui.rightExpandPb.clicked.connect(self.right_expand)
            self.ui.downExpandPb.clicked.connect(self.down_expand)
            self.ui.capLbl.mouseDoubleClickEvent = self.custom_flow_rate
            self.mainwindow.closeEvent = self.close
            # ---------------------------------------------------------------------------

            # -- Impostazione del ciclo delle azioni ------------------------------------
            timer = QtCore.QTimer()
            timer.timeout.connect(self.refresh)
            timer.start(200)
            # ---------------------------------------------------------------------------

            # Avvio dell'interfaccia
            self.mainwindow.setFixedSize(self.mainwindow.size())
            self.mainwindow.setWindowIcon(QtGui.QIcon('img/siargo_ico.ico'))
            self.mainwindow.show()
            self.app.exec()

    def mb_connect(self):   # Inizializzazione della connessione al MFC
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

    def mb_check(self):     # Verifica della connessione
        # Prova di lettira del Serial Number del MFC
        try:
            test = self.client.read_holding_registers(address=48, count=1, slave=instr['conn']['slave']).registers[0]
        except:
            test = 0
        self.client.close()
        return test > 0

    def mb_conn_par(self):      # Lettura dei parametri di connessione e di flusso
        with open(folders['cfg'] + '/config.yml') as f:
            cfg = yaml.safe_load(f)
        for p in cfg:
            instr[p] = copy.deepcopy(cfg[p])

    def mb_reg_read_all(self, lenght=200):      # Lettura dei registri del MFC
        results = []    # Registro provvisorio dei valodi di registro

        if self.client.connect():  # Connessione al dispositivo
            # lettura dei primi 250 registri del MFC
            registers = 250
            addr = 0
            while addr < registers:
                count = min(100, registers-addr)
                results += self.client.read_holding_registers(address=addr,
                                                              count=count,
                                                              slave=instr['conn']['slave']).registers
                addr += count

            # poppolamento del dizionario "mb_par"
            for par in mb_reg:
                addr = mb_reg[par]['reg'] - 1
                mb_reg[par]['value'] = results[addr]

    def tab_create(self):   # Inizializzazione tabella parametri MFC
        for par in mb_reg:
            r = self.ui.regTW.rowCount()
            self.ui.regTW.insertRow(r)
            self.ui.regTW.setItem(r, 0, QtWidgets.QTableWidgetItem(par))
            self.ui.regTW.setItem(r, 1, QtWidgets.QTableWidgetItem(str(mb_reg[par]['reg'])))
            self.ui.regTW.setItem(r, 2, QtWidgets.QTableWidgetItem(str(mb_reg[par]['value'])))

        self.ui.regTW.setColumnWidth(0, 140)
        self.ui.regTW.setColumnWidth(1, 50)
        self.ui.regTW.setColumnWidth(2, 65)
        self.ui.regTW.setVisible(False)     # La tabella di default è nascosta

    def tab_refresh(self):  # Popolamento della tabella dei parametri del MFC
        self.mb_reg_read_all()  # lettura del registro del MFC

        # Scrittura della tabella dei parametri
        for i in range(len(list(mb_reg.keys()))):
            par = self.ui.regTW.item(i, 0).text()
            self.ui.regTW.item(i, 2).setText(str(mb_reg[par]['value']))

    def setpoint_set(self):     # Invio del setpoint
        par['set'] = self.ui.setFlowDsb.value()
        if self.client.connect():  # Connessione al dispositivo
            value = self.ui.setFlowDsb.value() / instr['flux']['cap'] * 64000   # valore in P.U. del setpoint

            # Invio al MFC del SetPoint Percentuale
            self.client.write_register(slave=instr['conn']['slave'], address=187, value=int(value))

            # Aggiornamento dell'interfaccia grafica
            self.ui.setPercDsb.setValue(self.ui.setFlowDsb.value() / instr['flux']['cap'] * 100)
            self.ui.setPrB.setValue(int(self.ui.setPercDsb.value()))

    def com_selection(self):    # Selezione della porte COM
        self.client.close()

        from Utility.COM.com import Com
        self.comsel = Com()
        self.comsel.show()
        self.comsel.exec_()
        return self.comsel.ui.logLe.text() == 'Connessione OK'

    def refresh(self):          # Azioni cicliche
        # -- Lettura del valore del flusso ------------------------------------------
        if self.ui.fakeCkb.isChecked():     # Nel caso di Fake Flow
            par['read'] = self.ui.fake_flowReadDsb.value() / 100 * instr['flux']['cap']
        else:                               # Nel caso reale
            par['read'] = ((mb_reg['Flow rate 1']['value'] * 65536 + mb_reg['Flow rate 2']['value'])
                           / 1e6 * instr['flux']['cap'])
        # ---------------------------------------------------------------------------

        # -- Aggiornamento dell'interfaccia grafica ---------------------------------
        self.ui.readFlowDsb.setValue(par['read'])
        self.ui.readPercDsb.setValue(self.ui.readFlowDsb.value() / instr['flux']['cap'] * 100)
        self.ui.readPrB.setValue(int(self.ui.readPercDsb.value()))
        # ---------------------------------------------------------------------------

        # -- Definizione del colore della barra percentuale -------------------------
        if abs(self.ui.readPercDsb.value() - self.ui.setPercDsb.value()) / max(0.1, self.ui.setPercDsb.value()) > 0.05:
            col = "rgb(170, 0, 0)"
        elif abs(self.ui.readPercDsb.value() - self.ui.setPercDsb.value()) / max(0.1, self.ui.setPercDsb.value()) > 0.02:
            col = "rgb(255, 170, 0)"
        else:
            col = "rgb(0, 130, 0)"
        self.ui.readPrB.setStyleSheet('QProgressBar::chunk{background-color: '+ col + ' ; margin: 1px;}')
        # ---------------------------------------------------------------------------

        self.tab_refresh()      # Aggironamento della tabella
        self.data_storage()     # Salvataggio dati
        self.graph_update()     # Aggiornamento del grafico

    def data_storage(self):     # Salvataggio dati
        fieldnames = ['time [s]', 'Q_set [Nml/min]', 'Q_read [NmL/min]']

        # Scrittura della linea dei dati
        with open(folders['datapath'], 'a', newline='') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            line = {
                'time [s]': (time.perf_counter() - self.start_t) / 60,
                'Q_set [Nml/min]': par['set'],
                'Q_read [NmL/min]': par['read']
            }

            csv_writer.writerow(line)

    def custom_flow_rate(self, event=None):     # Modifica del fondo-scala
        popup = CustomFlowRate()
        popup.setFixedSize(200, 80)

        if popup.exec_():
            pass
        self.ui.capLbl.setText('Capacity: %.2f NmL/min' % instr['flux']['cap'])
        self.ui.setFlowDsb.setMaximum(instr['flux']['cap'])
        self.setpoint_set()     # Aggiornamento del setpoint sulla base del nuovo fondoscala

    def right_expand(self):     # Visualizzazione/nascondimento del grafico
        if par['down_expanded']:
            h = 490
        else:
            h = 250

        if par['right_expanded']:
            self.mainwindow.setFixedSize(350, h)
            self.ui.rightExpandPb.setText('>')
        else:
            self.mainwindow.setFixedSize(980, 490)
            self.ui.rightExpandPb.setText('<')
        par['right_expanded'] = not par['right_expanded']

    def down_expand(self):      # Visualizzazione/nascondimento della tabella
        # definizione delle dimensioni prima dell'azione
        l = self.mainwindow.size().width()
        if par['right_expanded']:
            h = 490
        else:
            h = 250

        if par['down_expanded']:
            self.mainwindow.setFixedSize(l, h)
            self.ui.downExpandPb.setText('V')
        else:
            self.mainwindow.setFixedSize(l, 490)
            # self.mainwindow.move(10,10)
            self.ui.downExpandPb.setText('A')
        par['down_expanded'] = not par['down_expanded']
        self.ui.regTW.setVisible(par['down_expanded'])

    def graph_init(self):       # inizializzazione del grafico
        self.graph_canvas = FigureCanvas(plt.Figure(figsize=(3, 2)))
        self.ax_Q = self.graph_canvas.figure.subplots()
        self.ui.graphMainHBL.addWidget(self.graph_canvas)

        self.line_Qset = self.ax_Q.plot([0, 1], [0, 10], label='Q Set')[0]
        self.line_Qread = self.ax_Q.plot([0, 1], [0, 7], label='Q read')[0]
        self.ax_Q.set_xlabel('Time [min]')
        self.ax_Q.set_ylabel('Flow Rate [NmL/min]')

        self.handles_Q = self.ax_Q.get_legend_handles_labels()[0]
        self.labels_Q = self.ax_Q.get_legend_handles_labels()[1]
        self.ax_Q.legend(self.handles_Q, self.labels_Q)

    def graph_update(self):     # Aggiornamento del grafico
        data = pd.read_csv(folders['datapath'])     # lettura dei dati da file

        self.line_Qset.set_xdata(data['time [s]'])
        self.line_Qread.set_xdata(data['time [s]'])
        self.line_Qset.set_ydata(data['Q_set [Nml/min]'])
        self.line_Qread.set_ydata(data['Q_read [NmL/min]'])

        self.x_axis_manager(data)   # aggiornamento dell'asse x
        self.y_axis_manager(data)   # aggiornamento dell'asse y

        self.graph_canvas.draw()
        self.graph_canvas.flush_events()
        pass

    def x_axis_manager(self, data):     # Aggiornamento dell'asse x
        self.ui.xminDsb.setEnabled(not self.ui.xautorangePb.isChecked())
        self.ui.xmaxDsb.setEnabled(not self.ui.xautorangePb.isChecked())
        self.ui.xposSld.setEnabled(not self.ui.xautorangePb.isChecked())

        self.ui.xrangeDsb.setEnabled(self.ui.xautorangePb.isChecked())
        self.ui.xrangeSld.setEnabled(self.ui.xautorangePb.isChecked())

        try:
            self.ui.xposSld.valueChanged.disconnect()
        except:
            pass

        try:
            self.ui.xrangeSld.valueChanged.disconnect()
        except:
            pass

        if self.ui.xautorangePb.isChecked():
            # self.ui.xminDsb.setValue(max(0, int(max(data['time [s]'])) - self.ui.xrangeDsb.value()))
            self.ui.xmaxDsb.setValue(max(int(max(data['time [s]'])) + 1, 1))
            self.ui.xminDsb.setValue(self.ui.xmaxDsb.value() - self.ui.xrangeDsb.value())
            self.ui.xposSld.setValue(int(self.ui.xmaxDsb.value()))

            self.ui.xrangeSld.setMaximum(int(max(data['time [s]'])) + 1)
            self.ui.xrangeSld.setValue(int(self.ui.xrangeDsb.value()))

            try:
                self.ui.xrangeSld.valueChanged.connect(self.xrange_changed)
            except:
                pass
        else:
            self.ui.xrangeDsb.setValue(self.ui.xmaxDsb.value() - self.ui.xminDsb.value())
            self.ui.xrangeSld.setValue(int(self.ui.xrangeDsb.value()))

            self.ui.xposSld.setMinimum(int(self.ui.xrangeDsb.value()))
            self.ui.xposSld.setMaximum(int(max(data['time [s]'])) + 1)
            self.ui.xposSld.setValue(int(self.ui.xmaxDsb.value()))

            try:
                self.ui.xposSld.valueChanged.connect(self.xslide_changed)
            except:
                pass

        self.ax_Q.set_xlim(left=self.ui.xminDsb.value(),
                           right=self.ui.xmaxDsb.value())

    def xslide_changed(self):
        self.ui.xmaxDsb.setValue(self.ui.xposSld.value())
        self.ui.xminDsb.setValue(self.ui.xposSld.value() - self.ui.xrangeDsb.value())

    def xrange_changed(self):
        self.ui.xrangeDsb.setValue(self.ui.xrangeSld.value())

    def y_axis_manager(self, data):
        self.ui.yminDsb.setReadOnly(self.ui.yautorangePb.isChecked())
        self.ui.ymaxDsb.setReadOnly(self.ui.yautorangePb.isChecked())

        self.ui.yminDsb.setMinimum(0)
        self.ui.yminDsb.setMaximum(self.ui.ymaxDsb.value() - 1)
        self.ui.ymaxDsb.setMinimum(self.ui.yminDsb.value() + 1)

        if self.ui.yautorangePb.isChecked():
            y_max = max(max(data['Q_set [Nml/min]']), max(data['Q_read [NmL/min]'])) + 50
            y_min = 0
            self.ui.yminDsb.setValue(0)
            self.ui.ymaxDsb.setValue(y_max)
        else:
            y_min = self.ui.yminDsb.value()
            y_max = self.ui.ymaxDsb.value()

        self.ax_Q.set_ylim(bottom=y_min, top=y_max)

    def folders_manager(self):      # Definizione delle cartelle di salvataggio
        folders['data'] = os.path.join(os.environ['USERPROFILE'], 'Documents', 'Siargo')
        if not os.path.isdir(folders['data']):
            os.makedirs(folders['data'])

        folders['cfg'] = os.path.join(os.environ['USERPROFILE'], 'Siargo')
        folders['cfgdata'] = os.path.join(folders['cfg'], 'config.yml')
        if not os.path.isdir(folders['cfg']):
            os.makedirs(folders['cfg'])
            with open(folders['cfgdata'], 'w') as f:
                yaml.dump(instr, f)

    def close(self, event):
        if self.client.connect():  # Connessione al dispositivo
            self.client.write_register(slave=instr['conn']['slave'], address=187, value=0)
            self.client.close()
        with open(folders['cfg'] + '/config.yml', 'w') as f:
            yaml.dump(instr, f)


Main()

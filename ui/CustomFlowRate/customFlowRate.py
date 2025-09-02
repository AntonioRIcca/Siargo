from ui.CustomFlowRate.customFlowRateUI import Ui_CustDlg

from PyQt5 import QtWidgets

from Utility.variables import instr


class CustomFlowRate(QtWidgets.QDialog):
    def __init__(self):
        super(CustomFlowRate, self).__init__()
        self.ui = Ui_CustDlg()
        self.ui.setupUi(self)

        self.ui.custCkb.setChecked(instr['flux']['custom'])
        self.ui.custFlowDsb.setValue(instr['flux']['cap'])

        self.cust_check()

        self.ui.confirmPb.clicked.connect(self.confirm)
        self.ui.custCkb.clicked.connect(self.cust_check)

    def confirm(self):
        instr['flux']['cap'] = self.ui.custFlowDsb.value()
        instr['flux']['custom'] = self.ui.custCkb.isChecked()
        self.close()

    def cust_check(self):
        if self.ui.custCkb.isChecked():
            bg = 'rgb(255, 255, 255)'
        else:
            bg = 'rgb(216, 216, 216)'
            self.ui.custFlowDsb.setValue(instr['flux']['def'])
        self.ui.custFlowDsb.setStyleSheet('background-color: ' + bg + ';')
        self.ui.custFlowDsb.setEnabled(self.ui.custCkb.isChecked())


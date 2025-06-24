from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QDialog, QTableWidgetItem, QHeaderView
from PyQt5 import QtWidgets

from guipy.ui import Ui_Dialog


class MainView(QDialog):
    signal_view_init = pyqtSignal()

    def __init__(self):
        super(MainView, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.view_init()

    def view_init(self):
        self.ui.labelMsg.setText("")
        self.ui.pushButtonAddNewLinVar.setEnabled(False)
        self.ui.pushButtonDraw.setEnabled(False)
        self.ui.pushButtonRuleAdd.setEnabled(False)
        self.ui.pushButtonRuleDel.setEnabled(False)
        self.connects()
        self.ui.lineEditNewLinVarName.setText("Лингвистическая переменная 1")
        self.table_init()

    def connects(self):
        self.ui.lineEditNewLinVarName.textChanged.connect(
            lambda: self.enable_buttons(self.ui.lineEditNewLinVarName.text(), self.ui.tableWidget.rowCount()))
        self.ui.pushButtonAddNewTerm.released.connect(self.on_add_new_term)
        self.ui.pushButtonDelTerm.released.connect(self.on_del_selected_term)
        self.ui.comboBoxRules.currentTextChanged.connect(
            lambda: self.enable_button_del_rule(self.ui.comboBoxRules.currentText()))

    def table_init(self):
        self.ui.tableWidget.setRowCount(2)
        self.ui.tableWidget.setColumnCount(5)
        self.ui.tableWidget.setHorizontalHeaderLabels(
            ['левая нижн точка', 'левая верхн точка', 'правая верхн точка', 'правая нижн точка', 'названия термов'])
        self.ui.tableWidget.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)

        self.ui.tableWidget.setItem(0, 0, QTableWidgetItem('0'))
        self.ui.tableWidget.setItem(0, 1, QTableWidgetItem('0'))
        self.ui.tableWidget.setItem(0, 2, QTableWidgetItem('30'))
        self.ui.tableWidget.setItem(0, 3, QTableWidgetItem('40'))
        self.ui.tableWidget.setItem(0, 4, QTableWidgetItem(f'Терм 1'))

        self.ui.tableWidget.setItem(1, 0, QTableWidgetItem('35'))
        self.ui.tableWidget.setItem(1, 1, QTableWidgetItem('70'))
        self.ui.tableWidget.setItem(1, 2, QTableWidgetItem('100'))
        self.ui.tableWidget.setItem(1, 3, QTableWidgetItem('100'))
        self.ui.tableWidget.setItem(1, 4, QTableWidgetItem(f'Терм 2'))

        self.ui.tableWidget.resizeColumnsToContents()
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.enable_buttons(self.ui.lineEditNewLinVarName.text(), self.ui.tableWidget.rowCount())

    def enable_buttons(self, txt, rows):
        if txt == "" or txt.isspace() or rows < 2:
            self.ui.pushButtonAddNewLinVar.setEnabled(False)
            self.ui.pushButtonDraw.setEnabled(False)
        else:
            self.ui.pushButtonAddNewLinVar.setEnabled(True)
            self.ui.pushButtonDraw.setEnabled(True)

    def enable_button_del_rule(self, txt):
        if txt == "" or txt.isspace():
            self.ui.pushButtonRuleDel.setEnabled(False)
        else:
            self.ui.pushButtonRuleDel.setEnabled(True)

    def get_table_data(self):
        table_data = []
        for r in range(self.ui.tableWidget.rowCount()):
            item0 = self.ui.tableWidget.item(r, 0).text()
            item1 = self.ui.tableWidget.item(r, 1).text()
            item2 = self.ui.tableWidget.item(r, 2).text()
            item3 = self.ui.tableWidget.item(r, 3).text()
            item4 = self.ui.tableWidget.item(r, 4).text()
            table_data.append([item0, item1, item2, item3, item4])
        return self.ui.lineEditNewLinVarName.text(), table_data

    def get_rule_data(self):
        data = [None] * 12
        data[0] = self.ui.comboBoxLv0.currentText()
        data[1] = self.ui.comboBoxTermsLv0.currentText()
        data[2] = self.ui.lineEditVar0.text()
        data[3] = self.ui.lineEditValueVar0.text()
        data[4] = self.ui.comboBoxOperator.currentText()
        data[5] = self.ui.comboBoxLv1.currentText()
        data[6] = self.ui.comboBoxTermsLv1.currentText()
        data[7] = self.ui.lineEditVar1.text()
        data[8] = self.ui.lineEditValueVar1.text()
        data[9] = self.ui.comboBoxLv2.currentText()
        data[10] = self.ui.comboBoxTermsLv2.currentText()
        data[11] = self.ui.lineEditVar2.text()
        return data

    def send_err_msg(self, msg):
        self.ui.labelMsg.setText(msg)

    def on_add_new_term(self):
        rowPosition = self.ui.tableWidget.rowCount()
        self.ui.tableWidget.insertRow(rowPosition)
        self.ui.tableWidget.setItem(rowPosition, 4, QTableWidgetItem(f'Терм {rowPosition + 1}'))
        for col in range(self.ui.tableWidget.columnCount() - 1):
            self.ui.tableWidget.setItem(rowPosition, col, QTableWidgetItem(""))
        self.enable_buttons(self.ui.lineEditNewLinVarName.text(), self.ui.tableWidget.rowCount())

    def on_del_selected_term(self):
        self.ui.tableWidget.removeRow(self.ui.tableWidget.currentRow())
        self.enable_buttons(self.ui.lineEditNewLinVarName.text(), self.ui.tableWidget.rowCount())

    def set_operators(self, opers):
        self.ui.comboBoxOperator.clear()
        self.ui.comboBoxOperator.addItems(opers)

    def set_lin_vars(self, filenames):
        self.ui.comboBoxLv0.clear()
        self.ui.comboBoxLv1.clear()
        self.ui.comboBoxLv2.clear()
        self.ui.comboBoxLv0.addItems(filenames)
        self.ui.comboBoxLv1.addItems(filenames)
        self.ui.comboBoxLv2.addItems(filenames)

    def set_rules(self, filenames):
        if len(filenames) == 0:
            self.ui.pushButtonCalculate.setEnabled(False)
        else:
            self.ui.pushButtonCalculate.setEnabled(True)
        self.ui.comboBoxRules.clear()
        self.ui.comboBoxRules.addItems(filenames)

    def get_curr_rule(self):
        return self.ui.comboBoxRules.currentText()

    def get_cb_lv0_curr_txt(self):
        return self.ui.comboBoxLv0.currentText()

    def get_cb_lv1_curr_txt(self):
        return self.ui.comboBoxLv1.currentText()

    def get_cb_lv2_curr_txt(self):
        return self.ui.comboBoxLv2.currentText()

    def set_terms_names_cb_lv0(self, names):
        self.ui.comboBoxTermsLv0.clear()
        self.ui.comboBoxTermsLv0.addItems(names)

    def set_terms_names_cb_lv1(self, names):
        self.ui.comboBoxTermsLv1.clear()
        self.ui.comboBoxTermsLv1.addItems(names)

    def set_terms_names_cb_lv2(self, names):
        self.ui.comboBoxTermsLv2.clear()
        self.ui.comboBoxTermsLv2.addItems(names)

    def set_button_state(self, state):
        self.ui.pushButtonRuleAdd.setEnabled(state)

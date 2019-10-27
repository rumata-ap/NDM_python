import copy
from PyQt5 import QtCore, QtWidgets, QtGui
from designer.formLoadsEditor import Ui_FormLoadsCreator
from modules.project import Project
from modules.loads import LoadNDM


class LoadsEditorWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent, QtCore.Qt.Window)
        self.prj: Project = parent.prj
        self.loadsModel = None

        self.form = Ui_FormLoadsCreator()
        ui = self.form
        self.form.setupUi(self)
        ui.pushButtonAddLoadsGroup.clicked.connect(self.on_createLoadsGroup)
        ui.pushButtonAddLoad.clicked.connect(self.on_createLoad)
        ui.cbNumsLoadsGroups.activated.connect(self.on_changeNum)

    def createTableView(self):
        lst = ['c', 'cl', 'n', 'nl']
        idx = self.form.comboBoxLoadsType.currentIndex()

        def on_clickedLoad(ind):
            loads = self.prj.loads[lst[idx]][int(
                self.form.cbNumsLoadsGroups.currentText())]
            self.prj.selectedLoad = loads[ind.row()]
            sell: LoadNDM = loads[ind.row()]
            self.form.doubleSpinBoxN.setValue(sell.N)
            self.form.doubleSpinBoxMx.setValue(sell.Mx)
            self.form.doubleSpinBoxMy.setValue(sell.My)

        model = QtGui.QStandardItemModel()

        loads = self.prj.loads[lst[idx]][int(
            self.form.cbNumsLoadsGroups.currentText())]
        for load in loads:
            L = []
            # load:LoadNDM
            L.append(QtGui.QStandardItem(str(load.N)))
            L.append(QtGui.QStandardItem(str(load.Mx)))
            L.append(QtGui.QStandardItem(str(load.My)))
            L.append(QtGui.QStandardItem(str(load.N_)))
            L.append(QtGui.QStandardItem(str(load.Mx_)))
            L.append(QtGui.QStandardItem(str(load.My_)))

            model.appendRow(L)

        model.setHorizontalHeaderLabels(
            ["N, кН", "Mx, кНм", "My, кНм", "N*, кН", "Mx*, кНм", "My*, кНм"])
        self.form.tableViewLoads.setModel(model)
        self.form.tableViewLoads.clicked["QModelIndex"].connect(on_clickedLoad)
        self.loadsModel = model

    def message(self):
        QtWidgets.QMessageBox.information(self, "Сообщение",
                                          "Невозможно добавить усилие. \nСначала добавьте группу усилий.",
                                          buttons=QtWidgets.QMessageBox.Close,
                                          defaultButton=QtWidgets.QMessageBox.Close)

    @QtCore.pyqtSlot()
    def on_createLoad(self):
        load = LoadNDM()
        load.N = self.form.doubleSpinBoxN.value()
        load.Mx = self.form.doubleSpinBoxMx.value()
        load.My = self.form.doubleSpinBoxMy.value()
        load.N_ = self.form.doubleSpinBoxN.value()
        load.Mx_ = self.form.doubleSpinBoxMx.value()
        load.My_ = self.form.doubleSpinBoxMy.value()

        lst = ['c', 'cl', 'n', 'nl']
        idx = self.form.comboBoxLoadsType.currentIndex()
        if len(self.prj.loads[lst[idx]]) == 0:
            self.message()
        else:
            grp = self.prj.loads[lst[idx]][int(
                self.form.cbNumsLoadsGroups.currentText())]
            grp.append(load)
            self.prj.selectedLoadsGroup = grp
            self.createTableView()

    @QtCore.pyqtSlot()
    def on_createLoadsGroup(self):
        lst = ['c', 'cl', 'n', 'nl']
        idx = self.form.comboBoxLoadsType.currentIndex()

        if len(self.prj.loads[lst[idx]]) == 0:
            self.prj.loads[lst[idx]][1] = []
            self.prj.selectedLoadsGroup = self.prj.loads[lst[idx]][1]
            self.form.cbNumsLoadsGroups.addItem('1')
            self.form.spinBoxNumGroup.stepUp()
        else:
            self.prj.loads[lst[idx]][self.form.spinBoxNumGroup.value()] = [
            ]
            self.prj.selectedLoadsGroup = self.prj.loads[lst[idx]][self.form.spinBoxNumGroup.value(
            )]
            self.form.cbNumsLoadsGroups.addItem(
                self.form.spinBoxNumGroup.text())
            self.form.cbNumsLoadsGroups.setCurrentText(
                self.form.spinBoxNumGroup.text())
            self.createTableView()
            self.form.spinBoxNumGroup.stepUp()

    @QtCore.pyqtSlot()
    def on_changeNum(self):
        lst = ['c', 'cl', 'n', 'nl']
        idx = self.form.comboBoxLoadsType.currentIndex()
        self.prj.selectedLoadsGroup = self.prj.loads[lst[idx]][int(
            self.form.cbNumsLoadsGroups.currentText())]

        self.createTableView()

    def showEvent(self, е):
    
        if self.form.comboBoxLoadsType.currentIndex() == 0:
            lst = ['Расчетные длительные',
                   'Нормативные', 'Нормативные длительные']
            self.form.comboBoxTypeConversion.addItems(lst)
            if len(self.prj.loads['c']) == 0:
                self.form.spinBoxNumGroup.setValue(1)
            else:
                for loadsKey in self.prj.loads['c'].keys():
                    self.form.cbNumsLoadsGroups.addItem(str(loadsKey))

                self.form.spinBoxNumGroup.setValue(
                    len(self.prj.loads['c']) + 1)

        elif self.form.comboBoxLoadsType.currentIndex() == 1:
            lst = ['Расчетные', 'Нормативные', 'Нормативные длительные']
            self.form.comboBoxTypeConversion.addItems(lst)
            if len(self.prj.loads['cl']) == 0:
                self.form.spinBoxNumGroup.setValue(1)
            else:
                for loadsKey in self.prj.loads['cl'].keys():
                    self.form.cbNumsLoadsGroups.addItem(str(loadsKey))

                self.form.spinBoxNumGroup.setValue(
                    len(self.prj.loads['cl']) + 1)

        elif self.form.comboBoxLoadsType.currentIndex() == 2:
            lst = ['Расчетные', 'Расчетные длительные',
                   'Нормативные длительные']
            self.form.comboBoxTypeConversion.addItems(lst)
            if len(self.prj.loads['n']) == 0:
                self.form.spinBoxNumGroup.setValue(1)
            else:
                for loadsKey in self.prj.loads['n'].keys():
                    self.form.cbNumsLoadsGroups.addItem(str(loadsKey))

                self.form.spinBoxNumGroup.setValue(
                    len(self.prj.loads['n']) + 1)

        elif self.form.comboBoxLoadsType.currentIndex() == 3:
            lst = ['Расчетные', 'Расчетные длительные', 'Нормативные']
            self.form.comboBoxTypeConversion.addItems(lst)
            if len(self.prj.loads['nl']) == 0:
                self.form.spinBoxNumGroup.setValue(1)
            else:
                for loadsKey in self.prj.loads['nl'].keys():
                    self.form.cbNumsLoadsGroups.addItem(str(loadsKey))

                self.form.spinBoxNumGroup.setValue(
                    len(self.prj.loads['nl']) + 1)

        QtWidgets.QWidget.showEvent(self, е)

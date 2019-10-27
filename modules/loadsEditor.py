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

    def showEvent(self, е):

        if self.form.comboBoxLoadsType.currentIndex() == 0:
            
            if len(self.prj.loads['c']) == 0:
                self.form.spinBoxNumGroup.setValue(1)
            else:
                for loadsKey in self.prj.loads['c'].keys():
                    self.form.cbNumsLoadsGroups.addItem(str(loadsKey))

                self.form.spinBoxNumGroup.setValue(
                    len(self.prj.loads['c']) + 1)

        elif self.form.comboBoxLoadsType.currentIndex() == 1:
            if len(self.prj.loads['cl']) == 0:
                self.form.spinBoxNumGroup.setValue(1)
            else:
                for loadsKey in self.prj.loads['cl'].keys():
                    self.form.cbNumsLoadsGroups.addItem(str(loadsKey))

                self.form.spinBoxNumGroup.setValue(
                    len(self.prj.loads['cl']) + 1)

        elif self.form.comboBoxLoadsType.currentIndex() == 2:
            if len(self.prj.loads['n']) == 0:
                self.form.spinBoxNumGroup.setValue(1)
            else:
                for loadsKey in self.prj.loads['n'].keys():
                    self.form.cbNumsLoadsGroups.addItem(str(loadsKey))

                self.form.spinBoxNumGroup.setValue(
                    len(self.prj.loads['n']) + 1)

        elif self.form.comboBoxLoadsType.currentIndex() == 3:
            if len(self.prj.loads['nl']) == 0:
                self.form.spinBoxNumGroup.setValue(1)
            else:
                for loadsKey in self.prj.loads['nl'].keys():
                    self.form.cbNumsLoadsGroups.addItem(str(loadsKey))

                self.form.spinBoxNumGroup.setValue(
                    len(self.prj.loads['nl']) + 1)
        
        QtWidgets.QWidget.showEvent(self, е)

    def createTableView(self):
       
        model = QtGui.QStandardItemModel()
        for load in self.prj.selectedLoadsGroup:
            L = []
            #load:LoadNDM
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
        self.loadsModel = model

    def message(self):
        QtWidgets.QMessageBox.information(self, "Сообщение",
                                            "Невозможно добавить усилие. \n Сначала создайте группу усилий.",
                                            buttons=QtWidgets.QMessageBox.Close,
                                            defaultButton=QtWidgets.QMessageBox.Close)

    @QtCore.pyqtSlot()
    def on_createLoad(self):
        load = LoadNDM()
        load.N = self.form.doubleSpinBoxN.value()
        load.Mx = self.form.doubleSpinBoxMx.value()
        load.My = self.form.doubleSpinBoxMy.value()
        load.N_ = 0.
        load.Mx_ = 0.
        load.My_ = 0.
        
        if self.form.comboBoxLoadsType.currentIndex() == 0:
            if len(self.prj.loads['c']) == 0:
                self.message()
            else:
                grp = self.prj.loads['c'][int(self.form.cbNumsLoadsGroups.currentText())]
                grp.append(load)
                self.prj.selectedLoadsGroup = grp
                self.createTableView()

        elif self.form.comboBoxLoadsType.currentIndex() == 1:
            if len(self.prj.loads['cl']) == 0:
                self.message()
            else:
                grp = self.prj.loads['cl'][int(self.form.cbNumsLoadsGroups.currentText())]
                grp.append(load)
                self.prj.selectedLoadsGroup = grp
                self.createTableView()

        elif self.form.comboBoxLoadsType.currentIndex() == 2:
            if len(self.prj.loads['n']) == 0:
                self.message()
            else:
                grp = self.prj.loads['n'][int(self.form.cbNumsLoadsGroups.currentText())]
                grp.append(load)
                self.prj.selectedLoadsGroup = grp
                self.createTableView()

        elif self.form.comboBoxLoadsType.currentIndex() == 2:
            if len(self.prj.loads['nl']) == 0:
                self.message()
            else:
                grp = self.prj.loads['nl'][int(self.form.cbNumsLoadsGroups.currentText())]
                grp.append(load)
                self.prj.selectedLoadsGroup = grp
                self.createTableView()


    @QtCore.pyqtSlot()
    def on_createLoadsGroup(self):
        
        if self.form.comboBoxLoadsType.currentIndex() == 0:
            if len(self.prj.loads['c']) == 0:
                self.prj.loads['c'][1] = []
                self.prj.selectedLoadsGroup = self.prj.loads['c'][1]
                self.form.cbNumsLoadsGroups.addItem('1')
                self.form.spinBoxNumGroup.stepUp()
            else:
                self.prj.loads['c'][self.form.spinBoxNumGroup.value()] = []
                self.prj.selectedLoadsGroup = self.prj.loads['c'][self.form.spinBoxNumGroup.value(
                )]
                self.form.cbNumsLoadsGroups.addItem(self.form.spinBoxNumGroup.text())
                self.form.spinBoxNumGroup.stepUp()
        elif self.form.comboBoxLoadsType.currentIndex() == 1:
            if len(self.prj.loads['cl']) == 0:
                self.prj.loads['cl'][1] = []
                self.prj.selectedLoadsGroup = self.prj.loads['cl'][1]
                self.form.cbNumsLoadsGroups.addItem('1')
                self.form.spinBoxNumGroup.stepUp()
            else:
                self.prj.loads['cl'][self.form.spinBoxNumGroup.value()] = []
                self.prj.selectedLoadsGroup = self.prj.loads['cl'][self.form.spinBoxNumGroup.value(
                )]
                self.form.cbNumsLoadsGroups.addItem(
                    self.form.spinBoxNumGroup.text())
                self.form.spinBoxNumGroup.stepUp()
        elif self.form.comboBoxLoadsType.currentIndex() == 2:
            if len(self.prj.loads['n']) == 0:
                self.prj.loads['n'][1] = []
                self.prj.selectedLoadsGroup = self.prj.loads['n'][1]
                self.form.cbNumsLoadsGroups.addItem('1')
                self.form.spinBoxNumGroup.stepUp()
            else:
                self.prj.loads['n'][self.form.spinBoxNumGroup.value()] = []
                self.prj.selectedLoadsGroup = self.prj.loads['n'][self.form.spinBoxNumGroup.value(
                )]
                self.form.cbNumsLoadsGroups.addItem(
                    self.form.spinBoxNumGroup.text())
                self.form.spinBoxNumGroup.stepUp()
        elif self.form.comboBoxLoadsType.currentIndex() == 3:
            if len(self.prj.loads['nl']) == 0:
                self.prj.loads['nl'][1] = []
                self.prj.selectedLoadsGroup = self.prj.loads['nl'][1]
                self.form.cbNumsLoadsGroups.addItem('1')
                self.form.spinBoxNumGroup.stepUp()
            else:
                self.prj.loads['nl'][self.form.spinBoxNumGroup.value()] = []
                self.prj.selectedLoadsGroup = self.prj.loads['nl'][self.form.spinBoxNumGroup.value(
                )]
                self.form.cbNumsLoadsGroups.addItem(self.form.spinBoxNumGroup.text())
                self.form.spinBoxNumGroup.stepUp()

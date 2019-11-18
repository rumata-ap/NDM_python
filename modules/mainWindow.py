# -*- coding: utf-8 -*-
import sys
import copy
import pickle
from PyQt5 import QtCore, QtWidgets, QtGui
from designer.formMainWindow import Ui_MainWindow
from modules.project import Project
from modules.betonSelector import BetonEditorWindow
from modules.armSelector import ArmEditorWindow
from modules.rectContourWindow import RectContourWindow
from modules.loadsEditor import LoadsEditorWindow

w = None


class MyWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.label = QtWidgets.QLabel("Содержимое страницы")
        self.button = QtWidgets.QPushButton("Кнопка")
        self.box = QtWidgets.QVBoxLayout()
        self.box.addWidget(self.label)
        self.box.addWidget(self.button)
        self.setLayout(self.box)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.prj: Project = Project('temp')
        self.loadsModel = None
        self.betonsModel = None
        self.armsModel = None

        self.form = Ui_MainWindow()
        ui = self.form
        ui.setupUi(self)
        ui.actionNew.triggered.connect(self.on_new)
        ui.actionOpen.triggered.connect(self.on_open)
        ui.actionSave.triggered.connect(self.on_save)
        ui.actionSaveAs.triggered.connect(self.on_saveas)
        ui.actionQuit.triggered.connect(self.on_quit)
        ui.actionAddBeton.triggered.connect(self.on_createBeton)
        ui.actionAddArm.triggered.connect(self.on_createArm)
        ui.actionViewTableMaterials.triggered.connect(self.createMaterialsView)
        ui.actionViewTableLoads.triggered.connect(self.createLoadsView)
        ui.actionAddContourRect.triggered.connect(self.on_createRectContour)
        ui.actionAddLoadsC.triggered.connect(self.on_loadsEditorC)
        ui.actionAddLoadsCL.triggered.connect(self.on_loadsEditorCL)
        ui.actionAddLoadsN.triggered.connect(self.on_loadsEditorN)
        ui.actionAddLoadsNL.triggered.connect(self.on_loadsEditorNL)

    @QtCore.pyqtSlot()
    def on_createRectContour(self):
        w = RectContourWindow(self)
        w.show()

    @QtCore.pyqtSlot()
    def on_loadsEditorC(self):
        w = LoadsEditorWindow(self)
        w.form.comboBoxLoadsType.setEnabled(False)
        w.show()

    @QtCore.pyqtSlot()
    def on_loadsEditorCL(self):
        w = LoadsEditorWindow(self)
        w.form.comboBoxLoadsType.setCurrentIndex(1)
        w.form.comboBoxLoadsType.setEnabled(False)
        w.show()

    @QtCore.pyqtSlot()
    def on_loadsEditorN(self):
        w = LoadsEditorWindow(self)
        w.form.comboBoxLoadsType.setCurrentIndex(2)
        w.form.comboBoxLoadsType.setEnabled(False)
        w.show()

    @QtCore.pyqtSlot()
    def on_loadsEditorNL(self):
        w = LoadsEditorWindow(self)
        w.form.comboBoxLoadsType.setCurrentIndex(3)
        w.form.comboBoxLoadsType.setEnabled(False)
        w.show()

    @QtCore.pyqtSlot()
    def on_open(self):
        f = QtWidgets.QFileDialog.getOpenFileName(parent=self, caption=" Открыть проект ",
                                                  filter="All (*) ;;NDMProjects (*.ndm) ",
                                                  initialFilter="NDMProjects (*.ndm)")
        if f[0] == '' or type(f[0]) == None:
            return

        with open(f[0], "rb") as file:
            self.prj = pickle.load(file)

        #self.prj = Project(f[0])
        print("Открыт проект " + f[0])
        self.statusBar().showMessage(f[0])

    @QtCore.pyqtSlot()
    def on_new(self):
        result = QtWidgets.QMessageBox.warning(self, "Внимание",
                                               "Сохранить внесенные изменения в текущий проект?",
                                               buttons=QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No |
                                               QtWidgets.QMessageBox.Cancel,
                                               defaultButton=QtWidgets.QMessageBox.Cancel)
        if result == 16384:
            self.on_save()

        file = QtWidgets.QFileDialog.getSaveFileName(parent=self, caption=" Создать проект ",
                                                     filter="All (*) ;;NDMProjects (*.ndm) ",
                                                     initialFilter="NDMProjects (*.ndm)")

        if file[0] == '' or type(file[0]) == None:
            return

        self.prj = Project(file[0])
        print("Создан новый проект " + file[0])

    @QtCore.pyqtSlot()
    def on_save(self):

        if self.prj.name == 'temp' or self.prj.name == '':
            file = QtWidgets.QFileDialog.getSaveFileName(parent=self, caption=" Сохранить проект ",
                                                         filter="All (*) ;;NDMProjects (*.ndm) ",
                                                         initialFilter="NDMProjects (*.ndm)")
            if file[0] == '' or type(file[0]) == None:
                return

            self.prj.name = file[0]
            with open(self.prj.name, "wb") as file:
                pickle.dump(self.prj, file)
            print("Текущий проект сохранен " + self.prj.name)
        else:
            with open(self.prj.name, "wb") as file:
                pickle.dump(self.prj, file)
            print("Текущий проект сохранен " + self.prj.name)

    @QtCore.pyqtSlot()
    def on_saveas(self):
        file = QtWidgets.QFileDialog.getSaveFileName(parent=self, caption=" Сохранить проект ",
                                                     filter="All (*) ;;NDMProjects (*.ndm) ",
                                                     initialFilter="NDMProjects (*.ndm)")

        if file[0] == '' or type(file[0]) == None:
            return

        self.prj.name = file[0]
        with open(self.prj.name, "wb") as file:
            pickle.dump(self.prj, file, protocol=4)
        print("Текущий проект сохранен как " + self.prj.name)

    @QtCore.pyqtSlot()
    def on_quit(self):
        result = QtWidgets.QMessageBox.warning(self, "Внимание!",
                                               "Вы закрываете приложение без сохранения введенных данных \nСохранить внесенные изменения в текущий проект?",
                                               buttons=QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               defaultButton=QtWidgets.QMessageBox.No)
        if result == 16384:
            self.on_save()
        QtWidgets.qApp.quit()

    def on_clicked(self):
        result = QtWidgets.QMessageBox.warning(self, "Внимание",
                                               "Сохранить внесенные изменения в текущий проект?",
                                               buttons=QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No |
                                               QtWidgets.QMessageBox.Cancel,
                                               defaultButton=QtWidgets.QMessageBox.Cancel)
        print(result)

    def on_createBeton(self):
        w = BetonEditorWindow(self)
        w.show()

    def createBetonsModel(self):
        model = QtGui.QStandardItemModel()
        # model.setRowCount(len(self.materials['b']))
        # model.setColumnCount(5)
        v = ["Ниже 40%", "40% - 75%", "Выше 75%"]
        d = ['Трехлинейная', 'Двухлинейная']

        for bet in self.prj.materials['b'].values():
            L = []
            L.append(QtGui.QStandardItem(str(bet.number)))
            L.append(QtGui.QStandardItem('B'+str(bet.classB)))
            L.append(QtGui.QStandardItem(d[bet.type-1]))
            L.append(QtGui.QStandardItem(v[bet.vlag-1]))
            L.append(QtGui.QStandardItem(str(bet.gamma_b_3)))
            L.append(QtGui.QStandardItem(bet.descript))
            model.appendRow(L)

        model.setHorizontalHeaderLabels(
            ["№", "Класс", "Диаграмма", "Среда", "γb3", "Описание"])
        self.betonsModel = model

    def createArmsModel(self):
        model = QtGui.QStandardItemModel()
        for arm in self.prj.materials['a'].values():
            L = []
            L.append(QtGui.QStandardItem(str(arm.number)))
            L.append(QtGui.QStandardItem(arm.classA))
            L.append(QtGui.QStandardItem(str(arm.gamma_s)))
            L.append(QtGui.QStandardItem(arm.descript))
            model.appendRow(L)

        model.setHorizontalHeaderLabels(
            ["№", "Класс", "γs", "Описание"])
        self.armsModel = model

    @QtCore.pyqtSlot()
    def createMaterialsView(self):
        def on_clickedBet(ind):
            bts = list(self.prj.materials['b'].values())
            self.prj.selectedBeton = bts[ind.row()]

        def on_clickedArm(ind):
            arms = list(self.prj.materials['a'].values())
            self.prj.selectedArm = arms[ind.row()]
        self.createBetonsModel()
        self.createArmsModel()
        ui = self.form
        ui.tableViewBeton.setModel(self.betonsModel)
        ui.tableViewBeton.clicked["QModelIndex"].connect(on_clickedBet)
        ui.tableViewArm.setModel(self.armsModel)
        ui.tableViewArm.clicked["QModelIndex"].connect(on_clickedArm)
        hHeader = ui.tableViewBeton.horizontalHeader()
        hHeader.setHighlightSections(True)
        hHeader = ui.tableViewArm.horizontalHeader()
        # hHeader.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        hHeader.setHighlightSections(True)
        ui.stackedWidget.setCurrentIndex(1)

    @QtCore.pyqtSlot()
    def createLoadsView(self):
        modelC = QtGui.QStandardItemModel()
        modelCL = QtGui.QStandardItemModel()
        modelN = QtGui.QStandardItemModel()
        modelNL = QtGui.QStandardItemModel()
        modelC.setHorizontalHeaderLabels(
            ['Группа', "N, кН", "Mx, кНм", "My, кНм", "N*, кН", "Mx*, кНм", "My*, кНм"])
        modelCL.setHorizontalHeaderLabels(
            ['Группа', "N, кН", "Mx, кНм", "My, кНм", "N*, кН", "Mx*, кНм", "My*, кНм"])
        modelN.setHorizontalHeaderLabels(
            ['Группа', "N, кН", "Mx, кНм", "My, кНм", "N*, кН", "Mx*, кНм", "My*, кНм"])
        modelNL.setHorizontalHeaderLabels(
            ['Группа', "N, кН", "Mx, кНм", "My, кНм", "N*, кН", "Mx*, кНм", "My*, кНм"])

        loadsGrp = list(self.prj.loads['c'].values())
        loadsGrpKeys = list(self.prj.loads['c'].keys())
        i = 0
        for loads in loadsGrp:
            for load in loads:
                L = []
                # load:LoadNDM
                L.append(QtGui.QStandardItem(str(loadsGrpKeys[i])))
                L.append(QtGui.QStandardItem(str(load.N)))
                L.append(QtGui.QStandardItem(str(load.Mx)))
                L.append(QtGui.QStandardItem(str(load.My)))
                L.append(QtGui.QStandardItem(str(load.N_)))
                L.append(QtGui.QStandardItem(str(load.Mx_)))
                L.append(QtGui.QStandardItem(str(load.My_)))
                modelC.appendRow(L)
            i = i + 1

        loadsGrp = list(self.prj.loads['cl'].values())
        loadsGrpKeys = list(self.prj.loads['cl'].keys())
        i = 0
        for loads in loadsGrp:
            for load in loads:
                L = []
                # load:LoadNDM
                L.append(QtGui.QStandardItem(str(loadsGrpKeys[i])))
                L.append(QtGui.QStandardItem(str(load.N)))
                L.append(QtGui.QStandardItem(str(load.Mx)))
                L.append(QtGui.QStandardItem(str(load.My)))
                L.append(QtGui.QStandardItem(str(load.N_)))
                L.append(QtGui.QStandardItem(str(load.Mx_)))
                L.append(QtGui.QStandardItem(str(load.My_)))
                modelCL.appendRow(L)
            i = i + 1

        loadsGrp = list(self.prj.loads['n'].values())
        loadsGrpKeys = list(self.prj.loads['n'].keys())
        i = 0
        for loads in loadsGrp:
            for load in loads:
                L = []
                # load:LoadNDM
                L.append(QtGui.QStandardItem(str(loadsGrpKeys[i])))
                L.append(QtGui.QStandardItem(str(load.N)))
                L.append(QtGui.QStandardItem(str(load.Mx)))
                L.append(QtGui.QStandardItem(str(load.My)))
                L.append(QtGui.QStandardItem(str(load.N_)))
                L.append(QtGui.QStandardItem(str(load.Mx_)))
                L.append(QtGui.QStandardItem(str(load.My_)))
                modelN.appendRow(L)
            i = i + 1

        loadsGrp = list(self.prj.loads['nl'].values())
        loadsGrpKeys = list(self.prj.loads['nl'].keys())
        i = 0
        for loads in loadsGrp:
            for load in loads:
                L = []
                # load:LoadNDM
                L.append(QtGui.QStandardItem(str(loadsGrpKeys[i])))
                L.append(QtGui.QStandardItem(str(load.N)))
                L.append(QtGui.QStandardItem(str(load.Mx)))
                L.append(QtGui.QStandardItem(str(load.My)))
                L.append(QtGui.QStandardItem(str(load.N_)))
                L.append(QtGui.QStandardItem(str(load.Mx_)))
                L.append(QtGui.QStandardItem(str(load.My_)))
                modelNL.appendRow(L)
            i = i + 1        
        
        ui = self.form
        ui.tableViewC.setModel(modelC)
        ui.tableViewCL.setModel(modelCL)
        ui.tableViewN.setModel(modelN)
        ui.tableViewNL.setModel(modelNL)
        ui.stackedWidget.setCurrentIndex(2)

    @QtCore.pyqtSlot()
    def on_createArm(self):
        w = ArmEditorWindow(self)
        w.show()

    @QtCore.pyqtSlot()
    def on_editArm(self):
        w = ArmEditorWindow(self)
        w.setWindowModality(QtCore.Qt.WindowModal)
        w.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        w.setFixedWidth(300)
        w.show()

    @QtCore.pyqtSlot()
    def on_settings(self):
        pass

        # def add_tool_bar(self):
    #     self.toolBar = QtWidgets.QToolBar("MyToolBar")
    #     ico = self.style().standardIcon(
    #         QtWidgets.QStyle.SP_MessageBoxCritical)
    #     self.actClose = self.toolBar.addAction(ico, "Close",
    #                                            QtWidgets.qApp.quit)
    #     self.actClose.setShortcut(QtGui.QKeySequence.Close)
    #     self.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
    #     #self.addToolBarBreak(QtCore.Qt.TopToolBarArea)
    #     self.toolBar2 = QtWidgets.QToolBar("MyToolBar2")
    #     ico2 = self.style().standardIcon(
    #         QtWidgets.QStyle.SP_DialogCloseButton)
    #     self.actQuit = self.toolBar2.addAction(ico2, "Quit",
    #                                            QtWidgets.qApp.quit)
    #     self.actQuit.setShortcut(QtGui.QKeySequence.Quit)
    #     #self.insertToolBar(self.toolBar, self.toolBar2)
    #     self.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar2)
    #     #self.insertToolBarBreak(self.toolBar2)

    # def add_dock_widget(self):
    #     self.dw = QtWidgets.QDockWidget("MyDockWidget1")
    #     self.lbl = QtWidgets.QLabel("Содержимое панели 1")
    #     self.lbl.setWordWrap(True)
    #     self.lbl.setFrameStyle(
    #         QtWidgets.QFrame.Box | QtWidgets.QFrame.Plain)
    #     self.dw.setWidget(self.lbl)
    #     self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.dw)

    #     self.dw2 = QtWidgets.QDockWidget("MyDockWidget2")
    #     self.lbl2 = QtWidgets.QLabel("Содержимое панели 2")
    #     self.lbl2.setWordWrap(True)
    #     self.lbl2.setFrameStyle(
    #         QtWidgets.QFrame.Box | QtWidgets.QFrame.Plain)
    #     self.dw2.setWidget(self.lbl2)
    #     self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.dw2,
    #                        QtCore.Qt.Vertical)

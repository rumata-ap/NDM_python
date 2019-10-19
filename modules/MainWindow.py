# -*- coding: utf-8 -*-
import sys
import copy
import pickle
from PyQt5 import QtCore, QtWidgets, QtGui
from modules.project import Project
from modules.betonSelector import BetonCreator, BetonEditor
from modules.armSelector import ArmCreator, ArmEditor

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

class MyWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.prj: Project = Project('temp')
        self.w = MyWidget()
        self.setCentralWidget(self.w)
        self.w.button.clicked.connect(self.on_clicked)
        self.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.setIconSize(QtCore.QSize(32, 32))
        self.setWindowTitle("Concrete Organizer")
        # self.setAnimated(False)
        self.setDockOptions(QtWidgets.QMainWindow.AnimatedDocks |
                            QtWidgets.QMainWindow.AllowTabbedDocks)
        self.setTabPosition(QtCore.Qt.LeftDockWidgetArea,
                            QtWidgets.QTabWidget.North)
        self.setTabPosition(QtCore.Qt.RightDockWidgetArea,
                            QtWidgets.QTabWidget.North)
        self.setTabShape(QtWidgets.QTabWidget.Triangular)
        self.add_menu()
        # self.add_tool_bar()
        # self.add_dock_widget()
        self.statusBar().showMessage("Текст в строке состояния")

    def add_menu(self):
        self.menuFile = QtWidgets.QMenu("&Файл")
        self.actNew = QtWidgets.QAction("Создать", None)
        self.actNew.setShortcut(QtGui.QKeySequence.New)
        self.actNew.triggered.connect(self.on_new)
        self.actOpen = QtWidgets.QAction("Открыть", None)
        self.actOpen.setShortcut(QtGui.QKeySequence.Open)
        self.actOpen.triggered.connect(self.on_open)
        self.actSave = QtWidgets.QAction("Сохранить", None)
        self.actSave.setShortcut(QtGui.QKeySequence.Save)
        self.actSave.triggered.connect(self.on_save)
        self.actSaveAs = QtWidgets.QAction("Сохранить как", None)
        self.actSaveAs.setShortcut(QtGui.QKeySequence.SaveAs)
        self.actSaveAs.triggered.connect(self.on_saveas)
        self.actSettings = QtWidgets.QAction("Параметры", None)
        self.actSettings.triggered.connect(self.on_settings)
        self.actExit = QtWidgets.QAction("Выход", None)
        self.actExit.setShortcut(QtGui.QKeySequence.Quit)
        self.actExit.triggered.connect(self.on_quit)

        self.menuFile.addAction(self.actNew)
        self.menuFile.addAction(self.actOpen)
        self.menuFile.addAction(self.actSave)
        self.menuFile.addAction(self.actSaveAs)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actSettings)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actExit)

        self.menuMaterials = QtWidgets.QMenu("&Материалы")
        self.menuBeton = self.menuMaterials.addMenu('Бетон')
        self.menuArm = self.menuMaterials.addMenu('Арматура')
        # self.menuMaterials.addAction(self.actGroupBeton)

        self.actNewBeton = QtWidgets.QAction("Добавить бетон")
        self.actNewBeton.triggered.connect(self.on_createBeton)
        self.menuBeton.addAction(self.actNewBeton)
        self.actEditBeton = QtWidgets.QAction("Изменить бетон")
        self.actEditBeton.triggered.connect(self.on_editBeton)
        self.menuBeton.addAction(self.actEditBeton)

        self.actNewArm = QtWidgets.QAction("Добавить арматуру")
        self.actNewArm.triggered.connect(self.on_createArm)
        self.menuArm.addAction(self.actNewArm)
        self.actEditArm = QtWidgets.QAction("Изменить арматуру")
        self.actEditArm.triggered.connect(self.on_editArm)
        self.menuArm.addAction(self.actEditArm)
        
        self.menuMaterials.addSeparator()
        self.actTables = QtWidgets.QAction("Таблицы")
        self.menuMaterials.addAction(self.actTables)

        self.menuImport = QtWidgets.QMenu("&Импорт")
        self.menuElems = QtWidgets.QMenu("&Элементы")
        self.menuFes = QtWidgets.QMenu("&Участки")
        self.menuSect = QtWidgets.QMenu("&Поперечные сечения")
        self.menuCrackResist = QtWidgets.QMenu("&Трещиностойкость")
        self.menuHelp = QtWidgets.QMenu("&Помощь")

        self.menuBar().addMenu(self.menuFile)
        self.menuBar().addMenu(self.menuMaterials)
        self.menuBar().addMenu(self.menuImport)
        self.menuBar().addMenu(self.menuElems)
        self.menuBar().addMenu(self.menuFes)
        self.menuBar().addMenu(self.menuSect)
        self.menuBar().addMenu(self.menuCrackResist)
        self.menuBar().addMenu(self.menuHelp)

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
        w = BetonCreator(self.prj, self)
        w.setWindowModality(QtCore.Qt.WindowModal)
        w.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        w.setFixedWidth(300)
        w.show()

    def on_editBeton(self):
        w = BetonEditor(self.prj, self)
        w.setWindowModality(QtCore.Qt.WindowModal)
        w.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        w.setFixedWidth(300)
        w.show()

    def on_createArm(self):
        w = ArmCreator(self.prj, self)
        w.setWindowModality(QtCore.Qt.WindowModal)
        w.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        w.setFixedWidth(300)
        w.show()

    def on_editArm(self):
        w = ArmEditor(self.prj, self)
        w.setWindowModality(QtCore.Qt.WindowModal)
        w.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        w.setFixedWidth(300)
        w.show()

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

import copy
from PyQt5 import QtCore, QtWidgets, QtGui
from designer.formRectContour import Ui_FormRectContour
from modules.project import Project
from modules.crossects import Node, Contour


class RectContourWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent, QtCore.Qt.Window)
        self.prj: Project = parent.prj
        self.pointsModel = None

        self.form = Ui_FormRectContour()
        ui = self.form
        ui.setupUi(self)
        ui.pushButtonAdd.clicked.connect(self.on_add)
        ui.pushButtonDel.clicked.connect(self.on_del)
        ui.comboBoxNums.activated.connect(self.on_changeNum)
        if len(self.prj.contours) > 0:
            ui.spinBoxNum.setValue(len(self.prj.contours) + 1)
            for cntr in self.prj.contours.values():
                ui.comboBoxNums.addItem(str(cntr.num))

    def createTableView(self, nds):
        model = QtGui.QStandardItemModel()
        ui = self.form
        for pt in nds:
            L = []
            L.append(QtGui.QStandardItem(str(pt.id)))
            L.append(QtGui.QStandardItem(str(pt.X)))
            L.append(QtGui.QStandardItem(str(pt.Y)))

            model.appendRow(L)

        model.setHorizontalHeaderLabels(["№", "X", "Y"])
        ui.tableViewPointsContour.setModel(model)
        self.pointsModel = model

    def createGraphicsView(self, b, h):
        ui = self.form
        s: QtCore.QSize = ui.graphicsView.size()
        hv = s.height()
        bv = s.width()

        scale = min([(bv-20) / b, (hv-20) / h])

        scene = QtWidgets.QGraphicsScene(10.0, 10.0, b*scale, h*scale)
        scene.setBackgroundBrush(QtCore.Qt.white)

        rect = scene.addRect(QtCore.QRectF(0.0, 0.0, b*scale, h*scale),
                             pen=QtGui.QPen(QtCore.Qt.blue, 3),
                             brush=QtGui.QBrush(QtCore.Qt.white))
        rect.setPos(QtCore.QPointF(10, 10))

        ui.graphicsView.setScene(scene)

    @QtCore.pyqtSlot()
    def on_add(self):
        ui = self.form
        b = float(ui.spinBoxB.value())
        h = float(ui.spinBoxH.value())
        nds = [Node(1, b / 2, -h / 2), Node(2, b / 2, h / 2),
               Node(3, -b / 2, h / 2), Node(4, -b / 2, -h / 2)]

        self.createTableView(nds)
        self.createGraphicsView(b, h)

        contour = Contour(ui.spinBoxNum.value(), nds)
        contour.attr['type'] = 'rect'
        contour.attr['b'] = b
        contour.attr['h'] = h
        ui.comboBoxNums.addItem(ui.spinBoxNum.text())

        self.prj.contours[ui.spinBoxNum.value()] = contour
        ui.spinBoxNum.stepUp()

    @QtCore.pyqtSlot()
    def on_changeNum(self):
        contour: Contour = self.prj.contours[int(
            self.form.comboBoxNums.currentText())]
        nds = contour.nodes
        b = contour.attr['b']
        h = contour.attr['h']
        self.createTableView(nds)
        self.createGraphicsView(b, h)
        self.form.spinBoxB.setValue(int(b))
        self.form.spinBoxH.setValue(int(h))

    @QtCore.pyqtSlot()
    def on_del(self):
        if self.prj.contours.__len__() == 0: return
        idx = int(self.form.comboBoxNums.currentText())
        del self.prj.contours[idx]
        self.form.comboBoxNums.clear()
        for cntr in self.prj.contours.values():
            self.form.comboBoxNums.addItem(str(cntr.num))


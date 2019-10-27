# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets, QtGui, QtCore
import sys


def on_activated(ind):
    print("on_activated", ind.data())


def on_clicked(ind: QtCore.QModelIndex):
    print("on_clicked", ind.row())


def on_double_clicked(ind):
    print("on_double_clicked", ind.data())


def on_entered(ind):
    print("on_entered", ind.data())


def on_pressed(ind):
    print("on_pressed", ind.data())


def on_viewport_entered():
    print("on_viewport_entered")


app = QtWidgets.QApplication(sys.argv)
window = QtWidgets.QWidget()
window.setWindowTitle("Класс QTableView")
window.resize(500, 200)

view = QtWidgets.QTableView()

model = QtGui.QStandardItemModel(4, 4)
for row in range(0, 4):
    for column in range(0, 4):
        item = QtGui.QStandardItem("({0}, {1})".format(row, column))
        model.setItem(row, column, item)
view.setModel(model)

view.activated["QModelIndex"].connect(on_activated)
view.clicked["QModelIndex"].connect(on_clicked)
view.doubleClicked["QModelIndex"].connect(on_double_clicked)
view.entered["QModelIndex"].connect(on_entered)
view.pressed["QModelIndex"].connect(on_pressed)
view.viewportEntered.connect(on_viewport_entered)
view.setMouseTracking(True)

box = QtWidgets.QVBoxLayout()
box.addWidget(view)
window.setLayout(box)
window.show()
sys.exit(app.exec_())

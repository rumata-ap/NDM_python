# -*- coding: utf-8 -*-
import sys, copy, pickle
from PyQt5 import QtCore, QtWidgets, QtGui
#from modules.project import Project
from modules.MainWindow import MyWindow
#ptj = Project('tmp')



if __name__=='__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    #window.setWindowTitle("Класс QMainWindow")
    window.resize(680, 70)

    window.show()
    sys.exit(app.exec_())

# %%

import sys
import pandas as pd
import numpy as np
import itertools as it
import openpyxl as xl
from PyQt5 import QtCore, QtWidgets

# %%


def ExcelOFDs():
    app = QtWidgets.QApplication(sys.argv)
    arr, l = QtWidgets.QFileDialog.getOpenFileNames(parent=None,
                                                    caption="Заголовок окна", directory=QtCore.QDir.currentPath(),
                                                    filter="Excel (*.xlsx);;Excel (*.xls);;Текст (*.csv);;All (*)")
    return arr

# %%


def ExcelOFD():
    app = QtWidgets.QApplication(sys.argv)
    arr, l = QtWidgets.QFileDialog.getOpenFileNames(parent=None,
                                                    caption="Заголовок окна", directory=QtCore.QDir.currentPath(),
                                                    filter="Excel (*.xlsx);;Excel (*.xls);;Текст (*.csv);;All (*)")
    return arr

# %%


class LiraParser:
    @staticmethod
    def RSU_xls2csv(pathes: list):
        for path in pathes:
            rsu = pd.read_excel(path)
            rsu = rsu.drop([0, 1])
            rsu.columns = ['Element', 'Sect', 'Col', 'Seism',
                           'GroupRSU', 'Crit', 'N', 'Mk', 'My', 'Qz', 'Mz', 'Qy', 'Loads']
            tmp = []
            for i in rsu.Loads:
                j = i.replace('\xa0', '')
                j = j.strip()
                tmp.append(j)
            rsu.Loads = tmp

            spath = str(path).replace('.xls', '.csv')
            rsu.to_csv(spath, ';', encoding="utf-8", index=False)
        print('Файлы преобразованы')

    @staticmethod
    def getBarsRSU():
        pathes = ExcelOFD()
        rsu = {}
        for path in pathes:
            wb = xl.load_workbook(path)
            ws = wb.active
            columns = list(ws.values)[2]
            ws.delete_rows(0, 3)
            df = pd.DataFrame(ws.values)
            df.columns = columns
            name = str(path).split('/')
            name.reverse()
            name = name[0].split('.')
            rsu[name[0]] = df
        #print(rsu)
        return rsu

    @staticmethod
    def getShellsRSU(parameter_list):
        pass


# %%
# LiraParser.RSU_xls2csv(['C_rsu.xls'])


# %%

# app = QtWidgets.QApplication(sys.argv)
# window = QtWidgets.QWidget()
# window.setWindowTitle("Преобразователь таблиц")
# #window.resize(300, 70)

# button = QtWidgets.QPushButton("Отобразить диалоговое окно...")
# button.clicked.connect(on_clicked)

# box = QtWidgets.QVBoxLayout()
# box.addWidget(button)
# window.setLayout(box)
# window.show()

# sys.exit(app.exec_())

# %%
if __name__ == '__main__':
    LiraParser.getBarsRSU()

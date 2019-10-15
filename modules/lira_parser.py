#%%

import pandas as pd
import numpy as np
from PyQt5 import QtCore, QtWidgets
import sys

#%%

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
                j=i.replace('\xa0','')
                j=j.strip()
                tmp.append(j)
            rsu.Loads = tmp
           
            spath = str(path).replace('.xls','.csv')
            rsu.to_csv(spath, ';', encoding="utf-8", index=False)
        print('Файлы преобразованы')

    @staticmethod
    def getBarsRSU(parameter_list):
        pass

    @staticmethod
    def getShellsRSU(parameter_list):
        pass
    
    

#%%
#LiraParser.RSU_xls2csv(['C_rsu.xls'])


#%%


def on_clicked():
    app = QtWidgets.QApplication(sys.argv)
    arr, l = QtWidgets.QFileDialog.getOpenFileNames(parent=None,
                                                    caption="Заголовок окна", directory=QtCore.QDir.currentPath(),
                                                    filter="Excel (*.xls);;Текст (*.csv);;All (*)")
    #LiraParser.RSU_xls2csv(arr)
    #sys.exit(app.exec_())
    print(arr)

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


#%%
if __name__ == '__main__':
    on_clicked()
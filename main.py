# %%
#from PyQt5 import QtCore, QtWidgets
#from MainWindow import Ui_MainWindow
from modules.project import Project
from modules.element import Element, Fe, FeBar, FePlate
import pickle
import sys


# %%


def createProject(namePrj):
    return Project(namePrj)


def saveProject(prj: Project):
    path = input('Введите расположение проекта: ')
    if path == '':
        path = 'work/' + prj.name + '.ndm'
    with open(path, "wb") as file:
        pickle.dump(prj, file)


def openProject(path: str = 'work/'):
    name = input('Введите имя проекта: ')
    if name == '':
        print('!Не указано имя проекта!')
        return
    with open(path + name + '.ndm', "rb") as file:
        res = pickle.load(file)
    return res


def createElement(proj: Project, numEl, descr=''):
    proj.elements.append(Element(numEl))

def addElement(prj: Project):
    item:Element
    num = input('Введите номер элемента: ')
    if num == '': return
    try:
        num = int(num)
        if num in prj.getElementsNumbers():
            print('!!!Элемент с указанным номером уже существует!!!')
            return
        else:
            item = Element(num)
            prj.elements.append(item)
            prj.selectedElement = item
    except:
        print('!!!Не верно задан номер элемента!!!')
        return


def add(prj: Project, inp='.el'):
    if inp == '.el':
        addElement(prj)

    


def main():
    prj: Project = Project('temp')
    inp = ''
    while inp != '.exit':

        if inp == '.new':
            alert = input('Cохранить открытый проект? (Y/n): ')
            name = input('Введите имя проекта: ')
            if alert == 'Y' or name == 'y':
                saveProject(prj)
            prj = createProject(name)

        elif inp == '.save':
            saveProject(prj)

        elif inp == '.open':
            prj = openProject()

        elif inp == '.add':
            sinp = input(
                '<.el> - добавление элемента\n<.fe> - добавление участка\n<.cs> - добавление сечения\n>>> ')
            add(sinp,prj)

        elif inp == '.help':
            print('==========================================')
            print('Программа расчета железобетонных элементов')
            print('==========================================')

        inp = input('>>> ')


if __name__ == "__main__":
    main()

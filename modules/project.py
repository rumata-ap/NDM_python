# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets, QtGui
import modules.lira_parser as lp

# %%


class Project:
    def __init__(self, name):
        self.name = name
        self.descr = ''
        self.nodes = {}
        self.stiffs = {}
        self.sections = {}
        self.contours = {}
        self.loads = {'c': {}, 'cl': {}, 'n': {}, 'nl': {}}
        self.fes = {'b': {}, 's': {}}
        self.elements = {}
        self.materials = {'b': {}, 'a': {}}
        self.selectedElement = None
        self.selectedBeton = None
        self.selectedArm = None
        self.selectedFe = None
        self.selectedSect = None
        self.selectedLoadsGroup = None

    def getElementsNumbers(self):
        if len(self.elements) == 0:
            return []
        return self.elements.keys()

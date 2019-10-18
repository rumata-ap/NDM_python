from modules.element import Element, Fe, FeBar, FePlate
from modules.betonSelector import Beton
from modules.armSelector import Armatura

# %%


class Project:
    def __init__(self, name):
        self.name = name
        self.descr = ''
        self.nodes = []
        self.fes = {'b': [], 's': []}
        self.elements = []
        self.materials = {'b': [], 'a': []}
        self.selectedElement:Element
        self.selectedBeton:Beton
        self.selectedArm:Armatura
        self.selectedFe:Fe

    def getElementsNumbers(self):
        res = []
        for item in self.elements:
            res.append(item.number)
        return res

from modules.element import Element, Fe, FeBar, FePlate

# %%


class Project:
    name = ''
    descr = ''
    nodes = []
    bars = []
    shells = []
    elements = []
    materials = {'beton': [], 'armatura': []}
    selectedElement: Element
    selectedFe: Fe

    def __init__(self, name):
        self.name = name

    def getElementsNumbers(self):
        res = []
        for item in self.elements:
            res.append(item.number)
        return res

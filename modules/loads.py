from modules.element import Element

# %%
class LoadNDM:
    def __init__(self, n=0., mx=0., my=0.):
        self.N = n
        self.Mx = mx
        self.My = my
        self.N_ = n
        self.Mx_ = mx
        self.My_ = my
        self.attr = {}

    def getNu(self, el:Element):
        pass

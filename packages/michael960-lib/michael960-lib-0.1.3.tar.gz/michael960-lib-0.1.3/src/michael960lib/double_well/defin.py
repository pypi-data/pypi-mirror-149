import numpy as np

class DoubleWellPotential:
    def __init__(self, name, U, dU, min_1, min_2, mx):
        self.U = U
        self.name = name
        self.dU = dU
        self.min_1 = min_1
        self.min_2 = min_2
        self.mx = mx

    def get_name(self):
        return self.name

    def get_U(self):
        return self.U

    def get_dU(self):
        return self.dU

    def get_min_1(self):
        return self.min_1

    def get_min_2(self):
        return self.min_2

    def get_mx(self):
        return self.mx

    def get_area(self, slices=1e4):
        b = np.linspace(self.get_min_1(), self.get_min_2(), int(slices))
        db = b[1] - b[0]
        return np.sum(self.get_U()(b) * db)

    def get_area_right(self, slices=1e4):
        b = np.linspace(self.get_mx(), self.get_min_2(), int(slices))
        db = b[1] - b[0]
        return np.sum(self.get_U()(b) * db)
    
    def get_area_left(self, slices=1e4):
        b = np.linspace(self.get_min_1(), self.get_mx(), int(slices))
        db = b[1] - b[0]
        return np.sum(self.get_U()(b) * db)

    def get_sqrt_area(self, slices=1e4):
        b = np.linspace(self.get_min_1(), self.get_min_2(), int(slices))
        db = b[1] - b[0]
        return np.sum(np.sqrt(self.get_U()(b)) * db)

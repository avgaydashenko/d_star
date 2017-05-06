class CellInfo:
    def __init__(self, g=0., rhs=0., cost=0.):
        self.g = g
        self.rhs = rhs
        self.cost = cost

    def __repr__(self):
        return "g: {g}, rhs: {r}, cost: {c}".format(g=self.g, r=self.rhs, c=self.cost)
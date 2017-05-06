class State:
    def __init__(self, x, y, k):
        self.x = x
        self.y = y
        self.k = k

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return self.x != other.x or self.y != other.y

    def __gt__(self, other):
        if self.k.first() - 0.00001 > other.k.first():
            return True
        elif self.k.first() < other.k.first() - 0.00001:
            return False
        return self.k.second() > other.k.second()

    def __le__(self, other):
        if self.k.first() < other.k.first():
            return True
        elif self.k.first() > other.k.first():
            return False
        return self.k.second() < other.k.second() + 0.00001

    def __lt__(self, other):
        if self.k.first() + 0.000001 < other.k.first():
            return True
        elif self.k.first() - 0.000001 > other.k.first():
            return False
        return self.k.second() < other.k.second()

    def __cmp__(self, other):
        if self.k.first() - 0.00001 > other.k.first():
            return 1
        elif self.k.first() < other.k.first() - 0.00001:
            return -1
        if self.k.second() > other.k.second():
            return 1
        elif self.k.second() < other.k.second():
            return -1
        return 0

    def __hash__(self):
        return self.x + 34245 * self.y

    def __repr__(self):
        return "State: {x}, {y}, ({f}, {s})".format(x=self.x, y=self.y, f=self.k.first(), s=self.k.second())

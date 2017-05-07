from pair import Pair
from state import State
from cell_info import CellInfo
from point import Point
from math import sqrt, pow, inf
from queue import Queue


class DStar:
    STRAIGHT_DIST = 1
    DIAGONAL_DIST = sqrt(2)

    @classmethod
    def heuristic(cls, a, b):
        x_diff, y_diff = abs(a.x - b.x), abs(a.y - b.y)
        return (cls.DIAGONAL_DIST - 1) * min(x_diff, y_diff) + max(x_diff, y_diff)

    @classmethod
    def key_hash_code(cls, u):
        return u.k.first() + 1193 * u.k.second()

    @classmethod
    def true_dist(cls, a, b):
        return sqrt(pow(a.x - b.x, 2) + pow(a.y - b.y, 2))

    @classmethod
    def close(cls, x, y):
        if x == inf and y == inf:
            return True
        return abs(x - y) < 0.00001

    def get_path(self):
        return self.path

    def cost(self, a, b):
        x_diff = abs(a.x - b.x)
        y_diff = abs(a.y - b.y)

        scale = self.DIAGONAL_DIST if x_diff + y_diff > 1 else self.STRAIGHT_DIST

        if a in self.cell_hash.keys():
            return scale * self.cell_hash[a].cost
        return scale

    def get_rhs(self, u):
        if u == self.s_goal:
            return 0
        if u not in self.cell_hash:
            return self.heuristic(u, self.s_goal)
        return self.cell_hash[u].rhs

    def get_g(self, u):
        if u not in self.cell_hash.keys():
            return self.heuristic(u, self.s_goal)
        return self.cell_hash[u].g

    def calculate_key(self, u):
        val = min(self.get_rhs(u), self.get_g(u))
        return State(u.x, u.y, Pair(val + self.heuristic(u, self.s_start) + self.k_m, val))

    def make_new_cell(self, u):
        if u in self.cell_hash.keys():
            return
        dist = self.heuristic(u, self.s_goal)
        tmp = CellInfo(dist, dist, self.STRAIGHT_DIST)
        self.cell_hash[u] = tmp

    def clear_fields(self):
        self.cell_hash = {}
        self.open_hash = {}
        self.open_list = Queue()
        self.k_m = 0

        self.make_new_cell(self.s_goal)
        self.make_new_cell(self.s_start)

        self.s_start = self.calculate_key(self.s_start)

        self.s_last = self.s_start

    def __init__(self, x_start, y_start, x_goal, y_goal):
        self.path = []

        self.s_start = State(x_start, y_start, Pair(0, 0))
        self.s_goal = State(x_goal, y_goal, Pair(0, 0))

        self.clear_fields()

    def set_g(self, u, g):
        self.make_new_cell(u)
        self.cell_hash[u].g = g

    def set_rhs(self, u, rhs):
        self.make_new_cell(u)
        self.cell_hash[u].rhs = rhs

    def is_valid(self, u):
        if u not in self.open_hash:
            return False
        if not self.close(self.key_hash_code(u), self.open_hash[u]):
            return False
        return True

    def occupied(self, u):
        if u not in self.cell_hash:
            return False
        return self.cell_hash[u].cost < 0

    def get_predecessors(self, u):
        s = []

        tmp = State(u.x + 1, u.y, Pair(-1, -1))
        if not self.occupied(tmp):
            s.append(tmp)
        tmp = State(u.x + 1, u.y + 1, Pair(-1, -1))
        if not self.occupied(tmp):
            s.append(tmp)
        tmp = State(u.x, u.y + 1, Pair(-1, -1))
        if not self.occupied(tmp):
            s.append(tmp)
        tmp = State(u.x - 1, u.y + 1, Pair(-1, -1))
        if not self.occupied(tmp):
            s.append(tmp)
        tmp = State(u.x - 1, u.y, Pair(-1, -1))
        if not self.occupied(tmp):
            s.append(tmp)
        tmp = State(u.x - 1, u.y - 1, Pair(-1, -1))
        if not self.occupied(tmp):
            s.append(tmp)
        tmp = State(u.x, u.y - 1, Pair(-1, -1))
        if not self.occupied(tmp):
            s.append(tmp)
        tmp = State(u.x + 1, u.y - 1, Pair(-1, -1))
        if not self.occupied(tmp):
            s.append(tmp)

        return s

    def get_successors(self, u):
        s = []

        if self.occupied(u):
            return s

        s.append(State(u.x + 1, u.y, Pair(-1, -1)))
        s.append(State(u.x + 1, u.y + 1, Pair(-1, -1)))
        s.append(State(u.x, u.y + 1, Pair(-1, -1)))
        s.append(State(u.x - 1, u.y + 1, Pair(-1, -1)))
        s.append(State(u.x - 1, u.y, Pair(-1, -1)))
        s.append(State(u.x - 1, u.y - 1, Pair(-1, -1)))
        s.append(State(u.x, u.y - 1, Pair(-1, -1)))
        s.append(State(u.x + 1, u.y - 1, Pair(-1, -1)))

        return s

    def update_start(self, x, y):
        self.s_start.x = x
        self.s_start.y = y
        self.k_m += self.heuristic(self.s_last, self.s_start)
        self.s_start = self.calculate_key(self.s_start)
        self.s_last = self.s_start

    def update_goal(self, x, y):
        to_add = []
        for state in self.cell_hash:
            if not self.close(self.cell_hash[state], self.STRAIGHT_DIST):
                to_add.append(Pair(Point(state.x, state.y), self.cell_hash[state].cost))

        self.s_goal.x = x
        self.s_goal.y = y

        self.clear_fields()

        for p in to_add:
            self.update_cell(p.first().x, p.first().y, p.second())

    def insert(self, u):
        u = self.calculate_key(u)
        csum = self.key_hash_code(u)
        self.open_hash[u] = csum
        self.open_list.put(u)

    def update_vertex(self, u):
        if u != self.s_goal:
            s = self.get_successors(u)
            tmp = inf

            for i in s:
                tmp = min(tmp, self.get_g(i) + self.cost(u, i))

            if not self.close(self.get_rhs(u), tmp):
                self.set_rhs(u, tmp)

        if not self.close(self.get_g(u), self.get_rhs(u)):
            self.insert(u)

    def update_cell(self, x, y, val):
        u = State(x, y, Pair(0, 0))

        if u == self.s_start or u == self.s_goal:
            return

        self.make_new_cell(u)
        self.cell_hash[u].cost = val
        self.update_vertex(u)

    def compute_shortest_path(self):
        if self.open_list.empty():
            return 1

        self.s_start = self.calculate_key(self.s_start)
        while not self.open_list.empty() and self.open_list.queue[0] < self.s_start \
                or self.get_rhs(self.s_start) != self.get_g(self.s_start):

            test = self.get_rhs(self.s_start) != self.get_g(self.s_start)

            while True:
                if self.open_list.empty():
                    return 1
                u = self.open_list.get()
                if not self.is_valid(u):
                    continue
                if not u < self.s_start and not test:
                    return 2
                break

            self.open_hash.pop(u)
            k_old = State(u.x, u.y, u.k)

            if k_old < self.calculate_key(u):
                self.insert(u)
            elif self.get_g(u) > self.get_rhs(u):
                self.set_g(u, self.get_rhs(u))
                s = self.get_predecessors(u)
                for i in s:
                    self.update_vertex(i)
            else:
                self.set_g(u, inf)
                s = self.get_predecessors(u)
                for i in s:
                    self.update_vertex(i)
                self.update_vertex(u)

            self.s_start = self.calculate_key(self.s_start)
        return 0

    def replan(self):
        self.path = []
        if self.compute_shortest_path() < 0:
            return False

        cur = self.s_start
        if self.get_g(self.s_start) == inf:
            return False
        while cur != self.s_goal:
            self.path.append(cur)
            n = self.get_successors(cur)

            if len(n) == 0:
                return False

            cmin = inf
            tmin = 0

            for i in n:
                val = self.cost(cur, i)
                val2 = self.true_dist(i, self.s_goal) + self.true_dist(self.s_start, i)
                val += self.get_g(i)

                if self.close(val, cmin) and tmin > val2 or val < cmin:
                    tmin = val2
                    cmin = val
                    smin = i

            cur = State(smin.x, smin.y, smin.k)

        self.path.append(self.s_goal)

        return True

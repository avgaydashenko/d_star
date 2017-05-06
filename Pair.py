class Pair:
    def __init__(self, fst, snd):
        self.fst = fst
        self.snd = snd
        self.fstNone = fst is None
        self.sndNone = snd is None
        self.dualNone = self.fstNone and self.sndNone

    def first(self):
        return self.fst

    def second(self):
        return self.snd

    def set_first(self, fst):
        self.fst = fst
        self.fstNone = fst is None
        self.dualNone = self.fstNone and self.sndNone

    def set_second(self, snd):
        self.snd = snd
        self.sndNone = snd is None
        self.dualNone = self.fstNone and self.sndNone

    def __eq__(self, other):
        if other is None:
            return False

        if self == other:
            return True

        if not isinstance(other, Pair):
            return False

        if self.dualNone:
            return other.dualNone

        if other.dualNone:
            return False

        if self.fstNone:
            if other.fstNone:
                return self.snd == other.snd
            elif other.sndNone:
                return self.snd == other.fst
            else:
                return False

        elif self.sndNone:
            if other.sndNone:
                return self.fst == other.fst
            elif other.fstNone:
                return self.fst == other.snd
            else:
                return False

        else:
            if self.fst == other.fst:
                return self.snd == other.snd
            elif self.fst == other.snd:
                return self.snd == other.fst
            else:
                return False

    def __hash__(self):
        hash_code = 0 if self.fstNone else hash(self.fst)
        hash_code += 0 if self.sndNone else hash(self.snd)
        return hash_code

    def __repr__(self):
        return "Pair: {f}, {s}".format(f=self.fst, s=self.snd)

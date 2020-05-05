import itertools
import copy


class AlphaPlus:
    def __init__(self, log):
        self.log = set(log)
        self.all_events = self.get_all_events()
        self.direct_succession = self.get_direct_succession()[0]
        self.l1l = self.get_direct_succession()[1]
        self.triangle = self.get_direct_succession()[2]
        self.romb = self.get_direct_succession()[3]
        self.causal = self.get_causality(self.direct_succession, self.romb)
        self.parallel = self.get_parallel(self.direct_succession, self.romb)
        self.independent = self.get_independent(self.all_events, self.causal, self.parallel)
        self.start_events = self.get_start_events()
        self.end_events = self.get_end_events()
        self.xl = self.get_XL_set(self.all_events, self.independent, self.causal)
        self.yl = self.get_YL_set(self.xl, self.parallel)

    def __str__(self):
        alpha_sets = []
        alpha_sets.append("Start events:\t{}".format(self.start_events))
        alpha_sets.append("End events:\t\t{}".format(self.end_events))
        alpha_sets.append("XL set:\t\t\t{}".format(self.xl))
        alpha_sets.append("YL set:\t\t\t{}".format(self.yl))
        return '\n'.join(alpha_sets)

    def get_all_events(self):
        all_events = set()
        for row in self.log:
            for i in row:
                all_events.add(i)
        return all_events

    def get_start_events(self):
        start_events = set()
        for row in self.log:
            start_events.add(row[0])
        return start_events

    def get_end_events(self):
        end_events = set()
        for row in self.log:
            end_events.add(row[-1])
        return end_events

    def get_XL_set(self, all_events, independent, causal):
        xl = set()
        subsets = itertools.chain.from_iterable(itertools.combinations(all_events, r) for r in range(1, len(all_events) + 1))
        independent_a_or_b = [a_or_b for a_or_b in subsets if self.is_independent(a_or_b, independent)]
        for a, b in itertools.product(independent_a_or_b, independent_a_or_b):
            if self.is_causal((a, b), causal):
                xl.add((a, b))
        return xl

    def is_independent(self, s, independent):
        if len(s) == 1:
            return True
        else:
            s_all = itertools.combinations(s, 2)
            for pair in s_all:
                if pair not in independent:
                    return False
            return True

    def is_causal(self, s, causal):
        set_a, set_b = s[0], s[1]
        s_all = itertools.product(set_a, set_b)
        for pair in s_all:
            if pair not in causal:
                return False
        return True

    def get_YL_set(self, xl, pr):
        yl = copy.deepcopy(xl)
        s_all = itertools.combinations(yl, 2)
        for pair in s_all:
            if self.issubset(pair[0], pair[1]):
                yl.discard(pair[0])
            elif self.issubset(pair[1], pair[0]):
                yl.discard(pair[1])

        # remove self-loops
        # e.g. if (a,b),(b,c) in YL, and (b,b) in Parallel, then we need to remove (a,b),(b,c)
        # (a,b) is equal to (a,bb), also b||b, thus a and bb cannot make a pair, only "#" relations can.
        self_loop = set()
        for pair in pr:
            if pair == pair[::-1]:  # if we found pairs like (b,b), add b into self-loop sets
                self_loop.add(pair[0])

        to_be_deleted = set()
        for pair in yl:
            if self.contains(pair, self_loop):
                to_be_deleted.add(pair)
        for pair in to_be_deleted:
            yl.discard(pair)
        return yl

    def issubset(self, a, b):
        if set(a[0]).issubset(b[0]) and set(a[1]).issubset(b[1]):
            return True
        return False

    def contains(self, a, b):
        # return True if nested tuple "a" contains any letter in set "b"
        # e.g. __contains((('a',), ('b',)), ('b', 'c')) -> True
        return any(j == i[0] for i in a for j in b)

    def get_footprint(self):
        footprint = []
        footprint.append("All transitions: {}".format(self.all_events))
        footprint.append("Direct succession: {}".format(self.direct_succession))
        footprint.append("Causality: {}".format(self.causal))
        footprint.append("Parallel: {}".format(self.parallel))
        footprint.append("Independent: {}".format(self.independent))
        return '\n'.join(footprint)

    def generate_footprint(self, txtfile='footprint.txt'):
        with open(txtfile, 'w') as f:
            f.write(self.get_footprint())

    def get_direct_succession(self):
        # x > y
        ds = set()
        l1l = set()
        tr = set()
        rb = set()
        for trace in self.log:
            for x, y, z in zip(trace, trace[1:], trace[2:]):
                if y == z and x != y:
                    l1l.add(((y, z), x))
                else:
                    if (y, z) not in ds:
                        ds.add((y, z))
                    if (x, y) not in ds:
                        ds.add((x, y))
                    if x == z and x != y:
                        tr.add((x, y))
                    if x == z and x != y and (y, x) in tr and (x, y) in tr:
                        tr.remove((y, x))
                        if (x, y) in tr:
                            tr.remove((x, y))
                            rb.add((y, x))
                            rb.add((x, y))
        return [ds, l1l, tr, rb]

    def get_causality(self, ds, rb):
        # x -> y
        cs = set()
        for pair in ds:
            if pair[::-1] not in ds or pair in rb:
                cs.add(pair)
        return cs

    def get_parallel(self, ds, rb):
        # (x || y) & (y || x)
        pr = set()
        for pair in ds:
            if pair[::-1] in ds and pair not in rb:
                pr.add(pair)
        return pr

    def get_independent(self, tl, cs, pr):
        # (x # y) & (y # x)
        ind = set()  # ind is the abbreviation of independent
        all_permutations = itertools.permutations(tl, 2)
        for pair in all_permutations:
            if pair not in cs and pair[::-1] not in cs and pair not in pr:
                ind.add(pair)
        return ind

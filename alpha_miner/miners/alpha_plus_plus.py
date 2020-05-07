import itertools
import copy


class AlphaPlusPlus:
    def __init__(self, log):
        self.log = set(log)
        self.all_events = self.get_all_events()
        self.direct_succession = self.get_direct_succession()[0]
        self.l1l = self.get_direct_succession()[1]
        self.triangle = self.get_direct_succession()[2]
        self.causal = self.get_causality(self.direct_succession, self.triangle)
        self.parallel = self.get_parallel(self.direct_succession, self.triangle)
        self.independent = self.get_independent(self.all_events, self.direct_succession)

        self.xor_split = self.get_xor_split(self.independent, self.causal, self.all_events)
        self.xor_join = self.get_xor_join(self.independent, self.causal, self.all_events)
        self.indirect_succession = self.get_indirect_succession(self.all_events, self.direct_succession,
                                                                self.xor_join, self.xor_split)
        self.succession = self.get_succesion(self.causal, self.indirect_succession)

        self.start_events = self.get_start_events()
        self.end_events = self.get_end_events()
        self.xl = self.get_XL_set(self.all_events, self.independent, self.causal)
        self.yl = self.get_YL_set(self.xl, self.parallel)

        self.all_places = self.get_places(self.yl)

        self.w1 = self.get_w1(self.all_events, self.direct_succession, self.all_places, self.succession, self.parallel)
        self.w2_1 = self.get_w2_1(self.all_events, self.indirect_succession, self.all_places, self.succession,
                                  self.parallel, self.xor_split)
        self.w2_2 = self.get_w2_2(self.all_events, self.indirect_succession, self.all_places, self.succession,
                                  self.parallel, self.xor_join)
        self.w2 = self.get_w2(self.w2_1, self.w2_2)
        self.w3 = self.get_w3(self.all_events, self.indirect_succession, self.all_places, self.succession,
                              self.parallel)

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
        for trace in self.log:
            for x, y, z in zip(trace, trace[1:], trace[2:]):
                if y == z:
                    l1l.add(((y, z), x))
                elif x == y:
                    l1l.add(((x, y), z))
                else:
                    if (y, z) not in ds:
                        ds.add((y, z))
                    if (x, y) not in ds:
                        ds.add((x, y))
                    if x == z:
                        tr.add((x, y))
        return [ds, l1l, tr]

    def get_causality(self, ds, tr):
        # x -> y
        cs = set()
        for pair in ds:
            if pair[::-1] not in ds or pair in tr or pair[::-1] in tr:
                cs.add(pair)
        return cs

    def get_parallel(self, ds, tr):
        # (x || y) & (y || x)
        pr = set()
        for pair in ds:
            if pair[::-1] in ds and (pair not in tr or pair[::-1] not in tr):
                pr.add(pair)
        return pr

    def get_independent(self, all_events, ds):
        # (x # y) & (y # x)
        ind = set()  # ind is the abbreviation of independent
        all_permutations = itertools.permutations(all_events, 2)
        for pair in all_permutations:
            if pair not in ds and pair[::-1] not in ds:
                ind.add(pair)
        return ind

    def get_xor_split(self, independent, casual, all_events):
        xor_split = set()
        for pair in independent:
            for event in all_events:
                if (event, pair[0]) in casual and (event, pair[1]) in casual:
                    xor_split.add(pair)
        return xor_split

    def get_xor_join(self, independent, casual, all_events):
        xor_join = set()
        for pair in independent:
            for event in all_events:
                if (pair[0], event) in casual and (pair[1], event) in casual:
                    xor_join.add(pair)
        return xor_join

    def get_indirect_succession(self, all_events, direct_succession, xor_join, xor_split):
        indirect_succession = set()
        all_permutations = itertools.permutations(all_events, 2)
        for pair in all_permutations:
            for trace in self.log:
                if pair[0] in trace and pair[1] in trace and trace.index(pair[0]) < trace.index(pair[1]) + 1 and pair not in direct_succession:
                    for x in range(trace.index(pair[0]), trace.index(pair[1])):
                        if (trace[x], pair[0]) not in xor_join and (trace[x], pair[0]) not in xor_split:
                            indirect_succession.add(pair)
        return indirect_succession

    def get_succesion(self, casual, indirect_succession):
        succession = set()
        succession = succession.union(casual, indirect_succession)
        return succession

    def get_places(self, yl):
        places = []
        for item in yl:
            ins = []
            outs = []
            for inp in item[0]:
                ins.append(inp)
            for outp in item[1]:
                outs.append(outp)
            new_place = Place(ins, outs)
            places.append(new_place)
        return places

    def get_w1(self, all_events, direct_succession, all_places, succession, parallel):
        w1 = set()
        all_permutations = itertools.permutations(all_events, 2)
        for pair in all_permutations:
            if pair not in direct_succession:
                for event in all_events:
                    places = []
                    for place in all_places:
                        if event in place.outs:
                            places.append(place)
                    if len(places) >= 2:
                        all_places_permutations = itertools.permutations(places, 2)
                        for perm in all_places_permutations:
                            if pair[0] in perm[0].ins and pair[0] not in perm[1].ins and pair[1] in perm[1].outs:
                                for t in perm[1].ins:
                                    if (t, pair[0]) not in succession and (t, pair[0]) not in parallel:
                                        w1.add(pair)
        return w1

    def get_w2_1(self, all_events, indirect_succession, all_places, succession, parallel, xor_split):
        w2_1 = set()
        all_permutations = itertools.permutations(all_events, 2)
        for pair in all_permutations:
            if pair in indirect_succession:
                a_places = []
                for place in all_places:
                    if pair[0] in place.ins:
                        a_places.append(place)
                if len(a_places) > 1:
                    for event in all_events:
                        if (pair[1], event) in xor_split:
                            for place in a_places:
                                for t in place.outs:
                                    for t_prim in place.outs:
                                        if not ((t, pair[1]) in succession or (t, pair[1]) in parallel) and ((t_prim, event) in succession or (t_prim, event) in parallel):
                                            w2_1.add(pair)
        return w2_1

    def get_w2_2(self, all_events, indirect_succession, all_places, succession, parallel, xor_join):
        w2_2 = set()
        all_permutations = itertools.permutations(all_events, 2)
        for pair in all_permutations:
            if pair in indirect_succession:
                b_places = []
                for place in all_places:
                    if pair[1] in place.outs:
                        b_places.append(place)
                if len(b_places) > 1:
                    for event in all_events:
                        if (pair[0], event) in xor_join:
                            for place in b_places:
                                for t in place.ins:
                                    for t_prim in place.ins:
                                        if not ((pair[0], t) in succession or (pair[0], t) in parallel) and ((event, t_prim) in succession or (event, t_prim) in parallel):
                                            w2_2.add(pair)
        return w2_2

    def get_w2(self, w2_1, w2_2):
        w2 = w2_1.union(w2_2)
        return w2

    def get_w3(self, all_events, indirect_succession, all_places, succession, parallel):
        w3 = set()
        all_permutations = itertools.permutations(all_events, 2)
        for pair in all_permutations:
            for a_prim in all_events:
                for b_prim in all_events:
                    if pair in indirect_succession and (a_prim, b_prim) in indirect_succession and (pair[0], b_prim) not in indirect_succession and (a_prim, pair[1]) not in indirect_succession:
                        a_out_places = []
                        b_in_places = []
                        a_prim_out_places = []
                        b_prim_in_places = []
                        for place in all_places:
                            if pair[0] in place.ins:
                                a_out_places.append(place)
                            if pair[1] in place.outs:
                                b_in_places.append(place)
                            if a_prim in place.ins:
                                a_prim_out_places.append(place)
                            if b_prim in place.outs:
                                b_prim_in_places.append(place)
                        a_common_part = list(set(a_out_places).intersection(a_prim_out_places))
                        b_common_part = list(set(b_in_places).intersection(b_prim_in_places))
                        if len(a_common_part) > 0 and len(b_common_part) > 0 and set(b_in_places).issubset(set(b_prim_in_places)):
                            for t in all_events:
                                if (pair[0], t) not in indirect_succession and (a_prim, t) in indirect_succession and ((b_prim, t) in parallel or (b_prim, t) in succession):
                                    t_in_places = []
                                    for t_place in all_places:
                                        if t in t_place.outs:
                                            t_in_places.append(t_place)
                                    b_t_common_part = list(set(b_in_places).intersection(t_in_places))
                                    if len(b_t_common_part) > 0:
                                        w3.add(pair)
        return w3


class Place:
    _ins = []
    _outs = []

    def __init__(self, ins, outs):
        self._ins = ins
        self._outs = outs

    @property
    def ins(self):
        return self._ins

    @property
    def outs(self):
        return self._outs

    def __str__(self):
        output = []
        for inp in self.ins:
            output.append(inp)
        output.append('-> o ->')
        for outp in self.outs:
            output.append(outp)
        return ' '.join(output)

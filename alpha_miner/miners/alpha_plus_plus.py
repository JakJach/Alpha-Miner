import itertools
import copy
from miners.alpha import Alpha


class AlphaPlusPlus:
    def __init__(self, log):
        # KROK 1
        self.log = set(log)
        self.all_events = self.set_all_events()
        # KROK 2
        self.l1l = self.set_direct_succession()[1]
        # KROK 3
        self.t_prim = self.set_t_prim()
        # KROK 4
        self.direct_succession = self.set_direct_succession()[0]
        self.triangle = self.set_direct_succession()[2]
        self.parallel = self.set_parallel()
        self.independent = self.set_independent()
        self.xw = self.set_xw(self.t_prim, self.l1l, self.direct_succession, self.triangle, self.parallel,
                              self.independent)
        # KROK 5
        self.lw = self.set_lw(self.xw)
        # KROK 6 i 7
        self.w_l1l = self.set_w_l1l()
        # KROK 8
        self.causal = self.set_causality()
        self.xl = self.set_XL_set()
        self.yl = self.set_YL_set()
        self.all_places = self.set_places(self.yl)
        self.xor_split = self.set_xor_split()
        self.xor_join = self.set_xor_join()
        self.indirect_succession = self.set_indirect_succession(self.all_events, self.direct_succession,
                                                                self.xor_join, self.xor_split)
        self.succession = self.set_succession(self.causal, self.indirect_succession)
        self.w1 = self.set_w1()
        self.idw1 = self.set_idw1()
        # KROK 9
        self.pw_l1l = self.set_pw_l1l()
        self.tw_l1l = self.set_tw_l1l()
        # KROK 10 i 11
        self.idw2 = self.eliminate_by_rule_1(self.set_idw2())
        # KROK 12
        self.w2_1 = self.set_w2_1(self.all_events, self.indirect_succession, self.all_places, self.succession,
                                  self.parallel, self.xor_split)
        self.w2_2 = self.set_w2_2(self.all_events, self.indirect_succession, self.all_places, self.succession,
                                  self.parallel, self.xor_join)
        self.w2 = self.set_w2(self.w2_1, self.w2_2)
        self.xw_12 = self.set_xw_12()
        # KROK 13
        self.yw = self.set_yw()
        # KROK 14 i 15
        self.idw3 = self.eliminate_by_rule_2(self.set_idw3())
        # KROK 16
        self.xw_16 = self.set_xw_16()
        # KROK 17
        self.zw = self.set_zw()
        # KROK 18
        self.pw = self.set_pw()
        # KROK 19
        self.tw = self.set_tw()
        self.start_events = self.set_start_events()
        self.end_events = self.set_end_events()
        # self.w3 = self.set_w3(self.all_events, self.indirect_succession, self.all_places, self.succession,
        #                       self.parallel)

    # FOOTPRINT MATRIX
    def set_footprint(self):
        footprint = ["All transitions: {}".format(self.all_events),
                     "Direct succession: {}".format(self.direct_succession), "Causality: {}".format(self.causal),
                     "Parallel: {}".format(self.parallel), "Independent: {}".format(self.independent)]
        return '\n'.join(footprint)

    def generate_footprint(self, txtfile='footprint.txt'):
        with open(txtfile, 'w') as f:
            f.write(self.set_footprint())

    # USEFUL FUNCTIONS
    def __str__(self):
        alpha_sets = ["Start events:\t{}".format(self.start_events), "End events:\t\t{}".format(self.end_events),
                      "XL set:\t\t\t{}".format(self.xl), "YL set:\t\t\t{}".format(self.yl)]
        return '\n'.join(alpha_sets)

    @staticmethod
    def is_independent(s, independent):
        if len(s) == 1:
            return True
        else:
            s_all = itertools.combinations(s, 2)
            for pair in s_all:
                if pair not in independent:
                    return False
            return True

    @staticmethod
    def is_causal(s, causal):
        set_a, set_b = s[0], s[1]
        s_all = itertools.product(set_a, set_b)
        for pair in s_all:
            if pair not in causal:
                return False
        return True

    @staticmethod
    def issubset(a, b):
        if set(a[0]).issubset(b[0]) and set(a[1]).issubset(b[1]):
            return True
        return False

    @staticmethod
    def contains(a, b):
        # return True if nested tuple "a" contains any letter in set "b"
        # e.g. __contains((('a',), ('b',)), ('b', 'c')) -> True
        return any(j == i[0] for i in a for j in b)

    @staticmethod
    def set_succession(casual, indirect_succession):
        succession = set()
        succession = succession.union(casual, indirect_succession)
        return succession

    @staticmethod
    def set_places(yl):
        '''
        :param yl:  YL set of miner
        :return:    list of Places
        '''
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

    # SETTERS
    # krok 1
    def set_all_events(self):
        all_events = set()
        for row in self.log:
            for i in row:
                all_events.add(i)
        return all_events

    # krok 2
    def set_direct_succession(self):
        # x > y
        direct_succession = set()
        l1l = set()
        triangle = set()
        for trace in self.log:
            for x, y, z in zip(trace, trace[1:], trace[2:]):
                if (x == y or y == z) and y not in l1l:
                    l1l.add(y)
                else:
                    if (y, z) not in direct_succession:
                        direct_succession.add((y, z))
                    if (x, y) not in direct_succession:
                        direct_succession.add((x, y))
                    if x == z:
                        triangle.add((x, y))
        return [direct_succession, l1l, triangle]

    # krok 3
    def set_t_prim(self):
        t_prim = set()
        for event in self.all_events:
            t_prim.add(event)
            for pair in self.l1l:
                if event in pair[0] and event in t_prim:
                    t_prim.remove(event)
        return t_prim

    # krok 4
    def set_parallel(self):
        # (x || y) & (y || x)
        parallel = set()
        for pair in self.direct_succession:
            if pair[::-1] in self.direct_succession and (pair not in self.triangle or pair[::-1] not in self.triangle):
                parallel.add(pair)
        return parallel

    def set_independent(self):
        # (x # y) & (y # x)
        ind = set()  # ind is the abbreviation of independent
        all_permutations = itertools.permutations(self.all_events, 2)
        for pair in all_permutations:
            if pair not in self.direct_succession and pair[::-1] not in self.direct_succession:
                ind.add(pair)
        return ind

    def set_xw(self, t_prim, l1l, direct_succession, triangle, parallel, independent):
        xw = set()
        a_set = []
        b_set = []
        for a in t_prim:
            for b in t_prim:
                if (a, b) not in parallel:
                    for c in l1l:
                        if (a, c) in direct_succession and (c, a) not in triangle and \
                                (c, b) in direct_succession and (c, b) not in triangle:
                            a_set.append(a)
                            b_set.append(b)

                            if len(a_set) > 1:
                                for a1, a2 in zip(a_set, a_set[1:]):
                                    if (a1, a2) not in independent:
                                        a_set.remove(a1)
                                        a_set.remove(a2)
                            if len(b_set) > 1:
                                for b1, b2 in zip(b_set, b_set[1:]):
                                    if (b1, b2) not in independent:
                                        b_set.remove(b1)
                                        b_set.remove(b2)

                            if a in a_set and b in b_set:
                                xw.add((a, b, c))
        return xw

    # krok 5
    def set_lw(self, xw):
        a_prim = []
        b_prim = []
        c_prim = []
        lw = set()
        for triplet in xw:
            if triplet[0] not in a_prim:
                a_prim.append(triplet[0])
            if triplet[1] not in b_prim:
                b_prim.append(triplet[1])
            if triplet[2] not in c_prim:
                c_prim.append(triplet[2])
        for a in a_prim:
            for b in b_prim:
                for c in c_prim:
                    if (a, b, c) in xw:
                        lw.add((a, b, c))
        return lw

    # krok 6 i 7
    def set_w_l1l(self):
        w_l1l = []
        for row in self.log:
            new_row = list(row)
            for i in self.l1l:
                new_row = list(filter((i).__ne__, new_row))
            w_l1l.append(tuple(new_row))
        return w_l1l

    # krok 8
    def set_causality(self):
        # x -> y
        casual = set()
        for pair in self.direct_succession:
            if pair[::-1] not in self.direct_succession or pair in self.triangle or pair[::-1] in self.triangle:
                casual.add(pair)
        return casual

    def set_XL_set(self):
        xl = set()
        subsets = itertools.chain.from_iterable(itertools.combinations(self.all_events, r) for r
                                                in range(1, len(self.all_events) + 1))
        independent_a_or_b = [a_or_b for a_or_b in subsets if self.is_independent(a_or_b, self.independent)]
        for a, b in itertools.product(independent_a_or_b, independent_a_or_b):
            if self.is_causal((a, b), self.causal):
                xl.add((a, b))
        return xl

    def set_YL_set(self):
        yl = copy.deepcopy(self.xl)
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
        for pair in self.parallel:
            if pair == pair[::-1]:  # if we found pairs like (b,b), add b into self-loop sets
                self_loop.add(pair[0])
        to_be_deleted = set()
        for pair in yl:
            if self.contains(pair, self_loop):
                to_be_deleted.add(pair)
        for pair in to_be_deleted:
            yl.discard(pair)
        return yl

    def set_xor_split(self):
        xor_split = set()
        for pair in self.independent:
            for event in self.all_events:
                if (event, pair[0]) in self.causal and (event, pair[1]) in self.causal:
                    xor_split.add(pair)
        return xor_split

    def set_xor_join(self):
        xor_join = set()
        for pair in self.independent:
            for event in self.all_events:
                if (pair[0], event) in self.causal and (pair[1], event) in self.causal:
                    xor_join.add(pair)
        return xor_join

    def set_indirect_succession(self, all_events, direct_succession, xor_join, xor_split):
        indirect_succession = set()
        all_permutations = itertools.permutations(all_events, 2)
        for pair in all_permutations:
            for trace in self.log:
                if pair[0] in trace and pair[1] in trace and trace.index(pair[0]) < trace.index(pair[1]) + 1 and\
                        pair not in direct_succession:
                    for x in range(trace.index(pair[0]), trace.index(pair[1])):
                        if (trace[x], pair[0]) not in xor_join and (trace[x], pair[0]) not in xor_split:
                            indirect_succession.add(pair)
        return indirect_succession

    def set_w1(self):
        w1 = set()
        all_permutations = itertools.permutations(self.all_events, 2)
        for pair in all_permutations:
            if pair not in self.direct_succession:
                for event in self.all_events:
                    places = []
                    for place in self.all_places:
                        if event in place.outs:
                            places.append(place)
                    if len(places) >= 2:
                        all_places_permutations = itertools.permutations(places, 2)
                        for perm in all_places_permutations:
                            if pair[0] in perm[0].ins and pair[0] not in perm[1].ins and pair[1] in perm[1].outs:
                                for t in perm[1].ins:
                                    if (t, pair[0]) not in self.succession and (t, pair[0]) not in self.parallel:
                                        w1.add(pair)
        return w1

    def set_idw1(self):
        idw1 = set()
        for a in self.t_prim:
            for b in self.t_prim:
                if (a, b) in self.w1:
                    idw1.add((a, b))
        return idw1

    # krok 9
    def set_pw_l1l(self):
        return self.set_places(Alpha(self.w_l1l).yl)

    def set_tw_l1l(self):
        return Alpha(self.w_l1l).all_events

    # krok 10 i 11
    def set_idw2(self):
        idw2 = set()
        as_causal = self.idw1.union(self.causal)
        as_indirect_succession = self.set_indirect_succession(self.t_prim, self.direct_succession, self.xor_join,
                                                              self.xor_split)
        as_succession = self.set_succession(as_causal, as_indirect_succession)
        as_w2_1 = self.set_w2_1(self.t_prim, as_indirect_succession, self.all_places, as_succession, self.parallel,
                                self.xor_split)
        as_w2_2 = self.set_w2_1(self.t_prim, as_indirect_succession, self.all_places, as_succession, self.parallel,
                                self.xor_join)
        as_w2 = self.set_w2(as_w2_1, as_w2_2)
        for a in self.t_prim:
            for b in self.t_prim:
                if (a, b) in as_w2:
                    idw2.add((a, b))
        return idw2

    def eliminate_by_rule_1(self, idw2):
        new_idw2 = idw2
        for a in self.all_events:
            for b in self.all_events:
                for c in self.all_events:
                    if (a, b) in new_idw2 and (a, c) in new_idw2 and (b, c) in self.succession:
                        new_idw2.remove((a, c))
        return new_idw2

    # krok 12
    @staticmethod
    def set_w2_1(all_events, indirect_succession, all_places, succession, parallel, xor_split):
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
                                        if not ((t, pair[1]) in succession or (t, pair[1]) in parallel) and\
                                                ((t_prim, event) in succession or (t_prim, event) in parallel):
                                            w2_1.add(pair)
        return w2_1

    @staticmethod
    def set_w2_2(all_events, indirect_succession, all_places, succession, parallel, xor_join):
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
                                        if not ((pair[0], t) in succession or (pair[0], t) in parallel) and\
                                                ((event, t_prim) in succession or (event, t_prim) in parallel):
                                            w2_2.add(pair)
        return w2_2

    @staticmethod
    def set_w2(w2_1, w2_2):
        w2 = w2_1.union(w2_2)
        return w2

    def set_xw_12(self):
        pw_l1l = self.pw_l1l
        As = []
        Bs = []
        xw_12 = set()
        for place in pw_l1l:
            As.append(place.ins)
            Bs.append(place.outs)
        for A, A2 in zip(As,As[1:]):
            for B, B2 in zip(Bs, Bs[1:]):
                if len(list(set(A2).union(B2))) > 0 and len(list(set(A).intersection(A2))) == 0 and\
                        len(list(set(B).intersection(B2))) == 0:
                    for a in A:
                        for a2 in A2:
                            for b in B:
                                for b2 in B2:
                                    for b_b2 in list(set(B).union(B2)):
                                        if ((a, b2) in self.w1 or (a, b2) in self.w2) and\
                                                ((a, b_b2) in self.w1 or (a, b_b2) in self.w2) and\
                                                (a2, a) in self.independent and\
                                                (a2, a) not in self.indirect_succession and\
                                                (b, b2) in self.independent and (b, b2) not in self.indirect_succession:
                                            ins = list(set(A).union(A2))
                                            outs = list(set(B).union(B2))
                                            xw_12.add(Place(ins, outs))
        return xw_12

    # krok 13
    def set_yw(self):
        xw = self.xw_12
        pw_l1l = self.pw_l1l
        yw = set()
        a_prim = []
        b_prim = []
        for place in xw:
            if place.ins not in a_prim:
                a_prim.append(place.ins)
            if place.outs not in b_prim:
                b_prim.append(place.outs)
        for place in pw_l1l:
            if place.ins not in a_prim:
                a_prim.append(place.ins)
            if place.outs not in b_prim:
                b_prim.append(place.outs)
        for a in a_prim:
            for b in b_prim:
                new_place = Place(a, b)
                if new_place in xw or new_place in pw_l1l:
                    yw.add(new_place)
        return yw

    # krok 14 i 15
    def set_idw3(self):
        idw3 = set()
        as_causal = self.idw2.union(self.causal)
        as_indirect_succession = self.set_indirect_succession(self.t_prim, self.direct_succession, self.xor_join,
                                                              self.xor_split)
        as_succession = self.set_succession(as_causal, as_indirect_succession)
        as_w3 = self.set_w3(self.t_prim, as_indirect_succession, self.pw_l1l, as_succession, self.parallel)
        for a in self.t_prim:
            for b in self.t_prim:
                if (a, b) in as_w3:
                    idw3.add((a, b))
        return idw3

    def eliminate_by_rule_2(self, idw3):
        new_idw3 = idw3
        for a in self.all_events:
            for b in self.all_events:
                for trace in self.all_events:
                    for x, y, in zip(trace, trace[1:]):
                        if (a, b) in new_idw3 and (a, x) in new_idw3 and (x, y) in new_idw3 and (y, b) in new_idw3:
                            new_idw3.remowe((a, b))
        return new_idw3

    def set_w3(self, all_events, indirect_succession, all_places, succession, parallel):
        w3 = set()
        all_permutations = itertools.permutations(all_events, 2)
        for pair in all_permutations:
            for a_prim in all_events:
                for b_prim in all_events:
                    if pair in indirect_succession and (a_prim, b_prim) in indirect_succession and\
                            (pair[0], b_prim) not in indirect_succession and\
                            (a_prim, pair[1]) not in indirect_succession:
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
                        if len(a_common_part) > 0 and len(b_common_part) > 0 and\
                                set(b_in_places).issubset(set(b_prim_in_places)):
                            for t in all_events:
                                if (pair[0], t) not in indirect_succession and (a_prim, t) in indirect_succession and\
                                        ((b_prim, t) in parallel or (b_prim, t) in succession):
                                    t_in_places = []
                                    for t_place in all_places:
                                        if t in t_place.outs:
                                            t_in_places.append(t_place)
                                    b_t_common_part = list(set(b_in_places).intersection(t_in_places))
                                    if len(b_t_common_part) > 0:
                                        w3.add(pair)
        return w3

    # krok 16
    def set_xw_16(self):
        xw_16 = set()
        for a in self.t_prim:
            for b in self.t_prim:
                if (a, b) in self.idw3:
                    ins = [a]
                    outs = [b]
                    for event in self.t_prim:
                        if (a, event) in self.independent and (event, b) in self.idw3:
                            ins.append(event)
                        if (b, event) in self.independent and (a, event) in self.idw3:
                            outs.append(event)
                    xw_16.add(Place(ins, outs))
        return xw_16

    # krok 17
    def set_zw(self):
        xw = self.xw_16
        zw = set()
        a_prim = []
        b_prim = []
        for place in xw:
            if place.ins not in a_prim:
                a_prim.append(place.ins)
            if place.outs not in b_prim:
                b_prim.append(place.outs)
        for a in a_prim:
            for b in b_prim:
                new_place = Place(a, b)
                if new_place in xw:
                    zw.add(new_place)
        return zw

    # krok 18
    def set_pw(self):
        pw = self.yw.union(self.zw)
        for triplet in self.lw:
            new_place = Place(triplet[0], triplet[1])
            if new_place in pw:
                pw.remove(new_place)
        for triplet in self.lw:
            ins = [triplet[0]].append(triplet[2])
            outs = [triplet[1]].append(triplet[2])
            new_place = Place(ins, outs)
            pw.add(new_place)
        return pw

    # krok 19
    def set_tw(self):
        tw_l1l = Alpha(self.log).all_events
        for pair in self.l1l:
            tw_l1l.union(set(pair[0][0]))
        return tw_l1l

    def set_start_events(self):
        start_events = set()
        for row in self.log:
            start_events.add(row[0])
        return start_events

    def set_end_events(self):
        end_events = set()
        for row in self.log:
            end_events.add(row[-1])
        return end_events


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

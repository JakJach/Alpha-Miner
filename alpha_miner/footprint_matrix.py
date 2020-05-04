from enum import IntEnum
import numpy as np

relations = [
    {"name": "NONE", "sign": str('#'), "value": 0},
    {"name": "BASIC", "sign": str('>'), "value": 1},
    {"name": "CAUSAL", "sign": str('->'), "value": 2},
    {"name": "CAUSAL_INV", "sign": str('<-'), "value": 3},
    {"name": "PARALLEL", "sign": str('||'), "value": 4},
]


class FootprintMatrix:
    def __init__(self, log):
        self._matrix = []
        self._events = []
        if log:
            self._events = self.init_events(log)
            self._matrix = self.init_matrix(log)

    @property
    def events(self):
        return self._events

    @property
    def matrix(self):
        return self._matrix

    @staticmethod
    def init_events(log):
        all_events = []
        for row in log:
            for event in row:
                if event not in all_events:
                    all_events.append(event)
        all_events = sorted(all_events)
        return all_events

    def init_matrix(self, log):
        events = self.events
        matrix = np.zeros((len(events), len(events)), dtype=IntEnum)
        basics = []
        causals = []
        parallels = []
        for row in log:
            for a, b in enumerate(row):
                for x, y in enumerate(row):
                    if x == a + 1:
                        print(b, y)
                        matrix[events.index(b)][events.index(y)] = 1
                        basics.append([b, y])
                    if x == a:
                        matrix[events.index(b)][events.index(y)] = 0
        for row in log:
            for a, b in enumerate(row):
                for x, y in enumerate(row):
                    if [b, y] in basics and [b, y] not in causals:
                        if [y, b] not in basics:
                            causals.append([b, y])
                            matrix[events.index(b)][events.index(y)] = 2
                            matrix[events.index(y)][events.index(b)] = 3
                        elif [b, y] not in parallels and [y, b] not in parallels:
                            parallels.append([b, y])
                            matrix[events.index(b)][events.index(y)] = 4
                            matrix[events.index(y)][events.index(b)] = 4
        return matrix

    def show(self):
        result = np.zeros((len(self.events) + 1, len(self.events) + 1), dtype=object)
        result[0][0] = 'x'
        result[0][1:len(self.events) + 1] = self.events
        for x in range(len(self.events)):
            result[x + 1][0] = self.events[x]
            for y in range(len(self.events)):
                result[x + 1][y + 1] = relations[self.matrix[x][y]]["sign"]
        print(result)

    @staticmethod
    def get_relation_type(f_matrix, a, b):
        if a not in f_matrix.events or b not in f_matrix.events:
            raise ('One of the events: {0}, {1} does not exist in this log'.format(a,b))
        else:
            a_index = f_matrix.events.index(a)
            b_index = f_matrix.events.index(b)
            return relations[f_matrix.matrix[a_index][b_index]]["name"]


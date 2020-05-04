import footprint_matrix


class AlphaMiner:
    def __init__(self, log):
        self._start_events = []
        self._end_events = []
        self._footprint_matrix = []
        if log:
            self._footprint_matrix = footprint_matrix.FootprintMatrix(log)
            self._start_events = self.init_events(log)[0]
            self._end_events = self.init_events(log)[1]

    @staticmethod
    def init_events(log):
        start_events = []
        end_events = []

        for row in log:
            if row[0] not in start_events:
                start_events.append(row[0])
            if row[-1] not in end_events:
                end_events.append(row[-1])

        start_events = sorted(start_events)
        end_events = sorted(end_events)

        return [start_events, end_events]

    @property
    def events(self):
        return self._footprint_matrix.events if self._footprint_matrix else []

    @property
    def start_events(self):
        return self._start_events if self._start_events else []

    @property
    def end_events(self):
        return self._end_events if self._end_events else []

    @property
    def matrix(self):
        return self._footprint_matrix.matrix

    def show(self):
        self._footprint_matrix.show()

    def get_relation_type(self, a, b):
        return footprint_matrix.FootprintMatrix.get_relation_type(self._footprint_matrix, a, b)
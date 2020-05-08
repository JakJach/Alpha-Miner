class PetriNet():
    def __init__(self):
        self.places = []
        self.transitions = []
        self.input = []
        self.output = []

    def __str__(self):
        pn = []
        pn.append("Places: {}".format(self.places))
        pn.append("Transitions: {}".format(self.transitions))
        pn.append("Input: {}".format(self.input))
        pn.append("Output: {}".format(self.output))
        return '\n'.join(pn)

    def generate_with_alpha(self, alpha_model, dotfile='pn.dot'):
        self.transitions = alpha_model.all_events
        self.input = alpha_model.start_events
        self.output = alpha_model.end_events
        iso = self.__isolated_transitions(alpha_model)
        digraph = self.__pn_description(alpha_model.yl, alpha_model.start_events, alpha_model.end_events, iso)
        with open(dotfile, 'w') as f:
            f.write(digraph)

    def __pn_description(self, yl, ti, to, iso):
        pn = []
        pn.append("digraph pn {")
        pn.append("rankdir=LR;")
        for c in iso:
            pn.append('"{}" [shape=box];'.format(c))
        for pair in yl:
            for i in pair[0]:
                pn.append('"{}" -> "P({})";'.format(i, pair))
                pn.append('"{}" [shape=box];'.format(i))
                pn.append('"P({})" [shape=circle];'.format(pair))
            for i in pair[1]:
                pn.append('"P({})" -> "{}";'.format(pair, i))
                pn.append('"{}" [shape=box];'.format(i))
        for i in ti:
            pn.append("In -> {}".format(i))
        for o in to:
            pn.append("{} -> Out".format(o))
        pn.append("}")
        return '\n'.join(pn)

    def __isolated_transitions(self, alpha_model):
        tl = alpha_model.all_events
        yl = alpha_model.pw_to_pn
        ti = alpha_model.start_events
        to = alpha_model.end_events

        yl_transitions = set()
        if yl:
            for pair in yl:
                # yl is like: {(('a',), ('b',)), (('b',), ('d',))}
                for p in pair:
                    yl_transitions.add(p[0])

        appeared = ti | to | yl_transitions  # "|" for set union
        iso = tl - appeared
        return iso
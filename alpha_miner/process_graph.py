import graphviz


class ProcessGraph(graphviz.Digraph):

    def __init__(self, *args):
        super(ProcessGraph, self).__init__(*args)
        self.graph_attr['rankdir'] = 'LR'
        self.node_attr['shape'] = 'Mrecord'
        self.graph_attr['splines'] = 'ortho'
        self.graph_attr['nodesep'] = '0.8'
        self.edge_attr.update(penwidth='2')
        self.engine = 'neato'

    def add_event(self, name):
        super(ProcessGraph, self).node(name, shape="circle", label="")

    def add_and_gateway(self, *args):
        super(ProcessGraph, self).node(*args, shape="diamond",
                                       width=".6", height=".6",
                                       fixedsize="true",
                                       fontsize="10", label="AND")

    def add_xor_gateway(self, *args, **kwargs):
        super(ProcessGraph, self).node(*args, shape="diamond",
                                       width=".6", height=".6",
                                       fixedsize="true",
                                       fontsize="10", label="XOR")

    def add_and_split_gateway(self, source, targets, *args):
        gateway = 'ANDs ' + str(source) + '->' + str(targets)
        self.add_and_gateway(gateway, *args)
        super(ProcessGraph, self).edge(source, gateway)
        for target in targets:
            super(ProcessGraph, self).edge(gateway, target)

    def add_xor_split_gateway(self, source, targets, *args):
        gateway = 'XORs ' + str(source) + '->' + str(targets)
        self.add_xor_gateway(gateway, *args)
        super(ProcessGraph, self).edge(source, gateway)
        for target in targets:
            super(ProcessGraph, self).edge(gateway, target)

    def add_and_merge_gateway(self, sources, target, *args):
        gateway = 'ANDm ' + str(sources) + '->' + str(target)
        self.add_and_gateway(gateway, *args)
        super(ProcessGraph, self).edge(gateway, target)
        for source in sources:
            super(ProcessGraph, self).edge(source, gateway)

    def add_xor_merge_gateway(self, sources, target, *args):
        gateway = 'XORm ' + str(sources) + '->' + str(target)
        self.add_xor_gateway(gateway, *args)
        super(ProcessGraph, self).edge(gateway, target)
        for source in sources:
            super(ProcessGraph, self).edge(source, gateway)
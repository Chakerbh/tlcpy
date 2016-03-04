import networkx as nx 
import graphviz


class Graphvz():
    def __init__(self, automaton):
        self.g = graphviz.Digraph(format="png")
        self.states = set()
        # Set the direction of the graph
        self.g.body.extend(['rankdir=LR', 'size="8,5"'])
        # Set the shape for the finals states and add them
        self.g.attr('node', shape='doublecircle')
        d = nx.get_node_attributes(automaton.G, 'final')
        for node, value in dict(d).items():
            # If the the state is final add it now else it will be added later 
            if value: 
                print(node)
                self.add_state(str(node))
        self.g.attr('node', shape='circle')
        # Add the states and arcs (edges) between them
        for from_state, to_state, data in automaton.G.edges_iter(data=True):
            self.add_edge(from_state, data['symbol'], to_state)
        self.g.attr('node', shape='none')
        self.add_edge("", "", "1")
        # Set the shape for other states

    def add_state(self, state_number):
        if state_number not in self.states:
            self.states.add(state_number)
            self.g.node(str(state_number))

    def add_edge(self, from_state, label, to_state):
        """ if one (or both) state don't exist add them """
        self.add_state(from_state)
        self.add_state(to_state)
        self.g.edge(str(from_state), str(to_state), label)
    
    def draw(self):
        self.g.view()
        
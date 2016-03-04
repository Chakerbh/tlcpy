import networkx as nx

class Automaton():
    def __init__(self, alphabet =(), string=None):
        self.alphabet = set(alphabet)
        self.G = nx.MultiDiGraph()
        self.states = []
        
    def add_state(self, state_number):
        """ Add the states if not already exist. """ 
        if state_number in self.states:
            return
        self.states.append(state_number)
        self.G.add_node(state_number, {"final": False})
        
    def add_transition(self, from_state, symbol, to_state):
        # Check if both states exists else add theme
        self.add_state(from_state)
        self.add_state(to_state)
        # Add the symbol to the alphabet 
        self.alphabet.add(symbol)
        # adding a edge from 'from_state' to 'to_state'
        self.G.add_edge(from_state, to_state, symbol=symbol)

    def set_state_final(self, state_to_set):
        nx.set_node_attributes(self.G, "final", {state_to_set: True})
    
    def get_all_transition_symbols(self, state):
        """ Iterator over all transition from state """
        symbols = ""
        for i in self.G.edges_iter(data=True):
            if i[0] == state:
                symbols+=i[2]['symbol']
        return symbols
    
    def get_next_state(self,state, symbol):
        for i in self.G.edges_iter(state, True):
            if i[2]['symbol'] == symbol :
                return i[1]

    def get_list_of_final(self, final=True):
        """ Return list of all final states in the graph """ 
        return [u for u,v in nx.get_node_attributes(self.G, 'final').items() if (v and final) or not(v or final)]

    def complet(self):
        """ Return a new complet Automaton """  
        new_state_number = max(self.states)+1
        self.add_state(new_state_number)
        automaton_complet = True
        for state in range(1, new_state_number+1):
            for letter in self.alphabet:
                all_transition = self.get_all_transition_symbols(state)
                if letter not in all_transition:
                    self.add_transition(state, letter,new_state_number)
                    automaton_complet = False
        if automaton_complet:
            self.G.remove_node(new_state_number)

    def get_moves(self, states):
        """ Return a list of list of transition that can be achieved from set of states"""
        result = []
        # Iterate over all letter in the alphabet in order
        # (We need the result ordered in the letters 
        for letter in sorted(self.alphabet):
            l = []
            # iterate over all edges in the graph and check if ther're
            # a edged from one of the states noted by the current letter
            for fr, to, data in self.G.edges_iter(data=True):
                # add the state if not already in the list 
                if fr in states and data["symbol"] == letter and to not in l:
                    l.append(to)
            # Append a sorted version of the list else it will differ determinization process
            result.append(sorted(l))
        return result

    def determinaze(self):
        """ Return a Automaton (using the algorithm we used in the course) 
            This implementation is very straight forward and can be done more efficiently 
            """ 
        # extract the new sets 
        states_waiting = [[1]]
        finished_states = []
        finish = []
        while len(states_waiting):
            iter_state = states_waiting[0]
            states_waiting = states_waiting[1:]
            moves = self.get_moves(iter_state)
            finished_states.append(iter_state)
            for move in moves:
                # If the move is waiting or already treated skip it
                if move not in finished_states and move not in states_waiting:
                    states_waiting.append(move)
            finish.append([iter_state, moves])
            
        # extract new automate
        d = {}
        for i, iteration in enumerate(finish):
            d[tuple(iteration[0])] = i+1
#         print(d)
        
        a = Automaton()
        alpha = sorted(self.alphabet)
        for i in finish:
#             print(i[1])
            for j in range(len(i[1])):
                a.add_transition(d[tuple(i[0])], alpha[j], d[tuple(i[1][j])] )
        states_final = nx.get_node_attributes(self.G, 'final')
        for key, value in d.items():
            for state in key:
                if states_final[state]:
#                     print(state, value) 
                    a.set_state_final(value)
        
        # Return the new automaton 
        return a
    

    def optimaze(self):
        """
        Optimize the automaton using Hopcroft algorithm 
        https://en.wikipedia.org/wiki/DFA_minimization#Hopcroft.27s_algorithm 
        
        return : New optimized automaton.
        """
        
        final = self.get_list_of_final()
        not_final = self.get_list_of_final(False)
        # Using frozenset since we will use set of sets. and we won't change it's value
        p = {frozenset(final), frozenset(not_final)}
        w = {frozenset(final)}

        while len(w):
            a = w.pop()
            x = set()
            for symbol in self.alphabet:
                x = {node for node in self.G.nodes_iter() if self.get_next_state(node, symbol) in a}
                # using set(p) instead of p since we will change it (the same for w).
                for y in set(p):
                    inter = x.intersection(y)
                    dif = y.difference(x)
                    if inter and dif :
                        p.remove(y)
                        p.add(frozenset(inter))
                        p.add(frozenset(dif))
                        if y in set(w):
                            w.remove(y)
                            w.add(frozenset(inter))
                            w.add(frozenset(dif))
                        elif len(inter) <= len(dif):
                            w.add(frozenset(inter))
                        else :
                            w.add(frozenset(dif))
        
        d = {}
        # Creation of a new automaton.
        for i, e in enumerate(sorted(p, key= lambda x: min(x))):
            d[e] = i+1
        new_automaton = Automaton()
        for key  in d:
            state = set(key).pop()
            for char in self.alphabet:
                next_state = self.get_next_state(state, char)
                for elem in d:
                    if next_state in elem:
                        to_state = d[elem]
                        break
                new_automaton.add_transition(d[key], char, to_state)
                for e in key:
                    if e in final:
                        new_automaton.set_state_final(d[key])
                        break
        print(new_automaton.G.edges())
        return new_automaton

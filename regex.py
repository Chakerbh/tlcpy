from collections import deque
follow_pos = {}

def _followers(node):
    if len(node.child) == 2 :
        for i in node.child[1]._last_pos:
            follow_pos[i] = follow_pos.get(i, set()).union(node.child[0]._first_pos)
    if node.symbol == "*":
        for i in node._last_pos:
            follow_pos[i] = follow_pos.get(i, set()).union(node._first_pos)
            
def _first_pos(node):
    if node.symbol == "§":
        node._first_pos = set()
    if node.pos:
        node._first_pos = {node.pos}.copy()
    if node.symbol == "|":
        node._first_pos = node.child[0]._first_pos.union(node.child[1]._first_pos).copy()
    if node.symbol == ".":
        if node.child[1]._nullable :
            node._first_pos = node.child[0]._first_pos.union(node.child[1]._first_pos).copy()
        else:
            node._first_pos = node.child[1]._first_pos.copy()
    if node.symbol == "*":
        node._first_pos = node.child[0]._first_pos.copy()

def _last_pos(node):
    if node.symbol == "§":
        node._last_pos = set()
    if node.pos:
        node._last_pos = {node.pos}.copy()
    if node.symbol == "|":
        node._last_pos = node.child[0]._first_pos.union(node.child[1]._first_pos).copy()
    if node.symbol == ".":
        if node.child[0]._nullable :
            node._last_pos = node.child[0]._first_pos.union(node.child[1]._first_pos).copy()
        else:
            node._last_pos = node.child[0]._first_pos.copy()
    if node.symbol == "*":
        node._last_pos = node.child[0]._first_pos.copy()

def _nullable(node):
    if node.symbol in "*§":
        node._nullable = True
    if node.pos :
        node._nullable = False
    if node.symbol == "|":
        node._nullable = node.child[0]._nullable or node.child[1]._nullable
    if node.symbol == ".":
        node._nullable = node.child[0]._nullable and node.child[1]._nullable
        
            

class Tree():
    def __init__(self):
        self.child = []
        self._nullable = False
        self._first_pos = set()
        self.symbol = ""
        self.pos = None 

    def add_child(self, child): 
        self.child.append(child)

    def set_symbol(self, symbol):
        self.symbol = symbol
    
    def set_pos(self, pos):
        self.pos = pos

    def __add__(self, other):
        new_tree = Tree()
        new_tree.child.append(self)
        new_tree.child.append(other)
        
        return new_tree
    
    def nullable(self):
        if len(self.child):
            if len(self.child)==2:
                self.child[1].nullable()
            self.child[0].nullable()
            _nullable(self)

    def first_pos(self):
        if len(self.child):
            self.child[0].first_pos()
        if len(self.child)==2:
            self.child[1].first_pos()
        _first_pos(self)
            
    def last_pos(self):
        if len(self.child):
            self.child[0].last_pos()
        if len(self.child)==2:
            self.child[1].last_pos()
        _last_pos(self)

    def followers(self):
        if len(self.child):
            self.child[0].followers()
        _followers(self)
        if len(self.child)==2:
            self.child[1].followers()
                
    def pprint(self): 
        if len(self.child):
            if len(self.child)==2:
                self.child[1].pprint()
            self.child[0].pprint()
#         print(self._first_pos, self.symbol,self._last_pos, self._nullable)
        print( self.symbol)
        
#         print(self.symbol, self.first_pos(), self.nullable())
    
class Regex():
    def __init__(self, regex):
        self.regex = regex

    def _add_concatenation(self):
        result = self.regex[0]
        for char in self.regex[1:]:
            if char in ".*|)" or result[-1] in ".|(":
                result+= char
            else:
                result+="."+char
        self.regex =  result

    def regex_to_postfix(self):
        # Add "." in place of concatenation
        self._add_concatenation()
        result = ""
        stack = deque()
        for char in self.regex:
            if char in "*.|()":
                if len(stack) == 0:
                    stack.append(char)
                else:
                    if char == ")" :
                        c = stack.pop()
                        while c!= "(":
                            result += c 
                            c = stack.pop()
                    elif char == "(":
                        stack.append(char) 
                    else:
                        if char == "*":
                            result+= char + stack.pop()
                        elif char == "." and stack[-1] == "*":
                            result += stack.pop()
                            stack.append(char)
                        else:
                            stack.append(char)
            else :
                result += char
        while len(stack):
            result+= stack.pop()
        self._postfix_regex = result
    
    def regex_to_tree(self):
        stack = deque()
        counter = 1
        for char in self._postfix_regex+"#.":
            if char in ".|" :
                a = stack.pop()
                b = stack.pop()
                c = a+b
                c.set_symbol(char)
                stack.append(c)
            elif char == "*":
                a = Tree()
                a.add_child(stack.pop())
                a.set_symbol(char)
                stack.append(a)
            else:
                a = Tree()
                a.set_symbol(char)
                if char != "§":
                    a.set_pos(counter)
                    counter += 1
                stack.append(a)

                
        return stack.pop()
                
if __name__ == '__main__':
    a = Regex("(a|b)*a")
    a._add_concatenation()
    a.regex_to_postfix()
    print(a.regex)
    print(a._postfix_regex)
    b = a.regex_to_tree()
    b.nullable()
    b.first_pos()
    b.last_pos()
    b.pprint()
    b.followers()
    print(follow_pos)
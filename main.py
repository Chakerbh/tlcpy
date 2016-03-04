from tlc import Automaton
from kivy.uix.button import Button
from kivy.app import App
from kivy.uix.image import Image


from graphvz import Graphvz

""" I need to add function to read the automaton from the user """

def read_automaton():
    print(r"Enter the transantions in the form of ' 1 - char - 2 ' when finish press Enter twice")
    l = 3 
    while l:
        l  = input()
        lis = list(map(str.strip,l.split("-")))
        if len(lis) != 3 : 
            print("Try again please")
        print(lis)

# read_automaton()     
if __name__ == '__main__':

    test = Automaton()
#     test.add_transition(1, 'a', 2)
#     test.add_transition(1, 'b', 3)
#   
#     test.add_transition(2, 'a', 2)
#     test.add_transition(2, 'b', 4)
#   
#     test.add_transition(3, 'b', 3)
#     test.add_transition(3, 'a', 2)
#   
#     test.add_transition(4, 'b', 5)
#     test.add_transition(4, 'a', 2)
#   
#     test.add_transition(5, 'b', 3)
#     test.add_transition(5, 'a', 2)
#   
#     test.set_state_final(5)
    test.add_transition(1, '1', 2)
    test.add_transition(1, '0', 8)
  
    test.add_transition(2, '1', 1)
    test.add_transition(2, '0', 8)
  
    test.add_transition(3, '1', 6)
    test.add_transition(3, '0', 5)
  
    test.add_transition(4, '0', 5)
    test.add_transition(4, '1', 6)
  
    test.add_transition(5, '0', 6)
    test.add_transition(5, '1', 7)
  
    test.add_transition(6, '0', 6)
    test.add_transition(6, '1', 6)
  
    test.add_transition(7, '0', 7)
    test.add_transition(7, '1', 6)
  
    test.add_transition(8, '0', 3)
    test.add_transition(8, '1', 3)
  
    test.set_state_final(6)
    test.set_state_final(7)

#     test.add_transition(1, 'b', 2)
#     test.add_transition(1, 'a', 3)
#     test.add_transition(2, 'a', 2)
#     test.add_transition(2, 'b', 3)
#     test.add_transition(3, 'a', 3)
#     test.add_transition(3, 'b', 3)
#     test.set_state_final(2)
#     test.set_state_final(3)

#     test.add_transition(1, 'a', 2)
#     test.add_transition(1, 'a', 3)
#     test.add_transition(1, 'b', 4)
#     test.add_transition(2, 'b', 4)
#     test.add_transition(3, 'b', 4)
#     test.add_transition(3, 'b', 3)
#     test.set_state_final(4)


#     test.add_transition(1, 'a', 2)
#     test.add_transition(2, 'a', 2)
#     test.add_transition(1, 'a', 4)
#     test.add_transition(4, 'a', 4)
#     test.add_transition(2, 'b', 3)
#     test.add_transition(3, 'b', 3)
#     test.add_transition(4, 'c', 5)
#     test.add_transition(5, 'c', 5)
#     test.set_state_final(3)
#     test.set_state_final(5)
#     graph_test = Graphvz(test)
#     graph_test.draw()
#     a = test.determinaze()
#     test.optimaze()
#     t = Graphvz(test)
#     t.draw()
#     t = Graphvz(test.determinaze().optimaze())
#     t = Graphvz(test.determinaze())
    t = Graphvz(test)


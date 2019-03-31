#============================
#Graph theory Project 
#Regular expression Matching
#Laura Flaherty

#=============================
# Shunting Yard Algorithm
# Laura Flaherty
# http://www.oxfordmathcenter.com/drupal7/node/628


def shunt(infix):
    """The shunting yard algorithm for converting infix regular expressions to postfix"""

    # numbers reflect the order of precedence
    # dictionaries are similar to arrays except they are indexed by strings rather than numbers
    specials = {'*': 50, '.': 40, '|': 30}

    pofix = ""
    # put various operators that are not wanted in the pofix
    stack = ""

    #Loop through the string a character at a time
    for c in infix:
        if c == '(':
            # if an open bracket, push to the stack
            stack = stack + c
            # if a closing bracket, pop from stack, push to output until open bracket
        elif c == ')':
            while stack[-1] != '(': 
                pofix,stack = pofix + stack[-1],stack[:-1]
            stack = stack[:-1]
            #if its an operator, push to stack after popping lower or equal precedence
            # operators from the top of the stack into ouput
         
        elif c in specials: # is the character c  in the dictionary
            while stack and specials.get(c,0) <= specials.get(stack[-1],0):
                pofix, stack = pofix + stack[-1], stack[:-1]
             #push this special operator onto the stack           
            stack = stack + c
        else:
        # append the regular characters from the infix to the postfix
            pofix = pofix + c

    while stack:
        pofix, stack = pofix + stack[-1],stack[:-1]

    return pofix
#print(shunt("(a.b)|(c*.d)"))


# Thompson's construction
# Laura Flaherty

# Represents a state with two arrows, labelled by label.
# Use None for a label representing "e" arrows.

class state: 
    label = None
    edge1 = None
    edge2 = None

# new class
class nfa:
 # every nfa represented as an initial state and an accept state
    initial = None 
    accept = None

    # two underscores used because its unique, must use self
    def __init__(self, initial, accept):
        self.initial = initial
        self.accept = accept

# takes a postfix regular expression
def compile(pofix):
    nfastack = [] #stack represented by empty list

    for c in pofix:
        if c == '.':
            # takes the last element out of the list and return that back
            nfa2 = nfastack.pop()
            nfa1 = nfastack.pop()
            # merge nfas
            # connect first NFAS's accept state to the second's initial.
            nfa1.accept.edge1 = nfa2.initial
            # Push NFA to the stack
            newNfa = nfa(nfa1.initial, nfa2.accept)
            nfastack.append(newNfa)
        elif c == '|':
            # pop 2 nfas off the stack.
            nfa2 = nfastack.pop()
            nfa1 = nfastack.pop()
            # Create a new initial state, connect it to initial states
            # of the 2 NFA'S popped from the stack 
            initial = state()
            initial.edge1 = nfa1.initial
            initial.edge2 = nfa2.initial
            # Create a new accept state, connecting the accept states
            # of the two NFA's popped from the stack,  to the new state.
            accept = state()
            nfa1.accept.edge1 = accept
            nfa2.accept.edge1 = accept
            # Push NFA to the stack
            newNfa = nfa(nfa1.initial, nfa2.accept)
            nfastack.append(newNfa)
        elif c == "*":
            # Pop a single NFA from the stack 
            nfa1 = nfastack.pop()
            # Create new initial and accept states.
            accept, initial = state(), state()
            # Join the new initial state to nfa1's initial and accept state.
            initial.edge1 = nfa1.initial
            initial.edge2 = accept
            # Join the old accept state to the new accept state and nfa1's initial state.
            nfa1.accept.edge1 = nfa.initial
            nfa1.accept.edge2 = accept
            # Push new nfa to the stack.
            newNfa = nfa(initial, accept)
            nfastack.append(newNfa)
        else:
            # doesn't have a special character
            #new instance of state class
            accept, initial = state(), state()
            # join the two states with a label
            initial.label = c 
            initial.edge1 = accept 
            # Push new nfa to the stack.
            newNfa = nfa(initial, accept)
            nfastack.append(newNfa)

    # nfastack should only have a single nfa on it at this point
    return nfastack.pop()

#print(compile("ab.cd.|"))
#print(compile("aa.*"))

def followes(state):
    """return the set of states that can be reached from state 
     following e arrows"""
    # Create a new set, with state as its only member.
    states = set()
    states.add(state)

    #Check if state has arrows labelled e from it.
    if state.label is None: 
        # check if edge1 is a state.
        if state.edge1 is not None:
            # if theres an edge1, follow it.
            states |= followes(state.edge1)
        #check if edge2 is a state
        if state.edge2 is not None:
            # if there's an edge2, follow it.
            states |= followes(state.edge2)
    
    # return the set of states.
    return states


def match(infix, string):
    """Matches string to infix regular expression"""

    # shunt and compile the regular expression
    postfix = shunt(infix)
    nfa = compile(postfix)

    # the current set of states and the next set of states.
    current = set()
    next = set()

    # add the initial state to the current set
    current  |= followes(nfa.initial)

    #Loop through each character in the string.
    for s in string:
        # loop through the current set of states.
        for c in current:
            # check if that state us labelled s.
            if c.label ==s:
                # add the edge1 state to the next set.
                next |= followes(c.edge1)
        # set current to next, and clear out next.
        current = next
        next = set()

    # check if the accept state is in the set of current states.
    return (nfa.accept in current)

#A few tests.
infixes = ["a.b.c*","a.(b|d).c*","(a.(b|d))*","a.(b.b)*.c"]
strings = ["", "abc", "abbc", "abcc", "abad", "abbc"]

for i in infixes:
    for s in strings:
        print(match(i, s), i,s)
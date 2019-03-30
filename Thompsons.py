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

print(compile("ab.cd.|"))
#print(compile("aa.*"))
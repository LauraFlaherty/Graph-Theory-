# Shunting Yard Algorithm
# Laura Flaherty
# http://www.oxfordmathcenter.com/drupal7/node/628


def shunt(infix):

    # numbers reflect the order of precedence
    # dictionaries are similar to arrays except they are indexed by strings rather than numbers
    specials = {'*': 50, '.': 40, '|': 30, '+': 50, '?': 50}

    pofix = ""
    # put various operators that are not wanted in the pofix
    stack = ""

    for c in infix:
        if c == '(':
            stack = stack + c
        elif c == ')':
            while stack[-1] != '(': # while the character at the end of the string
                pofix,stack = pofix + stack[-1],stack[:-1]
            stack = stack[:-1]
         # is the character c  in the dictionary
        elif c in specials:
            # while stack is not empty, and specials precendence is less than 
            # or equal to of the last operator on the stack, take the operator 
            # at the top of the stack that has greater precidence than the one 
            # just read from the infix regular expression and push them into 
            # postfix regular expression and pop them off the stack
            while stack and specials.get(c,0) <= specials.get(stack[-1],0):
                pofix, stack = pofix + stack[-1], stack[:-1]
             #push this special operator onto the stack           
            stack = stack + c
        else:
        # append the character from the infix to the postfix
            pofix = pofix + c

    while stack:
        pofix, stack = pofix + stack[-1],stack[:-1]

    return pofix

print(shunt("(a.b)|(c*.d)"))

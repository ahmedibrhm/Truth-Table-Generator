#Truth Table creator

#Argument data structure
class Node():
    def __init__(self, typ, arg1, arg1v, arg2, arg2v, val, sympol, sympolstate):
        self.typ = typ #type of the argument
        self.arg1 = arg1 #argument 1st element
        self.arg1v = arg1v #argument 1st element value
        self.arg2 = arg2 #argument 2nd element
        self.arg2v = arg2v #argument 2nd element value
        self.val = val #argument evaluated value
        self.sympol = sympol #argument sympol - if atomic sentece
        self.sympolstate = sympolstate #argument state (positive or negative)

#initiating starting node for the argument
start = Node(typ = None, arg1 = None, arg1v=None, arg2 = None, arg2v = None, val = None, sympol = None, sympolstate = True)

# basic argument evaluation functions
def Conditional(a,b):
    """
    The function takes input the truth values (boleans) of a conditional sentence and return the truth value of the condition.
    """
    return not a or b

def disjunction(a,b):
    """
    The function takes input the truth values (boleans) of a disjunction sentence and return the truth value of it.
    """
    return a or b

def adjunction(a,b):
    """
    The function takes input the truth values (boleans) of a adjunction sentence and return the truth value of it.
    """
    return a and b

#detecting the type of the simple argument and evaluate it
def evaluatesingle(typ, a, b):
    """
    This argument takes the type of the proposition needs to be implemented and the truth values of its two sides and implement one of the
    evaluation function according to the type.
    """
    if typ == 1:
        return Conditional(a,b)
    if typ == 2:
        return disjunction(a,b)
    if typ == 3:
        return adjunction(a,b)


#function to take a whole argument and organize it - return a node containing the argument
def takearg(argument):
    """
    This function works recrussively to take the argument inputs from the user. It stores
    the argument in a shape of tree to effectively store the order and relations between 
    argument compnents. This function priotrize the depth in storing input from the user. The function began to return when
    it reaches to atomic sentence input.
    """
    print(f"1 - implementation \n2 - disjunction \n3 - adjunction \n4 - atomic sentence")
    types = {
        1 : "implementation",
        2 : "disjunction",
        3 : "adjunction"
    }
    
    #taking input and handling some edge cases
    while True:
        try:
            itype = int(input())
            break
        except ValueError:
            print("Your entered value is incorrect! Try again")
            print(f"1 - Implementation \n2 - Disjunction \n3 - Adjunction \n4 - Atomic sentence")
    argument.typ = itype
    
    #recursion untill reaching to an atomic sentences input
    if argument.typ != 4:
        argument.typ = itype
        if argument.arg1 == None:
            argument.arg1 = Node(typ = None, arg1 = None, arg1v=None, arg2 = None, arg2v = None, val=None, sympol = None, sympolstate = True)
            print(types[argument.typ], "1st argument")
            argument.arg1 = takearg(argument.arg1)
        if argument.arg2 == None:
            print(types[argument.typ], "2nd argument")
            argument.arg2 = Node(typ = None, arg1 = None, arg1v=None, arg2 = None, arg2v = None, val=None, sympol = None, sympolstate = True)
            argument.arg2 = takearg(argument.arg2)
    
    #taking the atomic sentence
    if argument.typ == 4:
        argument = inputsentence(argument)
    
    #returning the final argument
    return argument

#function for inputting atomic sentence from the user
def inputsentence(argument):

    """
    The function executed when the takearg function reaches to atomic sentence input
    it takes the atomic sentence from the user and its state and update the argument then return it.
    """
    print(f"1- positive atomic sentence \n2- negative atomic sentece")
    while True:
        try:
            state = int(input())
            break
        except ValueError:
            print("Your entered value is incorrect! Try again")
            print(f"1- Positive atomic sentence \n2- Negative atomic sentece")
    if state == 2:
        argument.sympolstate = False
    print("atomic sentence letter")
    letter = input()
    argument.sympol = letter
    return argument

#evaluating the whole argument function
def evaluate(argument, atomic):
    """
    This function takes the argument tree and dictionary of the atomic sentences and their truth values
    it then works recrussively by DFS algorithm untill reaching the atomic sentences then it return the values of this atomic sentences
    then it began to evaluate each argument bottom-to-up and update their values to finally return the truth value of the tree(main argument).
    """
    if argument.typ != 4:
        argument.arg1v = evaluate(argument.arg1, atomic)
        argument.arg2v = evaluate(argument.arg2, atomic)
        argument.val = evaluatesingle(argument.typ, argument.arg1v, argument.arg2v)
    if argument.typ == 4:
        argument.val = atomic[argument.sympol]
        if argument.sympolstate == False:
            argument.val = not argument.val
    return argument.val

#generating truth table and check the validity of the argument
def tablegen(atomicsentences, n,argument, rows=[]):
    """
    This function takes the set of atomic sentences, their number, arguments, and list
    The function works recrussivly to generate all combinations of of truth values while tracking the depth of the recurssion
    When n reaches to 0 which means not n, the function knew it has a complete row of truth values and start evaluating the argument.

    """
    if not n:
        atm = {}
        i = 0
        for k in atomicsentences:
            atm[k] = rows[i]
            i += 1
        finalval = evaluate(argument,atm)
        rows = rows+[finalval]
        print(rows)
    else:
        for i in [True, False]:
            tablegen(atomicsentences, n-1, argument, rows+[i])

#naming function
def naming(argument):
    """
    This function takes the argument tree and return translations to the propositional language
    it depends on doing recurssion till reaching the atomic sentence - end of the tree. Then return the propositional langauge of 
    each argument till returning the full translation.
    """
    if argument.typ != 4:
        if argument.typ == 1:
            return f"( {naming(argument.arg1)} -> {naming(argument.arg2)} )"
        elif argument.typ == 2:
            return f"( {naming(argument.arg1)} OR {naming(argument.arg2)} )"
        else:
            return f"( {naming(argument.arg1)} AND {naming(argument.arg2)} )"
    if argument.typ == 4:
        if argument.sympolstate == False:
            return f"NOT {argument.sympol}"
        return argument.sympol


#The Main Function
def main():
    print("enter number of atomic sentences")
    #input taking and handeling different errors
    while True:
        try:
            n = int(input())
            break
        except ValueError:
            print("Your entered value is incorrect! Try again")
            print("Enter number of atomic sentences")

    #input of the set of atomic sentences
    atomic = set()
    for i in range(n):
        print("atomic sentence number", i+1)
        atomic.add(input())

    #taking the argument input and storing it in variable arg
    arg = takearg(start)

    #print the propositional translation to the argument
    print("Argument:", naming(arg))

    #constructing the truth table and printing it.
    for i in atomic:
        print("  ",i, end="  ")
    print("argument")
    tablegen(atomic,n, arg)
    
    return
if __name__ == "__main__":
    main()

"""
The classes of token are keyword, identifier, comparison, float and whitespace etc..
"""
import queue


letter = ('a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',
          'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z')
nzero = ('1','2','3','4','5','6','7','8','9')
zero = ('0')
skip = (" ","\r","\n")
keyword = ('int', 'INT', 'char', 'CHAR', 'if', 'IF', 'else', 'ELSE','while', 'WHILE','return', 'RETURN')
ARITHMETIC = ('MINUS', 'PLUS', 'MULTIPLY', 'DIVIDE')
COMPARISON = ('COMPARISONM', 'COMPARISON')

class DFA:
    state_now = None


    states = []
    finalState = []
    transitionFunction = dict()
    alphabet = []
    startState = ''


    token = ''
    finalStateCondition = False
    q = queue.Queue(100)


    def __init__(self, states, finalState, alphabet, startState, transitionFunction):
        self.states = states
        self.finalState = finalState
        self.transitionFunction = transitionFunction
        self.alphabet = alphabet
        self.state_now = startState
        self.startState = startState

    def transition(self, symbol):
        key = (self.state_now, symbol[1])
        if key in self.transitionFunction:
            self.q.put(symbol[0])

            #change the current state
            self.state_now = self.transitionFunction[key]

            #is this current state a final state
            if self.state_now in self.finalState:
                for i in range(self.q.qsize()):
                    self.token += self.q.get()
                self.finalStateCondition = True

        else :
            #previous state is finalstate and current state is not finalstate
            #print state and then DFA is initialized
            if self.finalStateCondition == True:
                self.removeSpace()
                self.isIdentifier()
                self.isArithmetic()
                self.isComparision()
                print(self.state_now, self.token)
                self.state_now = 'start'
                self.token = ''
                self.finalStateCondition = False
                self.transition(symbol)
            else:
                #exception handling
                print("it's not right input")
                exit(-1)

    def removeSpace(self):
        self.token = self.token.strip()

    def isIdentifier(self):
        if self.state_now == 'IDENTIFIER':
            if self.token in keyword:
                self.state_now = self.token.upper()
            else:
                pass
        else:
            pass
        return

    def isArithmetic(self):
        if self.state_now in ARITHMETIC:
            self.state_now = 'ARITHMETIC'
        return

    def isComparision(self):
        if self.state_now in COMPARISON:
            self.state_now = 'COMPARISON'

    def isthisfinalState(self):
        if self.state_now in self.finalState:
            return True


states = ['start', 'IDENTIFIER', 'MINUS', 'PLUS', 'MULTIPLY', 'DIVIDE', '!', 'COMPARISONM','COMPARISON', 'ASSIGNMENT', 'stringM', 'STRING', 'SEMICOLON', 'LBRACE', 'RBRACE','LPAREN', 'RPAREN', 'COMMA']
finalState = ['INTEGER', 'STRING', 'MINUS', 'PLUS', 'MULTIPLY', 'DIVIDE', 'COMPARISONM','COMPARISON', 'SEMICOLON', 'LBRACE', 'RBRACE', 'LPAREN','RPAREN', 'COMMA','IDENTIFIER', 'ASSIGNMENT']
alphabet = [' ', '\t', '\n', 'letter', 'zero', 'nzero', '-', '+', '*', '/', '!', '=', '<', '>', '\"', ';', '{', '}', '(', ')', ',']
startState = 'start'
trans = dict()

#trnas is transition function
#The feature of trans is trans[(curremt_state, symbol)] = next_state

#DFA for start
trans[('start', ' ')] = 'start'
trans[('start', '\t')] = 'start'
trans[('start', '\n')] = 'start'

#DFA for IDENTIFIER
trans[('start', 'letter')] = 'IDENTIFIER'
trans[('IDENTIFIER', 'letter')] = 'IDENTIFIER'
trans[('IDENTIFIER', 'zero')] = 'IDENTIFIER'
trans[('IDENTIFIER', 'nzero')] = 'IDENTIFIER'

#DFA for Signed INTEGER
trans[('start', '-')] = 'MINUS'
trans[('MINUS', 'nzero')] = 'INTEGER'

trans[('start', 'zero')] = 'INTEGER'
trans[('start', 'nzero')] = 'INTEGER'
trans[('INTEGER', 'zero')] = 'INTEGER'
trans[('INTEGER', 'nzero')] = 'INTEGER'


#DFA for ARITHMETIC
trans[('start', '+')] = 'PLUS'
trans[('start', '*')] = 'MULTIPLY'
trans[('start', '/')] = 'DIVIDE'

#DFA for COMPARISON and ASSIGNMENT
trans[('start', '!')] = '!'
trans[('start', '=')] = 'ASSIGNMENT'
trans[('start', '>')] = 'COMPARISONM'
trans[('start', '<')] = 'COMPARISONM'

trans[('!', '=')] = 'COMPARISON'
trans[('ASSIGNMENT', '=')] = 'COMPARISON'
trans[('COMPARISONM', '=')] = 'COMPARISON'

#DFA for STRING
trans[('start', '\"')] = 'stringM'
trans[('stringM', 'letter')] = 'stringM'
trans[('stringM', 'zero')] = 'stringM'
trans[('stringM', 'nzero')] = 'stringM'
trans[('stringM', ' ')] = 'stringM'
trans[('stringM', '\"')] = 'STRING'




#DFA for SEMICOLON
trans[('start', ';')] = 'SEMICOLON'

#DFA for LBRACE
trans[('start', '{')] = 'LBRACE'

#DFA for RBRACE
trans[('start', '}')] = 'RBRACE'

#DFA for LPAREN
trans[('start', '(')] = 'LPAREN'

#DFA for RPAREN
trans[('start', ')')] = 'RPAREN'

#DFA for COMMA
trans[('start', ',')] = 'COMMA'



#read file and we initialize DFA
filename = "test.c"
f = open(filename, 'r')
data = f.read()
data += ' '
dfa = DFA(states, finalState, alphabet, startState, trans)

#If c is letter or zero or nzero, we append the alphabet of  c ( ex) letter, zero, nzero)
def isitletterOrdigit(c):
    set = [c]
    if c in letter:
        set.append('letter')
    elif c in zero:
        set.append('zero')
    elif c in nzero:
        set.append('nzero')
    else:
        set.append(c)
    return set

#Input data into trasition function
for c in data:
    dfa.transition(isitletterOrdigit(c))

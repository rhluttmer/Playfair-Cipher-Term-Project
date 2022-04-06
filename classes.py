class Digraph(object):
    def __init__(self, letter1, letter2):
        self.let1 = letter1
        self.let2 = letter2
        self.encryptsTo = None
        self.decryptsTo = None
    
    def reverse(self):
        return Digraph(self.let2, self.let1)
    
    def __eq__(self, other):
        return (isinstance(other, Digraph) and self.let1 == other.let1 
                and self.let2 == other.let2)
    
    def __repr__(self):
        return f'({self.let1}, {self.let2})'

    def __hash__(self):
        return hash((self.let1, self.let2))

class Letter(object):
    def __init__(self, letterName):
        self.name = letterName
        self.encryptsTo = set()
        self.succeeds = set()
        self.proceeds = set()
        self.inSameRow = set()
        self.inSameCol = set()

    def __repr__(self):
        return (f'{self.name}, encrypts to {self.encryptsTo}, ' + 
                f'row with {self.inSameRow}, col with {self.inSameCol}, ' + 
                f'succeeds {self.succeeds}, proceeds {self.proceeds}')

    # This is just so we can check that a letter is not equal to 0
    def __eq__(self, other):
        if not isinstance(other, Letter):
            return False
        
        return self.name == other.name


    # Approximates how much we know about letter
    # Useful to decide where to start backtracking
    def amountOfInfo(self):
        return (3*len(self.succeeds) + 3*len(self.proceeds) 
                + len(self.inSameRow) + len(self.inSameCol))
     
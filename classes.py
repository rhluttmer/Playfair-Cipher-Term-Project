# Rose Luttmer

'''
Defines the classes used in algorithmic playfair files (everything but graphics)

Digraph class stores pairs of letters
Letter class stores a sinlge letter

'''

# Used to store pairs of letters
class Digraph(object):
    def __init__(self, letter1, letter2):
        self.let1 = letter1
        self.let2 = letter2

    # Make a new digraph that is the reverse of the first one
    def reverse(self):
        return Digraph(self.let2, self.let1)
    
    def __eq__(self, other):
        return (isinstance(other, Digraph) and self.let1 == other.let1 
                and self.let2 == other.let2)
    
    def __repr__(self):
        return f'{self.let1}{self.let2}'

    def __hash__(self):
        return hash((self.let1, self.let2))

# Stores a single letter, sued for cracking
class Letter(object):
    def __init__(self, letterName):
        self.name = letterName

        # All of these are modified later
        self.encryptsTo = set()
        self.inSameRow = set()
        self.inSameCol = set()

    # I have all info included to make debugging easier
    def __repr__(self):
        return (f'{self.name}, encrypts to {self.encryptsTo}, ' + 
                f'row with {self.inSameRow}, col with {self.inSameCol}')

    # This is just so we can check that a letter is not equal to 0
    # It is never actually used to check if two letters are equal
    def __eq__(self, other):
        if not isinstance(other, Letter):
            return False
        
        return self.name == other.name


     
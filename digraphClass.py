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

from numpy import poly1d
from scipy.signal import *
from typing import Union
numbers = Union[float, int]


class DialogBlock:
    
    def __init__(self, num, den = [1]):
        self.num = poly1d(num, variable='s')
        self.den = poly1d(den, variable='s')
    
    def __repr__(self) -> str:
        if len(self.den) > 0:
            return f"DialogBlock({list(self.num)} / {list(self.den)})"
        else:
            return f"DialogBlock({list(self.num)})"
    
    def __neg__(self) -> 'DialogBlock':
        return DialogBlock(-self.num, self.den)
    
    def __add__(self, db: Union['DialogBlock', numbers]) -> 'DialogBlock':
        if type(db) == DialogBlock:
            #DialogBlock
            num_first = self.num * db.den
            num_second = self.den * db.num
            den = self.den * db.den
            num = num_first + num_second
        else:
            #Number
            num = self.num + self.den * db
            den = self.den
        return DialogBlock(num, den)
    
    def __radd__(self, db: Union['DialogBlock', numbers]) -> 'DialogBlock':
        return self + db
    
    def __sub__(self, db: Union['DialogBlock', numbers]) -> 'DialogBlock':
        return self + (-db)
    
    def __mul__(self, db: Union['DialogBlock', numbers]) -> 'DialogBlock':
        if type(db) == DialogBlock:
            #DialogBlock
            num = self.num * db.num
            den = self.den * db.den
        else:
            #Number
            num = self.num * db
            den = self.den
        return DialogBlock(num, den)
    
    def __rmul__(self, db: Union['DialogBlock', numbers]) -> 'DialogBlock':
        return self * db
    
    def __truediv__(self, db: Union['DialogBlock', numbers]) -> 'DialogBlock':
        if type(db) == DialogBlock:
            #DialogBlock
            num = self.num * db.den
            den = self.den * db.num
        else:
            #Number
            num = self.num
            den = self.den * db
        return DialogBlock(num, den)
    
    def series(self, db: 'DialogBlock') -> 'DialogBlock':
        return self * db
    
    def paralell(self, db: 'DialogBlock') -> 'DialogBlock':
        return self + db
    
    def feedback(self, db: Union['DialogBlock', numbers]) -> 'DialogBlock':
        if db in (1, -1):
            return self.cloop(db == 1)
        return self / (self * db + 1)
    
    def cloop(self, reversed=True) -> 'DialogBlock':
        return DialogBlock(
            self.num,
            self.num + (self.den if reversed else -self.den)
        )
        

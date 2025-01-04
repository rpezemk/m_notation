from enum import Enum
from functools import cmp_to_key

from math import gcd



    


class Ratio():
    def LONGA(): return Ratio(t=(4,1))               # 4 times a whole note
    def BREVE(): return Ratio(t=(2,1))               # 2 times a whole note
    def WHOLE(): return Ratio(t=(1,1))               # 1 whole note
    def HALF(): return Ratio(t=(1,2))                # 1/2 of a whole note
    def QUARTER(): return Ratio(t=(1,4))             # 1/4 of a whole note
    def EIGHTH(): return Ratio(t=(1,8))              # 1/8 of a whole note
    def SIXTEENTH(): return Ratio(t=(1,16))          # 1/16 of a whole note
    def THIRTY_SECOND(): return Ratio(t=(1,32))      # 1/32 of a whole note
    def SIXTY_FOURTH(): return Ratio(t=(1,64))      
    
    def get_all_durations():
        all_durations = [
            Ratio.LONGA(),
            Ratio.BREVE(),
            Ratio.WHOLE(),
            Ratio.HALF(),
            Ratio.QUARTER(),
            Ratio.EIGHTH(),
            Ratio.SIXTEENTH(),
            Ratio.THIRTY_SECOND(),
            Ratio.SIXTY_FOURTH(),
        ]
        return all_durations
    
    def __init__(self, *, numerator: int = 1, denominator: int = 1, t: tuple[int, int] = None):
        if t is not None:
            numerator = t[0]
            denominator = t[1]
        self.numerator = numerator
        self.denominator = denominator

    def __hash__(self):
        return hash(self.simplify().to_float())
    
    def __lt__(self, other: 'Ratio'):
        res = self.numerator * other.denominator < other.numerator * self.denominator
        return res

    def __gt__(self, other: 'Ratio'):
        res = self.numerator * other.denominator > other.numerator * self.denominator
        return res

    def __le__(self, other: 'Ratio'):
        res = self.numerator * other.denominator <= other.numerator * self.denominator
        return res

    def __ge__(self, other: 'Ratio'):
        res = self.numerator * other.denominator >= other.numerator * self.denominator
        return res

    def __eq__(self, other: 'Ratio'):
        res = self.numerator * other.denominator == other.numerator * self.denominator
        return res

    def __ne__(self, other: 'Ratio'):
        res = self.numerator * other.denominator != other.numerator * self.denominator
        return res

    def __add__(self, other: 'Ratio'):
        new_num = (self.numerator * other.denominator + other.numerator * self.denominator)
        new_den = self.denominator * other.denominator
        return Ratio(numerator=new_num, denominator=new_den).simplify()
    
    def __sub__(self, other: 'Ratio'):
        new_num = (self.numerator * other.denominator - other.numerator * self.denominator)
        new_den = self.denominator * other.denominator
        return Ratio(numerator=new_num, denominator=new_den).simplify()

    def __mul__(self, other: 'Ratio'):
        new_num = self.numerator * other.numerator
        new_den = self.denominator * other.denominator
        return Ratio(numerator=new_num, denominator=new_den).simplify()
    
    def __truediv__(self, other: 'Ratio'):
        new_num = self.numerator * other.denominator
        new_den = self.denominator * other.numerator
        return Ratio(numerator=new_num, denominator=new_den).simplify()

    def simplify(self):
        common = gcd(self.numerator, self.denominator)
        self.numerator = self.numerator // common
        self.denominator = self.denominator // common
        return self

    def __str__(self):
        res = f"[{self.numerator}/{self.denominator}]"
        return res

    def custom_comparator(x: 'Ratio', y: 'Ratio'):
        if x < y:
            return -1  # x comes before y
        elif x > y:
            return 1   # x comes after y
        else:
            return 0   # x and y are equal    

    def sort(ratios: list['Ratio']):
        sorted_ratios = sorted(ratios, key=custom_key)
        return sorted_ratios

    def get_lowest(ratios: list['Ratio']) -> tuple[bool, list[int], 'Ratio']:
        if not ratios:
            return False, [], None

        lowest: Ratio = Ratio.sort(ratios)[0]
        res_idxs = [i for i, v in enumerate(ratios) if v == lowest]
        return True, res_idxs, lowest
    
    def to_float(self):
        res = self.numerator / self.denominator
        return res
    
    def clone(self):
        return Ratio(t=(self.numerator, self.denominator))
    
    def zero():
        """
        Returns:
            Ratio(t=(0, 1))
        """
        return Ratio(t=(0, 1))
    
    def one():
        """
        Returns:
            Ratio(t=(1, 1))
        """
        return Ratio(t=(1, 1))
    

    
class Dotting(Enum):
    NO_DOT = Ratio(t=(1,1))
    ONE_DOT = Ratio(t=(3,2))
    TWO_DOTS = Ratio(t=(7,4))
    THREE_DOTS = Ratio(t=(15,8))
    FOUR_DOTS = Ratio(t=(31,16))    
    
custom_key = cmp_to_key(Ratio.custom_comparator)
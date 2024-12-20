from math import gcd

class Ratio():
    def __init__(self, *, numerator: int = 1, denominator: int = 1, t: tuple[int, int] = None):
        if t is not None:
            numerator = t[0]
            denominator = t[1]
        self.numerator = numerator
        self.denominator = denominator 
        
    def __lt__(self, other: 'Ratio'):
        res = self.numerator * other.denominator < other.numerator * self.denominator
        return res
    
    def __gt__(self, other: 'Ratio'):
        res = self.numerator * other.denominator > other.numerator * self.denominator
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
        return Ratio(numerator=new_num, denominator=new_den)
        
    def __sub__(self, other: 'Ratio'):
        new_num = (self.numerator * other.denominator - other.numerator * self.denominator)
        new_den = self.denominator * other.denominator
        return Ratio(numerator=new_num, denominator=new_den)
    
    def simplify(self):
        common = gcd(self.numerator, self.denominator)
        self.numerator = self.numerator // common
        self.denominator = self.denominator // common
        return self
    
    def __str__(self):
        res = f"[{self.numerator}/{self.denominator}]"
        return res

def test_ratios():
        
    check_list = [
        [(4, 8), (2, 4)],
        [(1, 16), (2, 32)],
        [(4, 8), (2, 4)],
        [(2, 8), (2, 4)],
        [(3, 8), (2, 4)],
        ]


    ratio_pairs = [(Ratio(t=x), Ratio(t=y)) for (x, y) in check_list]
    operations = [
        lambda x, y: "is less than" if x < y else "is not less than",
        lambda x, y: "is greater than" if x > y else "is not greater than",
        lambda x, y: "equals to" if x == y else "is not equal to",
        lambda x, y: "is different to" if x != y else "is not different to",
        ]
    for check in ratio_pairs:
        print(check[0], 'and', check[1], ":")
        for op in operations:
            res = op(check[0], check[1])
            print("    ", check[0], res,  check[1])
            

if __name__ == "__main__":
    test_ratios()
from math import gcd
from functools import cmp_to_key

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
        
    
custom_key = cmp_to_key(Ratio.custom_comparator)

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
            

def to_moving_sum(lane: list[Ratio]) -> list[Ratio]:
    curr = Ratio(t=(0, 1))
    res = []
    for r in lane:
        curr = curr + r
        res.append(curr)

    return res


    

def ratio_lanes_to_ruler(lanes: list[list[Ratio]]) -> tuple[list[Ratio], list[Ratio]]:
    curr_pos = Ratio(t=(0, 1))
    moving_sum_lanes = [to_moving_sum(lane) for lane in lanes]        
    mov_sum_ruler = []
    widths_ruler = []
    while True:
        curr_check = []
        mov = [[m for m in mov if m > curr_pos][:1] for mov in moving_sum_lanes]
        if not mov:
            break
        for m in mov:
            if m:
                curr_check.append(m[0])
        
        ok, idxs, lowest = Ratio.get_lowest(curr_check)
        if not ok:
            break
        widths_ruler.append(lowest - curr_pos)
        curr_pos = lowest
        mov_sum_ruler.append(curr_pos)  
    return mov_sum_ruler, widths_ruler

def chunk_widths_by_duration(ratios: list[Ratio], chunk_by: Ratio):
    curr_ratio = Ratio(t=(0, 1))
    res_measures = []
    sub_measure = []
    for r in ratios:
        curr_ratio += r
        if curr_ratio == chunk_by:
            sub_measure.append(r)
            res_measures.append(sub_measure)
            sub_measure = []
            curr_ratio = Ratio(t=(0, 1))
        elif curr_ratio >= chunk_by:
            sub_measure.append(chunk_by - (curr_ratio - r))
            res_measures.append(sub_measure)
            sub_measure = [curr_ratio - chunk_by]
            curr_ratio = Ratio(t=(0, 1))
        else: 
            sub_measure.append(r)
            
    return res_measures


def test_ruler_get():
    check_list1 = [Ratio(t=r) for r in [ (1, 2), (1, 4), (1, 4)]]
    check_list2 = [Ratio(t=r) for r in [ (1, 4), (1, 12), (1, 12), (1, 12), (2, 4)]]
    m_ruler, widths = ratio_lanes_to_ruler([check_list1, check_list2])
    print("mov_ruler:")
    for ratio in m_ruler:
        print(ratio, end=" ")
    print("")
    print("widths:")
    for ratio in widths:
        print(ratio, end=" ")
    print("")
    
if __name__ == "__main__":
    # test_ratios()
    test_ruler_get()
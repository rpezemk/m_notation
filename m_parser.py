from enum import Enum

from model.musical.structure import *


note_tokens: list[tuple[str, Callable[[], Note]]] = [
    ("c", Note.C),
    ("d", Note.D),
    ("e", Note.E),
    ("f", Note.F),
    ("g", Note.G),
    ("a", Note.A),
    ("b", Note.B),
    ("!", Rest),
]

acc_tokens: list[tuple[str, Callable[[Note], Note]]] = [
    ("#",  lambda n: n.sharp()),
    ("x",  lambda n: n.double_sharp()),
    ("b",  lambda n: n.flat()),
    ("bb", lambda n: n.double_flat()),
]

ratio_tokens: list[tuple[str, Callable[[Note], Note]]]  = [
    ("r81", lambda n: n.set_base_duration(Ratio.R8_1())), 
    ("r41", lambda n: n.set_base_duration(Ratio.R4_1())), 
    ("r21", lambda n: n.set_base_duration(Ratio.R2_1())), 
    ("r1",  lambda n: n.set_base_duration(Ratio.R1_1())), 
    ("r2",  lambda n: n.set_base_duration(Ratio.R1_2())), 
    ("r4",  lambda n: n.set_base_duration(Ratio.R1_4())), 
    ("r8",  lambda n: n.set_base_duration(Ratio.R1_8())), 
    ("r16", lambda n: n.set_base_duration(Ratio.R1_16())), 
    ("r32", lambda n: n.set_base_duration(Ratio.R1_33())), 
    ("r64", lambda n: n.set_base_duration(Ratio.R1_64())), 
]

number_tokens = [
    ("0", ), 
    ("1", ), 
    ("3", ), 
    ("4", ), 
    ("5", ), 
    ("6", ), 
    ("7", ), 
    ("8", ), 
    ("9", ), 
]

oct_up_down_tokens = [
    ("^", ),
    ("v", ),
]

para_tokens = [("(", ), (")", )]

bar_tokens = [("|", )]

punctuation_tokens: list[tuple[str, Callable[[Note], Note]]] = [
    (".", lambda n: n.dot()),
    ("..", lambda n: n.double_dot()),
    ]

tie_tokens: list[tuple[str, Callable[[Note], Note]]] = [
    ("_", lambda n: n.tie()),
    ]

all_tokens = [
    *note_tokens, 
    *acc_tokens, 
    *ratio_tokens, 
    *para_tokens, 
    *oct_up_down_tokens, 
    *bar_tokens, 
    *punctuation_tokens, 
    *number_tokens
    ]

samples = [
    """r16 d e f g r8 a  ^d  c#   v a  e  g | f# d ^ r4 c.    r16 b a r8 b  g |
e  g  bb  d  c#  a  v a  ^g   | r4 f   e    r16 d c# d e f# g# a b |"""
,

"""r4 t3(c d e) t3(c d r16 e f) d c d e """,
"""r4 cx v dbb t3(c# db ebb) e._ f.. !.. """,
"r4 ebb.._ ebb.."
]


note_symbols = [n[0] for n in note_tokens]
acc_symbols =  [n[0] for n in acc_tokens]
punctuation_symbols =  [n[0] for n in punctuation_tokens]
tie_symbols = [n[0] for n in tie_tokens]

def parse_list(input_str: str, curr_idx = 0):
    max_idx = len(input_str) - 1
    res = []
    while curr_idx < max_idx:
        ch = input_str[curr_idx]
        if ch == "(":
            curr_idx, sub_res = parse_list(input_str, curr_idx+1)
            res.append([*sub_res])
        if ch in note_symbols:
            curr_idx, sub_res = parse_note(input_str, curr_idx+1)
            res.append([ch, *sub_res])
        elif ch == "r":
            curr_idx, sub_res = parse_number(input_str, curr_idx+1)
            res.append([ch, sub_res])
        elif ch in ["v", "^"]:
            res.append([ch])
        elif ch == "t":
            curr_idx, sub_res = parse_whole_tuple(input_str, curr_idx+1)
            res.append([ch, *sub_res])
        elif ch == ")":
            break
        curr_idx += 1
    
    return curr_idx, ["n", *res]
    
def parse_number(input_str: str, curr_idx = 0):
    max_idx = len(input_str) - 1
    res = ""
    while curr_idx <= max_idx:
        ch = input_str[curr_idx]
        if ch.isnumeric():
            res += ch
        else:
            curr_idx -= 1
            break
        curr_idx += 1
    
    return curr_idx, res

def parse_whole_tuple(input_str: str, curr_idx = 0):
    res = []
    max_idx = len(input_str) - 1
    while curr_idx < max_idx:
        ch = input_str[curr_idx]
        if ch == "(":
            curr_idx, sub_res = parse_list(input_str, curr_idx+1)
            res.append([*sub_res])
            break
        elif ch.isnumeric():
            curr_idx, sub_res = parse_number(input_str, curr_idx)
            res.append(sub_res)
        
        curr_idx += 1
    
    return curr_idx, res

def parse_note(input_str: str, curr_idx = 0):
    res = ""
    max_idx = len(input_str) - 1
    while curr_idx <= max_idx:
        ch = input_str[curr_idx]
        if ch not in acc_symbols and ch not in punctuation_symbols and ch not in tie_symbols:
            curr_idx -=1
            break
        else:
            res += ch
        curr_idx += 1
        
    return curr_idx, res
        

def crawl_structure(tokens: list, indent = 0):
    for token in tokens:
        if isinstance(token, str):
            print((" " * indent) + token)
        else:
            crawl_structure(token, indent + 4)



curr_ratio = Ratio(t=(1, 4))
curr_oct = 5
def eval(tokens: list) -> list[TimeHolder]:
    global curr_ratio
    global curr_oct
    time_holders = []
    first = tokens[0]
    

    if first == "n":
        for sub in tokens[1:]:
            ths = eval(sub)
            for th in ths:
                time_holders.append(th)
        ...
    elif first == "t":
        ths = eval(tokens[2])
        num = int(tokens[1])
        
        for th in ths:
            th.base_duration = th.base_duration * Ratio(t=(2, num))
            
        ths[0].tuple_start = True
        ths[-1].tuple_end = True
            
        for th in ths:
            time_holders.append(th)
        ...
        
    elif first == "r":
        num = tokens[1]
        curr_ratio = Ratio(t=(1, int(num)))
        ...
    
    elif first in note_symbols:
        func = [nt for nt in note_tokens if nt[0]==first][0][1]
        n = func()
        acc = "".join([x for x in tokens[1:] if x in acc_symbols])
        alter = [x for x in acc_tokens if x[0] == acc][:1]
        if alter:
            n = alter[0][1](n)
            n.base_duration = curr_ratio
        dot = "".join([x for x in tokens[1:] if x in punctuation_symbols])
        dotting = [x for x in punctuation_tokens if x[0] == dot][:1]
        if dotting:
            n = dotting[0][1](n)
            
        tie = "".join([x for x in tokens[1:] if x in tie_symbols])
        tied = [x for x in tie_tokens if x[0] == tie][:1]
        if tied:
            n = tied[0][1](n)
        time_holders.append(n)
        ...

    return time_holders

# for sample in samples:      
#     tokens = parse_list(sample)
#     eval(tokens[1])
#     print(tokens[1])
    

for sample in samples:      
    tokens = parse_list(sample)
    ths = eval(tokens[1])
    print("-------------")
    for th in ths:
        print(th)
    
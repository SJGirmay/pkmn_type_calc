from ast import Return
from asyncio.windows_events import NULL
from os import linesep

# Enumeration for type properties
NAME = 0
WEAK = 1
RESIST = 2
IMMUNE = 3
NEUTRAL = 4
#VWEAK = 5
#VRESIST = 6

# Hash Map, Collision of type weakness/resistances
# See if any overlay, seeing if x4, x.25 is needed
# Brute Force Baby

# list of possible type combos
type_combos = []
# Set of processed type combos
processed_type_combos = []

# List of all types and their properties
# NOTE: indexing is strict and affects property sets - DO NOT reorganize list
# Name, Weak to, Resist to, Immune to
types = [
    # 0
    ('Bug', {5, 13, 4}, {3, 8, 7}, set()),
    # 1
    ('Dragon', {1, 17, 9}, {4, 14, 7, 2}, set()),
    # 2
    ('Electric', {8}, {5, 16, 2}, set()),
    # 3
    ('Fighting', {5, 12, 17}, {13, 0, 15}, set()),
    # 4
    ('Fire', {8, 13, 14}, {0, 16, 4, 7, 9, 17}, set()),
    # 5
    ('Flying', {13, 2, 9}, {3, 0, 7}, {8}),
    # 6
    ('Ghost', {6, 15}, {11, 0}, {10, 3}),
    # 7
    ('Grass', {5, 11, 0, 4, 9}, {8, 14, 7, 2}, set()),
    # 8
    ('Ground', {14, 7, 9}, {11, 13}, {2}),
    # 9
    ('Ice', {3, 13, 16, 4}, {9}, set()),
    # 10
    ('Normal', {3}, set(), {6}),
    # 11
    ('Poison', {8, 11}, {3, 11, 0, 7, 17}, set()),
    # 12
    ('Psychic', {0, 6, 15}, {3, 12}, set()),
    # 13
    ('Rock', {3, 8, 16, 14, 7}, {10, 5, 11, 4}, set()),
    # 14
    ('Water', {7, 2}, {16, 4, 14, 9}, set()),
    # 15
    ('Dark', {3, 0, 17}, {6, 15}, {12}),
    # 16
    ('Steel', {3, 8, 4}, {10, 5, 13, 0, 16, 7, 12, 9, 1, 17}, {11}),
    # 17
    ('Fairy', {11, 16}, {3, 0, 15}, {1}),
    # 18 ('???', set(), set(), set()),
]

# function to get a property set as a single string
def get_property_str(property_set):
    if not property_set:
        return '-'

    try:
        type_names = [types[t][NAME] for t in property_set]
        return ', '.join(type_names)
    except Exception:
        print(f'***ERROR PROCESSING SET {property_set} ***')

# Define a class for a type combination
class Typing:
    def __init__(self, t1, t2, w1, w2, r1, r2, i):
        self.type1 = t1
        self.type2 = t2
        
        self.weak_x1 = w1
        self.weak_x2 = w2
        #self.weak_x4 = w4
        
        self.resist_x1 = r1
        self.resist_x2 = r2
        #self.resist_x2 = r4
        
        self.immune = i


    def __str__(self):
        if(self.type2[NAME] == self.type1[NAME]):
            s = f'TYPE: {self.type1[NAME]}{linesep}'
        else:
            s = f'TYPE: {self.type1[NAME]} / {self.type2[NAME]}{linesep}'
        s += f'=> WEAK x1: {get_property_str(self.weak_x1)}{linesep}'
        s += f'=> WEAK x2: {get_property_str(self.weak_x2)}{linesep}'
        s += f'=> RESIST x1: {get_property_str(self.resist_x1)}{linesep}'
        s += f'=> RESIST x2: {get_property_str(self.resist_x2)}{linesep}'
        s += f'=> IMMUNE: {get_property_str(self.immune)}{linesep}'
        s += f'------------------------{linesep}'
        return s

# Function to combine two types
# Utilizes set operations to calculate new properties
def combine(type1, type2):
    # calculate weak x2, resist x2, and immunities
    weak_x2 = type1[WEAK] & type2[WEAK]
    #for i in weak_x2:
        #print(i)
    resist_x2 = type1[RESIST] & type2[RESIST]
    #for i in resist_x2:
        #print(i + i)
    immune = type1[IMMUNE] | type2[IMMUNE]

    # initialize vars for reuse
    handled = weak_x2 | resist_x2 | immune
    weak_all = type1[WEAK] | type2[WEAK]
    resist_all = type1[RESIST] | type2[RESIST]

    # calculate weak x1 and resist x1
    weak_x1 = weak_all - resist_all - handled
    resist_x1 = resist_all - weak_all - handled

    # create and return a new Typing
    return Typing(type1, type2, set(weak_x1), set(weak_x2),
                     set(resist_x1), set(resist_x2), set(immune))

# Simulates a Pokemon Attack
def attack(typeAtk, Defender):
    print(typeAtk)
    immune  = Defender.type1[IMMUNE] | Defender.type2[IMMUNE] 
    if typeAtk in immune:
        print("It had no Effect!")
        return IMMUNE
    
    weak_x2 = Defender.type1[WEAK] & Defender.type2[WEAK]
    if typeAtk in weak_x2:
        print("It's Super Effective!")
        return WEAK
    
    resist_x2 = Defender.type1[RESIST] & Defender.type2[RESIST]
    if typeAtk in resist_x2:
        print("It's not very Effective...")
        return RESIST
    else:
        print("It's neutrally Effective.")
        return NEUTRAL

def curtain(input):
    if input == 1:
        return combine(types[0],types[6])
    if input == 2:
        return combine(types[0],types[6])
    if input == 3:
        return combine(types[0],types[6])

# Testing Function to see all combinations
def all_combos():   
    
    length = len(types)
    # loop over type combos
    for i1 in range(0, length):
        for i2 in range(0, length):
            # initialize a set of indexes of the current combo
            combo_indexes = {i1, i2}
            # check if combo was already processed
            if combo_indexes not in processed_type_combos:
                # if not, combine types
                new_type = combine(types[i1], types[i2])
                # add new type to global list
                type_combos.append(new_type)
                # add index set to the list of processed combos
                processed_type_combos.append(combo_indexes)
    
    
    
    
    #[print(t) for t in type_combos]
    out_file = open("result.txt", "w")
    for t in type_combos:
        out_file.write("%s\n" % t)
    out_file.close()

def main():
    all_combos()
    print("Welcome to the Pokemon Proof!")
    UnknownDefender = combine(types[0],types[6])
    attack(13, UnknownDefender) 

if __name__ == '__main__':
    main()

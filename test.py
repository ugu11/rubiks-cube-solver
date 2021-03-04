from populations_ops import repair_chromossome, social_disaster
from cube import Cube

def is_move_none(m): return m == 'n'


chr1 = {'fit': 0, 'val': ["r'", 'l', "u'", 'l2', "f'", 'd2', "l'", 'n', 'n']}
chr2 = {'fit': 0, 'val': ["r'", 'l', "u'", 'l2', "f'", 'd2', "l'", 'n', 'n', 'n']}
chr3 = {'fit': 0, 'val': ["r'", 'l', "u'", 'l2', "f'", 'd2', "l'", 'n']}
chr4 = {'fit': 0, 'val': ["r'", 'l', "u'", 'l', "f'", 'd2', "l'", 'n', 'n', 'n']}

pop = [chr1, chr2, chr3, chr4]

chr1['val'].sort(key=is_move_none)

cube = Cube()
cube.scramble()

new_pop = social_disaster(cube, pop)

for c in new_pop:
    print(c)
# print(chr2)

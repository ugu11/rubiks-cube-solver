from populations_ops import repair_chromossome, social_disaster
from cube import Cube

def is_move_none(m): return m == 'n'


chr1 = {'fit': 0, 'val': ['f2', 'd2', "d'", 'd', 'd2', 'f2']}
pop = [chr1]

chr1['val'].sort(key=is_move_none)

cube = Cube()
cube.scramble()

ws = True
while ws == True:
    new_pop, ws = repair_chromossome(chr1)

for c in new_pop:
    print(c)
print(chr1)

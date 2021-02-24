from cube import Cube
from copy import deepcopy

c = Cube()
c.scramble()
c2 = deepcopy(c)
print("-----------------")
c.print()
print("-----------------")
c2.print()

# c2.make_move('u2')
c2.faces['u'][0][0] = 2000
print("-----------------")
c2.print()
print("-----------------")
c.print()
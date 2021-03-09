from cube import Cube
import matplotlib.pyplot as plt
import numpy as np
from copy import deepcopy




cube = Cube()
cube.scramble()

# solve = ["b", "r", "d", "r'", "d2", "l", "b2", "u", "f'", "l2", "d", "b'", "u2", "l2", "b2", "u2", "l2", "f", "u2", "f2", "u2"]
solve = ["d2", "r", "f'", "b'", "d", "f'", "d", "l", "f'", "b2", "d", "b2", "d2", "r2", "b", "d2", "r2", "u2", "b2", "u2", "f2"]
# solve2 = ['b', 'd', "r'", 'l', "d'", "l'", "d'", 'f', 'u', 'l', "d'", "b'", 'd', 'l2', "u'", "r'", 'f', "u'", "f'", 'b', "l'", "b'", 'r', 'd', "l'", 'f', 'n', 'n']

# s = "d2 b2 r' f2 b l' f u b r' l f2 l u2 l' u2 d b d2 l f2 r' l2 b r2 b' r b r' l' d2 l2 u' d2"
# s = "d f d b r b' d' f b' r2 f2 b2 u f d2 l2 f l2 f2 b' r2 l2 u2 r d' f2 u d f' u2 f' u' l' u l f2 n n n"
s = "b l2 d r' l f2 l2 u l' d' r' d' r b' u d b2 u' d' f' u f2 b2 u' d' b' d f2 u f2 u' b' l2 u' l2 d' r2 d b l u' l' u' b2 u d' r2 d"
s = ""
solve2 = s.split(" ")
solve2 = ["d'", 'b', "u'", 'f', 'u', "d'", "b'", 'l2', 'b2', "m'", 'b2', 'm', 'n', "f'", "r'", 'f', "r'", "b'", 'd2', "b'", 'l', "f'", 'b', "d'", 'f', 'b', 'r2', "f'", 'b', 'u2', "f'", 'f', 'b2', 'u2', 'b2', 'u2', 'b2', 'u2', 'n', 'n', 'n', 'n', 'n']

while 'n' in solve2:
    solve2.remove('n')

print(len(solve2))
fitness = []

cub = Cube(cube)
cube2 = Cube(cube)

for move in solve:
    cub.make_move(move)
    # print("------------------------ ", move, " ----- ", cub.n_moves)
    fitness.append(cub.calc_fitness())

    
    # print("FINAL FITNESS", cub.fitness)

    if cub.fitness <= 0:
        cub.print()
fitness2 = []

for move in solve2:
    fits = []
    for m in cub.available_moves[:len(cub.available_moves)-1]:
        tmp_cube = Cube(cube)
        tmp_cube.make_move(m)
        fit = tmp_cube.calc_fitness()
        fits.append(fit)
    cube.make_move(move)
    fitness2.append(cube.calc_fitness())

print(m, "     ", [f for f in fits], "   min: ", min(fits), "   selected: ", cube.fitness)

print(solve2)


print(fitness)
# print(", ".join((s.split(" "))))

plt.plot(fitness) # plotting by columns
plt.plot(fitness2) # plotting by columns
plt.xticks(range(0, max([len(solve), len(solve2)])))
plt.yticks(range(0, int(max(fitness)+1)))
# plt.grid()
plt.show()

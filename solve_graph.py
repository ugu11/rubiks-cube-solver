from cube import Cube
import matplotlib.pyplot as plt
import numpy as np
from copy import deepcopy


def optimize_function(cube, s):
    c = Cube(cube)
    s = deepcopy(s)

    fs = []
    recalc = False
    for i in range(len(s)):
        print(fs)
        if len(fs) > 2:
            print(fs[i-1], fs[i-2])

            t = Cube(c)
            t.make_move(s[i])
            tf = t.calc_fitness()
            

            if tf - fs[i-1] >= 8 or recalc == True:
                recalc = True
                fits = []
                f = deepcopy(c.available_moves)
                f.remove(s[i-1][0])
                if s[i-1] != 'n':
                    f.remove(s[i-1][0]+"'")
                    f.remove(s[i-1][0]+"2")
                    if s[i-1] == c.oposite_face[s[i-2][0]]:
                        f.remove(s[i-2][0])
                        f.remove(s[i-2][0]+"'")
                        f.remove(s[i-2][0]+"2")
                for m in cub.available_moves[:18]:
                    tmp_cube = Cube(c)
                    tmp_cube.make_move(m)
                    fit = tmp_cube.calc_fitness()
                    fits.append(fit)
                
                c.make_move(f[np.argmin(fits)])
                s[i] = f[np.argmin(fits)]
                # print(fits, np.argmin(fits))
            else:
                c.make_move(s[i])
        else:
            c.make_move(s[i])
        
        

        fs.append(c.calc_fitness())

    print(fs)

    return s



cube = Cube()
cube.scramble()

# solve = ["b", "r", "d", "r'", "d2", "l", "b2", "u", "f'", "l2", "d", "b'", "u2", "l2", "b2", "u2", "l2", "f", "u2", "f2", "u2"]
solve = ["d2", "r", "f'", "b'", "d", "f'", "d", "l", "f'", "b2", "d", "b2", "d2", "r2", "b", "d2", "r2", "u2", "b2", "u2", "f2"]
# solve2 = ['b', 'd', "r'", 'l', "d'", "l'", "d'", 'f', 'u', 'l', "d'", "b'", 'd', 'l2', "u'", "r'", 'f', "u'", "f'", 'b', "l'", "b'", 'r', 'd', "l'", 'f', 'n', 'n']

# s = "d2 b2 r' f2 b l' f u b r' l f2 l u2 l' u2 d b d2 l f2 r' l2 b r2 b' r b r' l' d2 l2 u' d2"
# s = "d f d b r b' d' f b' r2 f2 b2 u f d2 l2 f l2 f2 b' r2 l2 u2 r d' f2 u d f' u2 f' u' l' u l f2 n n n"
s = "b l2 d r' l f2 l2 u l' d' r' d' r b' u d b2 u' d' f' u f2 b2 u' d' b' d f2 u f2 u' b' l2 u' l2 d' r2 d b l u' l' u' b2 u d' r2 d"
solve2 = s.split(" ")

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
    for m in cub.available_moves[:18]:
        tmp_cube = Cube(cube)
        tmp_cube.make_move(m)
        fit = tmp_cube.calc_fitness()
        fits.append(fit)
    cube.make_move(move)
    fitness2.append(cube.calc_fitness())

print(m, "     ", [f for f in fits], "   min: ", min(fits), "   selected: ", cube.fitness)

c = Cube(cube2)
solve3 = optimize_function(cube2, solve2)
print(solve2)
print(solve3)
fits3 = []
for move in solve3:
    fits = []
    for m in c.available_moves[:18]:
        tmp_cube = Cube(c)
        tmp_cube.make_move(m)
        fit = tmp_cube.calc_fitness()
        fits.append(fit)
    c.make_move(move)
    fits3.append(c.calc_fitness())
print(m, "     ", [f for f in fits3], "   min: ", min(fits3), "   selected: ", c.fitness)


print(fitness)
# print(", ".join((s.split(" "))))

plt.plot(fitness) # plotting by columns
plt.plot(fitness2) # plotting by columns
plt.plot(fits3) # plotting by columns
plt.xticks(range(0, max([len(solve), len(solve2)])))
plt.yticks(range(0, int(max(fitness)+1)))
# plt.grid()
plt.show()

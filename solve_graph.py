from cube import Cube
import matplotlib.pyplot as plt

cube = Cube()
cube.scramble()

solve = ["b", "r", "d", "r'", "d2", "l", "b2", "u", "f'", "l2", "d", "b'", "u2", "l2", "b2", "u2", "l2", "f", "u2", "f2", "u2"]
solve = ["d2", "r", "f'", "b'", "d", "f'", "d", "l", "f'", "b2", "d", "b2", "d2", "r2", "b", "d2", "r2", "u2", "b2", "u2", "f2"]

s = "d2 b2 r' f2 b l' f u b r' l f2 l u2 l' u2 d b d2 l f2 r' l2 b r2 b' r b r' l' d2 l2 u' d2 b' u' r b r' l' d' b d r' l b u b' r2"
solve = s.split(" ")

print(len(solve))
fitness = []

for move in solve:
    cube.make_move(move)
    print("------------------------ ", move, " ----- ", cube.n_moves)
    fitness.append(cube.calc_fitness())
    print("FINAL FITNESS", cube.fitness)
    if cube.fitness <= 0:
        cube.print()


print(fitness)
print(", ".join((s.split(" "))))

plt.plot(fitness) # plotting by columns
plt.xticks(range(0, len(solve)))
# plt.yticks(range(0, max(fitness)+1))
plt.grid()
plt.show()

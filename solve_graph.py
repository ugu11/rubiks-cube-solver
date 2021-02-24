from cube import Cube
import matplotlib.pyplot as plt

cube = Cube()
cube.scramble()

# solve = ["f", "l", "d", "l'", "d2", "r", "f2", "u", "b'", "r2", "d", "f'", "u2", "r2", "f2", "u2", "r2", "b", "u2", "b2", "u2"]
# solve = ["b", "r", "d", "r'", "d2", "l", "b2", "u", "f'", "l2", "d", "b'", "u2", "l2", "b2", "u2", "l2", "f", "u2", "f2", "u2"]
solve = ["d2", "r", "f'", "b'", "d", "f'", "d", "l", "f'", "b2", "d", "b2", "d2", "r2", "b", "d2", "r2", "u2", "b2", "u2", "f2"]

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

plt.plot(fitness) # plotting by columns
plt.show()





def test_line(cube):
    check_lines = []
    correct_values = [True, True, False, True, True, False, False, False]
    
    # Horizontal lines
    check_lines.append(cube.check_is_line(cube.faces['f'], (0, 0), (0, 2))) # True
    check_lines.append(cube.check_is_line(cube.faces['f'], (1, 0), (1, 2))) # True
    check_lines.append(cube.check_is_line(cube.faces['u'], (0, 0), (0, 2))) # False

    # Vertical lines
    check_lines.append(cube.check_is_line(cube.faces['b'], (0, 1), (2, 1))) # True
    check_lines.append(cube.check_is_line(cube.faces['b'], (0, 0), (2, 0))) # True
    cube.make_move("b'")
    cube.make_move("u2")
    cube.make_move("d2")
    check_lines.append(cube.check_is_line(cube.faces['f'], (0, 0), (2, 0))) # False
    cube.make_move("l'")
    check_lines.append(cube.check_is_line(cube.faces['u'], (0, 0), (2, 0))) # False
    cube.make_move("l'")
    cube.make_move("d")
    cube.make_move("f'")
    cube.make_move("r")
    check_lines.append(cube.check_is_line(cube.faces['u'], (0, 2), (2, 2))) # False



    
    print(check_lines)
    print(correct_values)

# test_line(cube)



def test(cube):

    check_pairs = []
    correct_values = [False, True, True, True, False, True, False, True, True]

    # False - Top horizontal pair
    check_pairs.append(cube.check_is_pair(
        cube.faces['l'],
        (0, 0),
        (0, 1)
    ))

    # True - Top horizontal pair
    check_pairs.append(cube.check_is_pair(
        cube.faces['b'],
        (0, 1),
        (0, 2)
    ))

    # True - Left vertical pair
    check_pairs.append(cube.check_is_pair(
        cube.faces['f'],
        (1, 0),
        (2, 0)
    ))

    # True - bottom - center->right pair
    check_pairs.append(cube.check_is_pair(
        cube.faces['d'],
        (1, 1),
        (1, 2)
    ))

    # False - Bottom horizontal pair
    check_pairs.append(cube.check_is_pair(
        cube.faces['l'],
        (2, 0),
        (2, 1)
    ))

    cube.make_move('b2')

    # True - Bottom horizontal pair
    check_pairs.append(cube.check_is_pair(
        cube.faces['b'],
        (2, 0),
        (2, 1)
    ))

    cube.make_move("l'")

    # False - Right vertical pair
    check_pairs.append(cube.check_is_pair(
        cube.faces['b'],
        (1, 2),
        (2, 2)
    ))

    # True - Left vertical pair
    check_pairs.append(cube.check_is_pair(
        cube.faces['u'],
        (1, 0),
        (2, 0)
    ))

    cube.make_move("d'")

    # True - Right vertical pair
    check_pairs.append(cube.check_is_pair(
        cube.faces['d'],
        (0, 2),
        (1, 2)
    ))



    print(check_pairs)
    print(correct_values)

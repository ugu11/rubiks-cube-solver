from cube import Cube
from sa import simulated_anealing
from ga import genetic_algorithm
from copy import deepcopy

def solve():
    cube = Cube()
    cube.scramble()
    # original_cube = Cube(cube)
    # cube.calc_fitness()

    # simulated_anealing(cube)
    best_sols = []
    for i in range(2):
        best_solve = genetic_algorithm(Cube(cube))
        best_sols.append(deepcopy(best_solve))

    print([sol for sol in best_sols])

    # b = "d2 b2 r' f2 b l' f u b r' l f2 l u2 l' u2 d b d2 l f2 r' l2 b r2 b' r b r' l' d2 l2 u' d2"
    # b = "d2 b2 r' f2 b l' f u b r' l f2 l u2 l' u2 d b d2 l f2 r' l2 b r2 b' r b r' l' d2" #l2 u' d2"
    # b = b.split(" ")
    # b = ['u2', "d'", 'r', "u'", 'd', "b'", 'l2', 'u', 'f', 'r', "d'", 'f', "u'", "r'", 'u2', 'd', 'f2', 'l2', 'u', "b'", "l'", "f'", 'r', 'b', "r'", "l'", 'f', "r'", 'l', 'd2', 'r', 'f', 'l', 'f', "l'", 'f2']

    # best_solve = {'fit': 0, 'val': b}

    # for move in best_solve['val']:
    #     cube.make_move(move)

    # best_solve['fit'] = cube.calc_fitness()

    # new_moves = []

    # while cube.fitness > 0:
    #     best_move = []
    #     best_fit = cube.max_fitness
    #     print(cube.fitness, best_fit, new_moves)
    #     moves_cpy = deepcopy(cube.available_moves[:18])

    #     if len(new_moves) == 0:
    #         moves_cpy.remove(b[len(b)-1][0])
    #         moves_cpy.remove(b[len(b)-1][0]+"'")
    #         moves_cpy.remove(b[len(b)-1][0]+"2")
    #     else:
    #         moves_cpy.remove(new_moves[len(new_moves)-1][0])
    #         moves_cpy.remove(new_moves[len(new_moves)-1][0]+"'")
    #         moves_cpy.remove(new_moves[len(new_moves)-1][0]+"2")
        
        
    #     for move in moves_cpy:
    #         moves2_cpy = deepcopy(moves_cpy)
    #         moves2_cpy.remove(move[0])
    #         moves2_cpy.remove(move[0]+"'")
    #         moves2_cpy.remove(move[0]+"2")

    #         tmp_cube = Cube(cube)
    #         tmp_cube.make_move(move)


    #         if tmp_cube.fitness < best_fit:
    #             best_move = [move]
    #             best_fit = tmp_cube.fitness

    #         for move2 in moves2_cpy:
    #             tmp_cube2 = Cube(tmp_cube)
    #             tmp_cube2.make_move(move2)

    #             moves3_cpy = deepcopy(cube.available_moves[:18])
    #             moves3_cpy.remove(move2[0])
    #             moves3_cpy.remove(move2[0]+"'")
    #             moves3_cpy.remove(move2[0]+"2")


    #             if tmp_cube2.fitness < best_fit:
    #                 best_move = [move, move2]
    #                 best_fit = tmp_cube2.fitness

    #             for move3 in moves3_cpy:
    #                 tmp_cube3 = Cube(tmp_cube2)
    #                 tmp_cube3.make_move(move3)

    #                 moves4_cpy = deepcopy(cube.available_moves[:18])
    #                 moves4_cpy.remove(move3[0])
    #                 moves4_cpy.remove(move3[0]+"'")
    #                 moves4_cpy.remove(move3[0]+"2")

    #                 if tmp_cube3.fitness < best_fit:
    #                     best_move = [move, move2, move3]
    #                     best_fit = tmp_cube3.fitness

    #                 for move4 in moves4_cpy:
    #                     tmp_cube4 = Cube(tmp_cube3)
    #                     tmp_cube4.make_move(move4)
    #                     tmp_cube4.calc_fitness()

    #                     if tmp_cube4.fitness < best_fit:
    #                         best_move = [move, move2, move3, move4]
    #                         best_fit = tmp_cube4.fitness

    #     for move in best_move:
    #         cube.make_move(move)
    #     cube.calc_fitness()
    #     new_moves += best_move

    #     print(best_solve['val'] + new_moves)


def main():
    solve()

main()
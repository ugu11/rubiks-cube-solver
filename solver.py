from cube import Cube
from sa import simulated_anealing
from ga import genetic_algorithm
from populations_ops import repair_chromossome, evaluate_solution
from copy import deepcopy

import json

def solve():
    cube = Cube()
    cube.scramble()
    original_cube = Cube(cube)
    curr_cube = Cube(original_cube)
    # cube.calc_fitness()

    # best_sols = []
    # i = 0
    # n_repeats = 0
    # while i < 15:
    #     print(curr_cube.fitness)
    #     best_solve = genetic_algorithm(Cube(curr_cube), 5 + n_repeats)
    #     if best_solve['fit'] < curr_cube.fitness:
    #         best_sols.append(deepcopy(best_solve))

    #         for m in best_solve['val']:
    #             curr_cube.make_move(m)
    #         curr_cube.calc_fitness()
    #         n_repeats = 0
    #     else:
    #         n_repeats += 1
    #     i += 1
    #         # print([sol for sol in best_solve['val']])

    # final_sol = []
    # for sol in best_sols:
    #     print(sol)
    #     final_sol += sol['val']

    # final_chrom = {
    #     'fit': 0,
    #     'val': final_sol
    # }

    # 'fit': 230, 'val': ['f2', 'r', "d'", 'b', "d'", "l'", "f'", 'l']}
    # {'fit': 226, 'val': ['l', 'f2', "r'", 'u', "d'", "b'"]}
    # {'fit': 215, 'val': ["u'", "l'", 'u', "d'", 'b', "u'"]}
    # {'fit': 204, 'val': ['d', 'b2', "u'", 'b', 'd', 'l2']}
    # {'fit': 197, 'val': ['l', 'f2', "l'", 'f', 'u2', "f'", 'b', "l'"]}
    # {'fit': 183, 'val': ['b2', 'd', "r'", 'b2', "u'", 'b', 'l']}
    # {'fit': 174, 'val': ["l'", 'f', "b'", "f'", 'b', 'l2']}
    # {'fit': 121, 'val': ["f'", 'b', "d'", 'f', "b'", 'l', 'f', "b'", "u'"]}
    # {'fit': 95, 'val': ['u2', "b'", "u'", "r'", 'u', 'r', 'b']}
    # {'fit': 75, 'val': ['u', 'b', "l'", "b'", 'l', 'u']}

    with open('data.json') as json_file:
        data = json.load(json_file)
    

    moves = ['f2', 'r', "d'", 'b', "d'", "l'", "f'", 'l', 'l', 'f2', "r'", 'u', "d'", "b'", "u'", "l'", 'u', "d'", 'b',
    "u'", 'd', 'b2', "u'", 'b', 'd', 'l2', 'l', 'f2', "l'", 'f', 'u2', "f'", 'b', "l'", 'b2', 'd', "r'", 'b2', "u'", 'b', 'l',
    "l'", 'f', "b'", "f'", 'b', 'l2', "f'", 'b', "d'", 'f', "b'", 'l', 'f', "b'", "u'", 'u2', "b'", "u'", "r'", 'u', 'r', 'b',
    'u', 'b', "l'", "b'", 'l', 'u']

    sol = {'fit': 0, 'val': moves}

    evaluate_solution(cube, sol)

    print(sol)

    for move in sol['val']:
        curr_cube.make_move(move)
    curr_cube.calc_fitness()

    solved_faces = curr_cube.get_solved_faces()

    print(solved_faces)
    




    # rc = True

    # while rc == True:
    #     final_chrom, rc = repair_chromossome(final_chrom)
    
    # print("Final sol: ", final_chrom['val'])
    # print("Sol size: ", len(final_chrom['val']))
    # print("Fit: ", final_chrom['fit'])



def main():
    solve()

main()
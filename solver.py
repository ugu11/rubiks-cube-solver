from cube import Cube
from sa import simulated_anealing
from ga import genetic_algorithm
from populations_ops import repair_chromossome, evaluate_solution
from copy import deepcopy

import json

def solve():
    with open('data.json') as json_file:
        oll_data = json.load(json_file)

    cube = Cube()
    cube.scramble()
    original_cube = Cube(cube)
    curr_cube = Cube(original_cube)
    # cube.calc_fitness()

    best_sols = []
    i = 0
    n_repeats = 0
    while curr_cube.fitness > 100:
        print(curr_cube.fitness, n_repeats)
        best_solve = genetic_algorithm(Cube(curr_cube), 7 + n_repeats)
        if best_solve['fit'] < curr_cube.fitness:
            best_sols.append(deepcopy(best_solve))

            for m in best_solve['val']:
                curr_cube.make_move(m)
            curr_cube.calc_fitness()
            n_repeats = 0
        else:
            n_repeats += 1
        i += 1
            # print([sol for sol in best_solve['val']])

    final_sol = []
    for sol in best_sols:
        print(sol)
        final_sol += sol['val']

    # final_sol = ['f2', 'l2', 'b', "u'", 'f', "u'", 'l', 'b', 'l', 'b', 'l', 'b2', 'l', 'f', 'b', 'u2', 'f2', 'u2', 'b2', 'd2', 'b2',
    #     'r2', 'f2', 'l', 'f2', 'r2', "f'", 'l2', 'f2', 'r', 'f2', 'l2', "f'", 'r', "f'", "b'", "r'", 'u2', 'r', 'u', 'm', "u'", "m'",
    #     "u'", 'b2', 'u', 'b2', 'u', 'b2', "m'", 'b2', 'm', "u'", 'l', "u'", 'f', 'u', "f'", 'u', "l'", "u'", 'u2', "f'", 'u2', 'f', 'u',
    #     "f'", 'u', 'f']

    final_chrom = {
        'fit': 0,
        'val': final_sol
    }

    evaluate_solution(cube, final_chrom)
    print(final_chrom)

    # for move in final_chrom['val']:
    #     curr_cube.make_move(move)
    # curr_cube.calc_fitness()
    # curr_cube.rotate('z')

    solved_faces = curr_cube.get_solved_faces()

    print(solved_faces)
    oll_face = ''
    
    for face in solved_faces:
        is_slice_solved = curr_cube.check_is_slice_solved(curr_cube.oposite_face[face][1])
        print(face, curr_cube.oposite_face[face][1], is_slice_solved)

        if is_slice_solved == True:
            oll_face = curr_cube.oposite_face[face][0]
            break

    print(oll_face)

    if oll_face == 'd':
        curr_cube.rotate('x2')
    elif oll_face == 'l':
        curr_cube.rotate('z')
    elif oll_face == 'r':
        curr_cube.rotate("z'")
    elif oll_face == 'f':
        curr_cube.rotate("x")
    elif oll_face == 'b':
        curr_cube.rotate("x'")

    curr_cube.print()

    oll_moves = []

    for i in range(4):
        curr_cube.make_move('u')
        oll_moves.append('u')

        oll_id_bits = []

        for face in ['l', 'b', 'r', 'f']:
            if face == 'b' or face == 'r':
                for piece in curr_cube.faces[face][0][::-1]:
                    if piece[0] == curr_cube.faces['u'][1][1][0]:
                        oll_id_bits.append('1')
                    else:
                        oll_id_bits.append('0')
            else:
                for piece in curr_cube.faces[face][0]:
                    if piece[0] == curr_cube.faces['u'][1][1][0]:
                        oll_id_bits.append('1')
                    else:
                        oll_id_bits.append('0')
                
        for row in curr_cube.faces['u']:
            for piece in row:
                if piece[0] == curr_cube.faces['u'][1][1][0]:
                    oll_id_bits.append('1')
                else:
                    oll_id_bits.append('0')

        print("".join(oll_id_bits))

        oll_id_bits = "".join(oll_id_bits)

        if oll_id_bits in oll_data.keys():
            break

    oll_moves += oll_data[oll_id_bits]

    print("FINAL SOLVE: ", " ".join(final_chrom['val'] + oll_moves))



    # rc = True

    # while rc == True:
    #     final_chrom, rc = repair_chromossome(final_chrom)
    
    # print("Final sol: ", final_chrom['val'])
    # print("Sol size: ", len(final_chrom['val']))
    # print("Fit: ", final_chrom['fit'])



def main():
    solve()

main()
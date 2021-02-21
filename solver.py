import os
from cube import Cube
from Tree import Tree
from copy import deepcopy
from random import randint, random
from math import exp

# Perform two moves
def generate_neighbor_2moves(cube):
    neighbor = deepcopy(cube)
    moves = ["u", "u'", "f", "f'", "l", "l'", "r", "r'", "d", "d'", "b", "b'", 'u2', 'b2', 'f2', 'l2', 'r2', 'd2']
    move1 = moves[randint(0, len(moves)-1)]
    moves.remove(move1)
    neighbor.make_move(move1)
    if neighbor.fitness != 0:
        move2 = moves[randint(0, len(moves)-1)]
        neighbor.make_move(move2)

    return neighbor


def generate_neighbor(cube):
    neighbor = deepcopy(cube)
    moves = ["u", "u'", "f", "f'", "l", "l'", "r", "r'", "d", "d'", "b", "b'", 'u2', 'b2', 'f2', 'l2', 'r2', 'd2']
    move = moves[randint(0, len(moves)-1)]
    neighbor.make_move(move)
    return neighbor, move

# Converges when fitness => [24; 27]
def simulated_anealing(cube):
    best_cube = deepcopy(cube)
    print("Initial fitness: ", best_cube.fitness)

    moves = []

    T = 5000
    a = 0.7
    i = 0

    while T > 0.0000000000001:
        i = 0
        local_best = deepcopy(best_cube)
        local_best_move = ''
        while i < 50000:
            neighbor, move = generate_neighbor(local_best)
            delta = local_best.fitness - neighbor.fitness

            if delta >= 0:
                local_best = deepcopy(neighbor)
                local_best_move = move
            else:
                if random() < exp((delta/T)):
                    local_best = deepcopy(neighbor)
                    local_best_move = move

            # neighbor.print()
            i += 1

        if local_best.fitness <= best_cube.fitness:
            best_cube = deepcopy(local_best)
            moves.append(local_best_move)

        print("New best fit", best_cube.fitness, "   Local best move", local_best_move, "    Local best fit", local_best.fitness)
        if best_cube.fitness == 0:
            break

        print("T ", T)
        T *= a

        # if T < 0.0000000000001:
        #     T = 3
        

    # print(neighbor.fitness)
    best_cube.print()
    print("Bestest fit", best_cube.fitness)
    print(moves)


def solve():
    cube = Cube()
    cube.scramble()
    # original_cube = deepcopy(cube)
    # cube.calc_fitness()

    simulated_anealing(cube)

    

def main():
    solve()

main()
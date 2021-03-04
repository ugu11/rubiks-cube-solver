import os
from cube import Cube
from random import randint, random
from copy import deepcopy
from math import exp

def generate_neighbor_4moves(cube):
    neighbor = Cube(cube)
    moves = Cube.available_moves
    while neighbor.faces == cube.faces:
        forbidden_moves = []
        move1 = moves[randint(0, len(moves)-1)]
        forbidden_moves.append(move1[0])
        forbidden_moves.append(move1[0] + "'")
        forbidden_moves.append(move1[0] + "2")
        neighbor.make_move(move1)
        
        if neighbor.fitness == 0:
            neighbor.calc_fitness()
            return neighbor, [move1]
        move2 = move1
        while move2 in forbidden_moves:
            move2 = moves[randint(0, len(moves)-1)]
        forbidden_moves.clear()
        forbidden_moves.append(move2[0])
        forbidden_moves.append(move2[0] + "'")
        forbidden_moves.append(move2[0] + "2")
        neighbor.make_move(move2)

        if neighbor.fitness == 0:
            neighbor.calc_fitness()
            return neighbor, [move1, move2]
        move3 = move2
        while move3 in forbidden_moves:
            move3 = moves[randint(0, len(moves)-1)]
        forbidden_moves.clear()
        forbidden_moves.append(move3[0])
        forbidden_moves.append(move3[0] + "'")
        forbidden_moves.append(move3[0] + "2")
        neighbor.make_move(move3)

        if neighbor.fitness == 0:
            neighbor.calc_fitness()
            return neighbor, [move1, move2, move3]
        # move4 = move3
        # while move4 in forbidden_moves:
        #     move4 = moves[randint(0, len(moves)-1)]
        # neighbor.make_move(move4)

    neighbor.calc_fitness()
    return neighbor, [move1, move2, move3]

# Perform two moves
def generate_neighbor_2moves(cube):
    neighbor = Cube(cube)
    moves = deepcopy(Cube.available_moves)
    move1 = moves[randint(0, len(moves)-1)]
    # if '2' in move1:
    #     moves.remove(move1)
    # else:
    #     moves.remove(move1[0])
    #     moves.remove(move1[0] + "'")
    neighbor.make_move(move1)
    if neighbor.fitness == 0:
        neighbor.calc_fitness()
        return neighbor, [move1]
    move2 = move1
    while move2[0] == move1[0]:
        move2 = moves[randint(0, len(moves)-1)]
    neighbor.make_move(move2)
    neighbor.calc_fitness()
    return neighbor, [move1, move2]

def gen_8_moves(cube):
    neighbor, moves = generate_neighbor_4moves(cube)
    neighbor, moves2 = generate_neighbor_4moves(neighbor)

    return neighbor, moves + moves2
    



def generate_neighbor(neighbor):
    neighbor = Cube(neighbor)
    moves = Cube.available_moves[:len(Cube.available_moves)-1]
    move = moves[randint(0, len(moves)-1)]
    neighbor.make_move(move)
    neighbor.calc_fitness()
    return neighbor, move

# Converges when fitness => [24; 27]
def simulated_anealing(cube):
    best_cube = Cube(cube)

    moves = []
    # s = "l2 u2 f2 u f2 r' u2 d f2 d2 u2 l d2 l r' b' d' u f2 l f r2 l2 b2 l b r' u2 l n n"
    # s = "l r' l2 f l2 d r d r' l' f' b l2 b' l' f r2 u' f' l d' b' d r' l' r' l r2"
    # s = "u f' r u' r' d' f r2 f u' r2 b' l2 r2 u' f' r b r' b' r2 f u' b d u' l2 u r b r2 b' u' d'"
    # s = "u' d u2 r d2 b f' r2 u' b' r' l' r2 u2 r u2 d2 b r2 f r l2 f2 b' r' l2 u' r2 l2 d2"
    s = "b l2 d r' l f2 l2 u l' d' r' d' r b' u d b2 u' d' f' u f2 b2 u' d' b' d f2 u f2 u' b' l2 u' l2 d' r2 d b l u' l' u' b2 u d' r2 d"
    moves = s.split(" ")
    # moves = ['u2', "d'", 'r', "u'", 'd', "b'", 'l2', 'u', 'f', 'r', "d'", 'f', "u'", "r'", 'u2', 'd', 'f2', 'l2', 'u', "b'", "l'", "f'", 'r', 'b', "r'", "l'", 'f', "r'", 'l', 'd2', 'r', 'f', 'l', 'f', "l'", 'f2']
    # moves = ['d', 'f', 'd', 'b', 'r', "b'", "d'", 'f', "b'", 'r2', 'f2', 'b2', 'u', 'f', 'd2', 'l2', 'f', 'l2', 'f2', "b'", "r'", 'l2', 'u2', 'r', "d'", 'f2', 'u', 'd', "f'", "u'", 'f', 'n']

    for move in moves:
        best_cube.make_move(move)
    best_cube.calc_fitness()
    print("Initial fitness: ", best_cube.fitness)

    T = 2000
    a = 0.03
    i = 0
    n_changes = 0

    while n_changes < 10: #T > 0.000001:
        i = 0
        local_best = Cube(best_cube)
        local_best_move = ''
        print("T ", T)
        while i < 10000:
            neighbor, n_move = generate_neighbor(best_cube)
            neighbor_2moves, n2_moves = generate_neighbor_2moves(best_cube)
            neighbor_4moves, n4_moves = generate_neighbor_4moves(best_cube)
            n8, n8m = gen_8_moves(best_cube)
            
            if neighbor_2moves.fitness <= neighbor_4moves.fitness:
                selected_neighbor = neighbor_2moves
                move = n2_moves
            else:
                selected_neighbor = neighbor_4moves
                move = n4_moves

            if neighbor.fitness <= selected_neighbor.fitness:
                selected_neighbor = neighbor
                move = [n_move]

            if n8.fitness < selected_neighbor.fitness:
                selected_neighbor = n8
                move = n8m

            delta = local_best.fitness - selected_neighbor.fitness

            if delta >= 0:
                local_best = Cube(selected_neighbor)
                local_best_move = move
            else:
                if random() < exp((delta/T)):
                    local_best = Cube(selected_neighbor)
                    local_best_move = move

            local_best.calc_fitness()


            i += 1

        print(T, local_best.fitness)

        
        if local_best.fitness <= best_cube.fitness and local_best_move != '':
            best_cube = Cube(local_best)
            best_cube.calc_fitness()
            # moves.append(local_best_move)
            moves += local_best_move

        # best_cube.print()

        print("New best fit", best_cube.fitness, "   Local best move", local_best_move, "    Local best fit", local_best.fitness)
        if best_cube.fitness == 0:
            break

        print("T ", T)
        T *= a

        if T < 0.00001:
            T = 10
            n_changes += 1
        

    # print(neighbor.fitness)
    best_cube.print()
    print("Bestest fit", best_cube.fitness)
    print(moves)

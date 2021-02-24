import os
from cube import Cube
from random import randint, random
from math import exp

def generate_neighbor_4moves(cube):
    neighbor = Cube(cube)
    moves = ["u", "u'", "f", "f'", "l", "l'", "r", "r'", "d", "d'", "b", "b'", 'u2', 'b2', 'f2', 'l2', 'r2', 'd2']
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
        move4 = move3
        while move4 in forbidden_moves:
            move4 = moves[randint(0, len(moves)-1)]
        neighbor.make_move(move4)

    neighbor.calc_fitness()
    return neighbor, [move1, move2, move3, move4]

# Perform two moves
def generate_neighbor_2moves(cube):
    neighbor = Cube(cube)
    moves = ["u", "u'", "f", "f'", "l", "l'", "r", "r'", "d", "d'", "b", "b'", 'u2', 'b2', 'f2', 'l2', 'r2', 'd2']
    move1 = moves[randint(0, len(moves)-1)]
    if '2' in move1:
        moves.remove(move1)
    else:
        moves.remove(move1[0])
        moves.remove(move1[0] + "'")
    neighbor.make_move(move1)
    if neighbor.fitness == 0:
        neighbor.calc_fitness()
        return neighbor, [move1]

    move2 = moves[randint(0, len(moves)-1)]
    neighbor.make_move(move2)

    neighbor.calc_fitness()
    return neighbor, [move1, move2]


def generate_neighbor(neighbor):
    neighbor = Cube(neighbor)
    moves = ["u", "u'", "f", "f'", "l", "l'", "r", "r'", "d", "d'", "b", "b'", 'u2', 'b2', 'f2', 'l2', 'r2', 'd2']
    move = moves[randint(0, len(moves)-1)]
    neighbor.make_move(move)
    neighbor.calc_fitness()
    return neighbor, move

# Converges when fitness => [24; 27]
def simulated_anealing(cube):
    best_cube = Cube(cube)
    print("Initial fitness: ", best_cube.fitness)

    moves = []

    T = 1000
    a = 0.05
    i = 0
    n_changes = 0

    while best_cube.fitness != 0:
        i = 0
        local_best = Cube(best_cube)
        local_best_move = ''
        while i < 5000:
            neighbor, n_move = generate_neighbor(best_cube)
            neighbor_2moves, n2_moves = generate_neighbor_2moves(best_cube)
            neighbor_4moves, n4_moves = generate_neighbor_4moves(best_cube)
            
            if neighbor.fitness < neighbor_2moves.fitness:
                selected_neighbor = neighbor
                move = [n_move]
            else:
                selected_neighbor = neighbor_2moves
                move = n2_moves

            if neighbor_4moves.fitness < selected_neighbor.fitness:
                selected_neighbor = neighbor_4moves
                move = n4_moves

            delta = local_best.fitness - selected_neighbor.fitness

            if delta > 0:
                local_best = Cube(selected_neighbor)
                local_best_move = move
            else:
                if random() < exp((delta/T)):
                    local_best = Cube(neighbor)
                    local_best_move = move

            i += 1

        
        if local_best.fitness <= best_cube.fitness and local_best_move != '':
            best_cube = Cube(local_best)
            # moves.append(local_best_move)
            moves += local_best_move

        # best_cube.print()

        print("New best fit", best_cube.fitness, "   Local best move", local_best_move, "    Local best fit", local_best.fitness)
        if best_cube.fitness == 0:
            break

        print("T ", T)
        T *= a

        # if T < 0.0001:
        #     T = 10
        #     n_changes += 1
        

    # print(neighbor.fitness)
    best_cube.print()
    print("Bestest fit", best_cube.fitness)
    print(moves)

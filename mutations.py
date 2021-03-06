import os
from cube import Cube
from random import randint, random, uniform, shuffle
from math import exp
from copy import deepcopy
from chromossomes import *

def mutation(cube, chromossome):
    chromossome = deepcopy(chromossome)
    moves = Cube.available_moves

    for i in range(len(chromossome['val'])):
        if random() < MUTATION_PROB: #get_mutation_prob(0.2, cube.max_fitness, chromossome['fit']):
            new_move = moves[randint(0, len(moves)-1)]
    
            if i == 0:
                while chromossome['val'][i+1][0] == new_move[0]:
                    new_move = moves[randint(0, len(moves)-1)]

            elif i == len(chromossome['val'])-1:
                while chromossome['val'][i-1][0] == new_move[0]:
                    new_move = moves[randint(0, len(moves)-1)]
            else:
                while chromossome['val'][i-1][0] == new_move[0] and chromossome['val'][i+1][0] == new_move[0]:
                    new_move = moves[randint(0, len(moves)-1)]

            chromossome['val'][i] = new_move

    return chromossome


def mutation_to_best_fit(cube, chromossome):
    cube = Cube(cube)
    chromossome = deepcopy(chromossome)
    moves = Cube.available_moves

    for i in range(len(chromossome['val'])):
        if random() < MUTATION_PROB: #get_mutation_prob(0.2, cube.max_fitness, chromossome['fit']):
            moves_cpy = deepcopy(moves)
            if i > 0 and chromossome['val'][i-1][0] != 'n':
                moves_cpy.remove(chromossome['val'][i-1][0])
                moves_cpy.remove(chromossome['val'][i-1][0]+"'")
                moves_cpy.remove(chromossome['val'][i-1][0]+"2")

            best_move = ''
            best_fit = cube.max_fitness

            for move in moves_cpy:
                tmp_cube = Cube(cube)
                for m in range(0, i):
                    tmp_cube.make_move(chromossome['val'][m])
                tmp_cube.make_move(move)
                tmp_cube.calc_fitness()

                if tmp_cube.fitness <= best_fit:
                    best_move = move
                    best_fit = tmp_cube.fitness

            

            
            # new_move = moves_cpy[randint(0, len(moves)-1)]
            chromossome['val'][i] = best_move

    return chromossome

def worst_fit_mutation(cube, chromossome):
    moves = Cube.available_moves
    best_worst_index = get_worst_fit_index(cube, chromossome)+1
    new_move = moves[randint(0, len(moves)-1)]
    
    if best_worst_index == 0:
        while chromossome['val'][best_worst_index+1][0] == new_move[0]:
            new_move = moves[randint(0, len(moves)-1)]

    elif best_worst_index == len(chromossome['val'])-1:
        while chromossome['val'][best_worst_index-1][0] == new_move[0]:
            new_move = moves[randint(0, len(moves)-1)]
    else:
        while chromossome['val'][best_worst_index-1][0] == new_move[0] and chromossome['val'][best_worst_index+1][0] == new_move[0]:
            new_move = moves[randint(0, len(moves)-1)]

    chromossome['val'][best_worst_index] = new_move
    return deepcopy(chromossome)


def mutation_exchange(chromossome):
    for i in range(len(chromossome['val'])):
        if random() < MUTATION_PROB:
            random_pos = randint(0, len(chromossome['val'])-1)

            while random_pos == i:
                random_pos = randint(0, len(chromossome['val'])-1)

            chromossome['val'][random_pos], chromossome['val'][i] = chromossome['val'][i], chromossome['val'][random_pos]

    return chromossome

def mutation_by_random_generation(cube, chromossome):
    # cut_point = get_best_fit_index(cube, chromossome)
    cut_point = randint(int(len(chromossome['val']) * (4/5)), len(chromossome['val'])-1)
    random_chromossome = generate_chromossome(5)

    mutated_chromossome = {
        'fit': 0,
        'val': chromossome['val'][:cut_point] + random_chromossome['val']#[cut_point:]# + chromossome['val'][cut_point2:]
    } 

    evaluate_solution(cube, mutated_chromossome)

    return mutated_chromossome

def uniform_mutation(cube, chromossome):
    chrom = deepcopy(chromossome)
    random_chromossome = generate_chromossome(len(chrom['val']))
    
    for i in range(len(chrom['val'])):
        for h in range(0, len(chrom['val'][i]), 2):
            chrom['val'][i][h] = random_chromossome['val'][i][h]

    evaluate_solution(cube, chrom)

    return chrom

def get_mutation_prob(max_prob, max_fitness, curr_fitness):
    return -((max_prob - MUTATION_PROB) * curr_fitness / max_fitness) + MUTATION_PROB
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
    cut_point = get_best_fit_index(cube, chromossome)
    random_chromossome = generate_chromossome()

    mutated_chromossome = {
        'fit': 0,
        'val': chromossome['val'][:cut_point] + random_chromossome['val'][cut_point:]# + chromossome['val'][cut_point2:]
    } 

    evaluate_solution(cube, mutated_chromossome)

    return mutated_chromossome

def uniform_mutation(cube, chromossome):
    chrom = deepcopy(chromossome)
    random_chromossome = generate_chromossome(len(chrom['val']))
    
    for i in range(0, len(chrom['val']), 2):
        chrom['val'][i] = random_chromossome['val'][i]

    evaluate_solution(cube, chrom)

    return chrom

def get_mutation_prob(max_prob, max_fitness, curr_fitness):
    return -((max_prob - MUTATION_PROB) * curr_fitness / max_fitness) + MUTATION_PROB
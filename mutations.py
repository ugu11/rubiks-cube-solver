import os
from cube import Cube
from random import randint, random, uniform, shuffle
from math import exp
from copy import deepcopy
from populations_ops import *

def mutation(chromossome):
    moves = ["u", "u'", "f", "f'", "l", "l'", "r", "r'", "d", "d'", "b", "b'", 'u2', 'b2', 'f2', 'l2', 'r2', 'd2', 'n']
    random_pos = randint(0, len(chromossome))

    new_move = moves[randint(0, len(moves)-1)]
    
    if random_pos == 0:
        while chromossome['val'][random_pos+1][0] in new_move:
            new_move = moves[randint(0, len(moves)-1)]

    elif random_pos == len(chromossome)-1:
        while chromossome['val'][random_pos-1][0] in new_move:
            new_move = moves[randint(0, len(moves)-1)]
    else:
        while chromossome['val'][random_pos-1][0] in new_move and chromossome['val'][random_pos+1][0] in new_move:
            new_move = moves[randint(0, len(moves)-1)]

    chromossome['val'][random_pos] = new_move
    return chromossome

def mutation_exchange(chromossome):
    random_pos = randint(0, len(chromossome))
    random_pos1 = random_pos

    while random_pos == random_pos1:
        random_pos1 = randint(0, len(chromossome))

    chromossome['val'][random_pos], chromossome['val'][random_pos1] = chromossome['val'][random_pos1], chromossome['val'][random_pos]
    return chromossome

def mutation_by_random_generation(cube, chromossome):
    cut_point = get_best_fit_index(cube, chromossome)
    cut_point2 = randint(cut_point+1, CHROMOSSOME_SIZE)
    random_chromossome = generate_chromossome()

    mutated_chromossome = {
        'fit': 0,
        'val': chromossome['val'][:cut_point] + random_chromossome['val'][cut_point:cut_point2] + chromossome['val'][cut_point2:]
    } 

    evaluate_solution(cube, mutated_chromossome)

    return mutated_chromossome

def uniform_mutation(cube, chromossome):
    cut_point = get_best_fit_index(cube, chromossome)
    random_chromossome = generate_chromossome()
    
    for i in range(cut_point, len(chromossome['val']), 2):
        chromossome['val'][i] = random_chromossome['val'][i]

    evaluate_solution(cube, chromossome)

    return chromossome


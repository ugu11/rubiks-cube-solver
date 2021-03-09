import os
from cube import Cube
from random import randint, random, uniform, shuffle
from math import exp
from copy import deepcopy


N_GENERATIONS = 150
POP_SIZE = 100
CROSSOVER_PROB = 0.7
MUTATION_PROB = 0.3
CHROMOSSOME_SIZE = 6

def get_fit_1h(chromossome):
    return chromossome['fit']

def get_fit_2h(chromossome):
    return chromossome['fit']


def get_fit(chromossome):
    return chromossome['fit']

def generate_chromossome(size=None):
    moves = Cube.available_moves
    moves = moves[:len(moves)-1]
    chromossome = []

    if size == None:
        chrom_size = CHROMOSSOME_SIZE
    else:
        chrom_size = size

    for h in range(chrom_size):
        if len(chromossome) > 0:
            while (chromossome[h-1][0] == move[0] and chromossome[h-1] + "'" == move
            or chromossome[h-1] == move):
                move = moves[randint(0, len(moves)-1)]
        else:
            move = moves[randint(0, len(moves)-1)]
        
        chromossome.append(move)

    # chromossome += ['n'] * (CHROMOSSOME_SIZE - 20)
    return {
        'fit': 0,
        'val': chromossome
    }

def evaluate_solution(cube, chromossome):
    cube = Cube(cube)

    # First half
    for move in chromossome['val']:
        if not move[0] == 'n':
            cube.make_move(move)

    fitness = cube.calc_fitness()

    chromossome['fit'] = fitness

def get_best_fit_index(cube, chromossome):
    cube = Cube(cube)
    best_fit = cube.max_fitness
    best_index = 0

    for i in range(1, len(chromossome['val'])-1):
        move = chromossome['val'][i]
        cube.make_move(move)
        tmp_fit = cube.calc_fitness()
        if tmp_fit < best_fit:
            best_fit = tmp_fit
            best_index = i

    return best_index

def get_worst_fit_index(cube, chromossome):
    cube = Cube(cube)
    worst_fit = cube.max_fitness
    worst_index = 0

    for i in range(len(chromossome['val'])):
        move = chromossome['val'][i]
        cube.make_move(move)
        tmp_fit = cube.calc_fitness()
        if tmp_fit > worst_fit:
            worst_fit = tmp_fit
            worst_index = i

    return worst_index


def evaluate_pop(cube, population):
    i = 0
    while i < len(population):
        if len(population[i]['val']) == 0:
            population.pop(i)
            continue
        evaluate_solution(cube, population[i])
        i += 1

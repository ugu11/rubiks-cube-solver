import os
from cube import Cube
from random import randint, random, uniform, shuffle
from math import exp
from copy import deepcopy
from populations_ops import *

def crossover_1_point(chromossome1, chromossome2):
    smallest_len = chromossome1 if len(chromossome1['val']) < len(chromossome2['val']) else chromossome2
    cut_point = randint(1, len(smallest_len['val'])-1)
    offspring1 = {
        'fit': 0,
        'val': chromossome1['val'][:cut_point] + chromossome2['val'][cut_point:]
    }
    offspring2 = {
        'fit': 0,
        'val': chromossome2['val'][:cut_point] + chromossome1['val'][cut_point:]
    }
    return [offspring1, offspring2]

def crossover_1_point_same_fit(cube, chromossome1, chromossome2):
    cube_cpy = Cube(cube)
    smallest_len = chromossome1 if len(chromossome1['val']) < len(chromossome2['val']) else chromossome2
    i = get_best_fit_index(cube_cpy, chromossome1)
    h = get_best_fit_index(cube_cpy, chromossome2)

    offspring1 = {
        'fit': 0,
        'val': chromossome1['val'][:i+1] + chromossome2['val'][h+1:]
    }
    
    offspring2 = {
        'fit': 0,
        'val': chromossome2['val'][:i+1] + chromossome1['val'][h+1:]
    }

    evaluate_solution(cube_cpy, offspring1)
    evaluate_solution(cube_cpy, offspring2)

    return [offspring1, offspring2]

    


def crossover_2_point(chromossome1, chromossome2):
    smallest_len = chromossome1 if len(chromossome1['val']) < len(chromossome2['val']) else chromossome2
    cut_point1 = randint(0, len(smallest_len['val'])-1)
    cut_point2 = randint(cut_point1, len(smallest_len['val'])-1)

    offspring1 = {
        'fit': 0,
        'val': chromossome1['val'][:cut_point1] + chromossome2['val'][cut_point1:cut_point2] + chromossome1['val'][cut_point2:]
    }
    offspring2 = {
        'fit': 0,
        'val': chromossome2['val'][:cut_point1] + chromossome1['val'][cut_point1:cut_point2] + chromossome2['val'][cut_point2:]
    }
    return [offspring1, offspring2]

def generate_mask(size):
    mask = []
    random_step1 = randint(1, 3)
    random_step2 = randint(1, 3)

    category = True
    for i in range(0, size, random_step1 + random_step2):
        # if category:
        mask += ['1'] * random_step1
        # else:
        mask += ['0'] * random_step2

        category = not category

    return "".join(mask)[:size]


def uniform_crossover(chromossome1, chromossome2):
    max_len = max([len(chromossome1['val']), len(chromossome2['val'])])
    mask = generate_mask(max_len)
    offspring1 = chromossome1['val'] + ['n'] * (max_len - len(chromossome1['val']))
    offspring2 = chromossome2['val'] + ['n'] * (max_len - len(chromossome2['val']))

    for i in range(max_len):
        if mask[i] == '0':
            offspring1[i] = offspring2[i]
            offspring2[i] = offspring1[i]

    offspring1 = { 'fit': 0, 'val': offspring1 }
    offspring2 = { 'fit': 0, 'val': offspring2 }

    # evaluate_solution(cube, offspring1)
    # evaluate_solution(cube, offspring2)

    return [offspring1, offspring2]


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
    cut_point1 = randint(1, len(smallest_len['val'])-3)
    cut_point2 = randint(cut_point1+1, len(smallest_len['val'])-1)

    offspring1 = {
        'fit': 0,
        'val': chromossome1['val'][:cut_point1] + chromossome2['val'][cut_point1:cut_point2] + chromossome1['val'][cut_point2:]
    }
    offspring2 = {
        'fit': 0,
        'val': chromossome2['val'][:cut_point1] + chromossome1['val'][cut_point1:cut_point2] + chromossome2['val'][cut_point2:]
    }
    return [offspring1, offspring2]


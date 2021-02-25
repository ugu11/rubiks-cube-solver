import os
from cube import Cube
from random import randint, random, uniform, shuffle
from math import exp
from copy import deepcopy
from populations_ops import *

def crossover_1_point(chromossome1, chromossome2):
    cut_point = randint(1, len(chromossome1)-1)
    offspring1 = {
        'fit': 0,
        'val': chromossome1['val'][:cut_point] + chromossome2['val'][cut_point:]
    }
    offspring2 = {
        'fit': 0,
        'val': chromossome2['val'][:cut_point] + chromossome1['val'][cut_point:]
    }
    return [offspring1, offspring2]

def crossover_2_point(chromossome1, chromossome2):
    cut_point1 = randint(1, len(chromossome1)-1)
    cut_point2 = randint(cut_point1+1, len(chromossome1))

    offspring1 = {
        'fit': 0,
        'val': chromossome1['val'][:cut_point1] + chromossome2['val'][cut_point1:cut_point2] + chromossome1['val'][cut_point2:]
    }
    offspring2 = {
        'fit': 0,
        'val': chromossome2['val'][:cut_point1] + chromossome1['val'][cut_point1:cut_point2] + chromossome2['val'][cut_point2:]
    }
    return [offspring1, offspring2]


import os
from cube import Cube
from random import randint, random, uniform, shuffle
from math import exp
from copy import deepcopy
from populations_ops import *

def roullete_selection(cube, population):
    fitness_sum = 0
    normalized_fits = []
    selected_population = []
    population.sort(key=get_fit)

    # Get fitness_sum
    for chromossome in population:
        fitness_sum += (cube.max_fitness - chromossome['fit'])

    total_norm_sum = 0

    # Normalize fitness
    for chromossome in population:
        total_norm_sum += (cube.max_fitness - chromossome['fit']) / fitness_sum
        normalized_fits.append(total_norm_sum)

    # Spin roullete
    for i in range(int(len(population))):
        roullete_num = random()#uniform(0.8, 1)
        selected_offspring = None

        for h in range(len(normalized_fits)-1):
            if roullete_num >= normalized_fits[h] and roullete_num < normalized_fits[h+1]:
                selected_offspring = population[h]

        if selected_offspring == None:
            selected_offspring = population[len(population)-1]

        selected_population.append(selected_offspring)


    return selected_population

def truncated_selection(cube, population):
    BEST_RATE = 0.4
    n_to_select = int(POP_SIZE * BEST_RATE)

    population.sort(key=get_fit)

    return population[:n_to_select]

def tournment_selection(cube, population, tournment_size):
    selected = []
    k = 0.85

    for i in range(0, len(population)):
        # participants = []
        best_chromossome = population[0]
        random_factor = random()

        for h in range(0, tournment_size):
            random_chrmossome_pos = randint(0, len(population)-1)
            # print(random_chrmossome_pos)
            if (best_chromossome == None
            or (random_factor < k and population[random_chrmossome_pos]['fit'] < best_chromossome['fit'])
            or (random_factor >= k and population[random_chrmossome_pos]['fit'] > best_chromossome['fit'])):
                best_chromossome = population[random_chrmossome_pos]

        selected.append(deepcopy(best_chromossome))


    return selected

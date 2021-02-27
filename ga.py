import os
from cube import Cube
from random import randint, random, uniform, shuffle
from math import exp
from copy import deepcopy

from mutations import *
from crossovers import *
from selections import *
from populations_ops import *

def apply_genetic_operators(cube, population, elite):
    mating_pool = []

    for i in range(0, len(population), 2):
        new_offsprings = [deepcopy(population[i]), deepcopy(population[i+1])]
        mating_candidates = []
        random_prob = random()
        if random_prob <= CROSSOVER_PROB:
            cross_offsprings = deepcopy(new_offsprings)
            cross_offsprings = crossover_2_point(cross_offsprings[0], cross_offsprings[1])
            evaluate_solution(cube, cross_offsprings[0])
            evaluate_solution(cube, cross_offsprings[1])

            mating_candidates = cross_offsprings

            mating_pool += mating_candidates

        mut_offsprings = deepcopy(new_offsprings)
        mut_offsprings[0] = mutation(cube, mut_offsprings[0])
        mut_offsprings[1] = mutation(cube, mut_offsprings[1])
        
        evaluate_solution(cube, mut_offsprings[0])
        evaluate_solution(cube, mut_offsprings[1])

        mating_pool += mut_offsprings

    offsprings = mating_pool

    return offsprings

def genetic_algorithm(cube):
    cube = Cube(cube)

    population = generate_pop()
    evaluate_pop(cube, population)

    i = 0
    elite = None
    best_chromossome = None
    n_unimproved_gens = 0

    while i < N_GENERATIONS:
        evaluate_pop(cube, population)

        elite = deepcopy(population[:int(len(population) * 0.1)])

        # Selections
        parents = deepcopy(roullete_selection(cube, population))
        population = apply_genetic_operators(cube, parents, elite)

        population = random_kill(cube, population, int(len(population) * 0.2))
        population += elite
        population.sort(key=get_fit)
        population = social_disaster(cube, population)

        if i % 50 == 0:
            print("BEST OVERTAKE")
            population = best_overtake(cube, population)

        population = repair(population)
        evaluate_pop(cube, population)
        population.sort(key=get_fit)

        population = population[:POP_SIZE]

        if best_chromossome != population[0]:
            best_chromossome = deepcopy(population[0])
            n_unimproved_gens = 0
        elif n_unimproved_gens >= 600 and len(population['val']) < 50:
            random_generated_moves = []

            for i in range(5):
                random_generated_moves.append(cube.available_moves[randint(0, len(cube.available_moves)-1)])

            population['val'] += random_generated_moves
            best_chromossome = deepcopy(population[0])
            n_unimproved_gens = 0
        else:
            n_unimproved_gens += 1

        if population[0]['fit'] == 0: break
        print("GENERATION", i, "   Curr best fit:", population[0]['fit'], "    Len: ", len(population), "    N moves", cube.n_moves, "    parents", len(parents))
        print([c['fit'] for c in population])
        print([m for m in population[0]['val']])
        print([m for m in population[1]['val']])
        i += 1

    print([c['fit'] for c in population])
    print("\nBest fit: ", population[0]['fit'])
    print(' '.join(population[0]['val']))
    # m = ["b2", "u", "d2", "f", "r2", "f2", "d2", "u2", "f'", "u2", "f2", "u2", "r2", "d2", "r", "b'", "d'", "u2", "b'", "r'", "b2"]

    population = repair(population)
    evaluate_pop(cube, population)
    print("\nBest fit: ", population[0]['fit'])
    print(' '.join(population[0]['val']))
    # print("\nScramble: ")
    # print(' '.join(m))

    return population[0]





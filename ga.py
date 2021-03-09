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
        # if len(population) % 2 == 0:
        new_offsprings = [deepcopy(population[i]), deepcopy(population[i+1])]
        mating_candidates = []
        random_prob = random()
        if random_prob <= CROSSOVER_PROB:
            cross_offsprings = deepcopy(new_offsprings)
            cross_offsprings = crossover_2_point(cross_offsprings[0], cross_offsprings[1])
            # cross_offsprings = crossover_1_point(cross_offsprings[0], cross_offsprings[1])
            # cross_offsprings = uniform_crossover(cross_offsprings[0], cross_offsprings[1])
            evaluate_pop(cube, cross_offsprings)

            mating_candidates = cross_offsprings

            mating_pool += mating_candidates

        mut_offsprings = deepcopy(new_offsprings)
        mut_offsprings[0] = mutation(cube, mut_offsprings[0])
        mut_offsprings[1] = mutation(cube, mut_offsprings[1])
        # mut_offsprings[0] = mutation_to_best_fit(cube, mut_offsprings[0])
        # mut_offsprings[1] = mutation_to_best_fit(cube, mut_offsprings[1])
        # mut_offsprings[0] = uniform_mutation(cube, mut_offsprings[0])
        # mut_offsprings[1] = uniform_mutation(cube, mut_offsprings[1])
        
        evaluate_pop(cube, mut_offsprings)

        mating_pool += mut_offsprings

    offsprings = mating_pool

    return offsprings

def genetic_algorithm(cube, chrom_size):
    # CHROMOSSOME_SIZE = chrom_size
    cube.print()
    cube = Cube(cube)
    print("INITIAL FIT:", cube.fitness)
    cube.print()

    if cube.fitness < 150:
        population = generate_pop(chrom_size=15)
    else:
        population = generate_pop(chrom_size=chrom_size)
        
    print("=> ", population[0])
    evaluate_pop(cube, population)
    population = repair(population)
    population.sort(key=get_fit)
    population = population[:POP_SIZE]
    print("=> ", population[0])

    i = 0
    elite = None
    best_chromossome = None
    n_unimproved_gens = 0


    while i < N_GENERATIONS:

        elite = deepcopy(population[:int(len(population) * 0.1)])

        # if i > 0 and i % 30 == 0:
        #     print("GROWUP")
        #     population += growup(cube, population[:10])

        # Selections
        parents = deepcopy(roullete_selection(cube, population))
        population = apply_genetic_operators(cube, parents, elite)

        population = random_kill(cube, population, int(len(population) * 0.1))
        # population = repair(population)
        # evaluate_pop(cube, population)
        # population.sort(key=get_fit)

        # population = sorted(population, key=lambda chrom: (get_fit_2h(chrom), get_fit_1h(chrom)))
        population = social_disaster(cube, population)

        # evaluate_pop(cube, population)
        # population.sort(key=get_fit)
        # if i % 50 == 0:
        #     print("BEST OVERTAKE")
        #     # population = renovate_half(cube, population)
        #     population = best_overtake(cube, population)

        population = repair(population)
        population += elite

        # if best_chromossome != None and best_chromossome['fit'] != population[0]['fit']:
        #     best_chromossome = deepcopy(population[0])
        #     n_unimproved_gens = 0
        # elif n_unimproved_gens >= 80:
        #     print("Generating new genes")
        #     for r in range(10):
        #         random_generated_moves = []

        #         for h in range(6):
        #             random_generated_moves.append(cube.available_moves[randint(0, 18)])

        #         new_chrom = population[0]['val'] + random_generated_moves
        #         population.append({'fit': 0, 'val': new_chrom})
        #     best_chromossome = deepcopy(population[0])
        #     n_unimproved_gens = 0
        # else:
        #     n_unimproved_gens += 1

        evaluate_pop(cube, population)
        population.sort(key=get_fit)
        # population = sorted(population, key=lambda chrom: (get_fit(chrom), len(chrom['val'])))
        population = population[:POP_SIZE]

        if population[0]['fit'] == 0: break
        print("GENERATION", i, "   Curr best fit:", population[0]['fit'], "    Len: ", len(population), "    N moves", cube.n_moves, "    parents", len(parents))
        print([(c['fit'], len(c['val'])) for c in population])
        print([m for m in population[0]['val']])
        print([m for m in population[1]['val']])
        i += 1
 
    print("Final pop\n", [c['fit'] for c in population])
    print("\nBest fit: ", population[0]['fit'])
    print("Best sol: ", population[0]['val'])

    cube.print()

    print("============================================")
    # print(' '.join(population[0]['val']))
    # m = ["b2", "u", "d2", "f", "r2", "f2", "d2", "u2", "f'", "u2", "f2", "u2", "r2", "d2", "r", "b'", "d'", "u2", "b'", "r'", "b2"]

    # population = repair(population)
    # evaluate_pop(cube, population)
    # print("\nBest fit: ", population[0]['fit'])
    # print(' '.join(population[0]['val']))
    # print("\nScramble: ")
    # print(' '.join(m))

    return population[0]





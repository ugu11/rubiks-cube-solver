import os
from cube import Cube
from random import randint, random, uniform, shuffle
from math import exp
from copy import deepcopy

from mutations import *
from crossovers import *
from selections import *
from populations_ops import *

def is_move_none(m): return m == 'n'

def repair_chromossome(chromossome):
    cube = Cube()
    chromossome_val = chromossome['val']
    i = 0
    while i < len(chromossome_val)-1:
        if chromossome_val[i][0] == chromossome_val[i+1][0] and chromossome_val[i][0] != 'n' and chromossome_val[i+1][0] != 'n':
            if '2' in chromossome_val[i]:
                if '2' in chromossome_val[i+1]:
                    chromossome_val[i] = 'n'
                    chromossome_val[i+1] = 'n'
                elif "'" in chromossome_val[i+1]:
                    chromossome_val[i] = chromossome_val[i]
                    chromossome_val[i+1] = 'n'
                else:
                    chromossome_val[i] = chromossome_val[i] + "'"
                    chromossome_val[i+1] = 'n'
            elif chromossome_val[i] == chromossome_val[i+1]:
                chromossome_val[i] = chromossome_val[i] + '2'
                chromossome_val[i+1] = 'n'
            elif '2' in chromossome_val[i+1]:
                if '2' in chromossome_val[i]:
                    chromossome_val[i] = 'n'
                    chromossome_val[i+1] = 'n'
                elif "'" in chromossome_val[i]:
                    chromossome_val[i] = chromossome_val[i]
                    chromossome_val[i+1] = 'n'
                else:
                    chromossome_val[i] = chromossome_val[i] + "'"
                    chromossome_val[i+1] = 'n'
            elif (("'" not in chromossome_val[i] and not "2" in chromossome_val[i] and "'" in chromossome_val[i+1])
            or ("'" in chromossome_val[i] and "'" not in chromossome_val[i+1] and not "2" in chromossome_val[i+1])):
                chromossome_val[i] = 'n'
                chromossome_val[i+1] = 'n'
        elif (i > len(chromossome_val)-2
        and chromossome_val[i][0] != 'n' and chromossome_val[i+1][0] != 'n' and chromossome_val[i+2][0] != 'n'
        and chromossome_val[i][0] == cube.oposite_face[chromossome_val[i+1][0]] and i+2 < len(chromossome)-1):
            if '2' in chromossome_val[i]:
                if '2' in chromossome_val[i+2]:
                    chromossome_val[i] = 'n'
                    chromossome_val[i+2] = 'n'
                elif "'" in chromossome_val[i+2]:
                    chromossome_val[i] = chromossome_val[i]
                    chromossome_val[i+2] = 'n'
                else:
                    chromossome_val[i] = chromossome_val[i] + "'"
                    chromossome_val[i+2] = 'n'
            elif chromossome_val[i] == chromossome_val[i+2]:
                    chromossome_val[i] = chromossome_val[i] + '2'
                    chromossome_val[i+2] = 'n'
            elif (("'" not in chromossome_val[i] and "'" in chromossome_val[i+2])
            or ("'" in chromossome_val[i] and "'" not in chromossome_val[i+2])):
                    chromossome_val[i] = 'n'
                    chromossome_val[i+2] = 'n'

            elif '2' in chromossome_val[i+2]:
                if '2' in chromossome_val[i]:
                    chromossome_val[i] = 'n'
                    chromossome_val[i+2] = 'n'
                elif "'" in chromossome_val[i]:
                    chromossome_val[i] = chromossome_val[i]
                    chromossome_val[i+2] = 'n'
                else:
                    chromossome_val[i] = chromossome_val[i] + "'"
                    chromossome_val[i+2] = 'n'
        # print("-", chromossome_val[i])
            
        i += 1

    chromossome_val.sort(key=is_move_none)                
    chromossome['val'] = chromossome_val

    return chromossome

def fix_empty_moves(chromossome):
    cube = Cube()
    new_chromossomes = []
    n_count = 0
    moves = ["u", "u'", "f", "f'", "l", "l'", "r", "r'", "d", "d'", "b", "b'", 'u2', 'b2', 'f2', 'l2', 'r2', 'd2']
    chromossome_val = deepcopy(chromossome['val'])

    for i in range(len(chromossome_val)-1, 0, -1):
        if chromossome_val[i] == 'n':
            n_count += 1
        else: break

    last_move = chromossome_val[len(chromossome_val) - n_count - 1]
    second_last_move = chromossome_val[len(chromossome_val) - n_count - 2]

    for i in range(n_count):
        new_move = last_move
        while (new_move[0] == last_move[0] or (new_move[0] == second_last_move[0] and last_move[0] == cube.oposite_face[new_move[0]])):
            new_move = moves[randint(0, len(moves)-1)]
        chromossome_val[len(chromossome_val) - n_count + i] = new_move
        new_chrom = {
            'fit': 0,
            'val': deepcopy(chromossome_val)
        }

        new_chromossomes.append(new_chrom)

    return new_chromossomes


def repair(population):
    new_population = []
    for i in range(len(population)):
        population[i] = repair_chromossome(population[i])
        new_chromossomes = fix_empty_moves(population[i])
        new_population += new_chromossomes

    population += new_population

    return population


def apply_genetic_operators(cube, population, elite):
    mating_pool = []

    for i in range(0, len(population), 2):
        new_offsprings = [deepcopy(population[i]), deepcopy(population[i+1])]
        mating_candidates = []
        random_prob = random()
        if random_prob <= CROSSOVER_PROB:
            cross_offsprings = deepcopy(new_offsprings)
            cross_offsprings = crossover_1_point(cross_offsprings[0], cross_offsprings[1])

            # cross_offsprings[0] = mutation_by_random_generation(cube, cross_offsprings[0])
            # cross_offsprings[1] = mutation_by_random_generation(cube, cross_offsprings[1])
            evaluate_solution(cube, cross_offsprings[0])
            evaluate_solution(cube, cross_offsprings[1])

            mating_candidates = cross_offsprings
            # mating_candidates.sort(key=get_fit)

            mating_pool += mating_candidates
        
        if random_prob <= MUTATION_PROB:
            mut_offsprings = deepcopy(new_offsprings)
            # mut_offsprings[0] = mutation_exchange(mut_offsprings[0])
            # mut_offsprings[1] = mutation_exchange(mut_offsprings[1])
            mut_offsprings[0] = mutation(mut_offsprings[0])
            mut_offsprings[1] = mutation(mut_offsprings[1])
            # mut_offsprings[0] = mutation_by_random_generation(cube, mut_offsprings[0])
            # mut_offsprings[1] = mutation_by_random_generation(cube, mut_offsprings[1])

            # mut_offsprings[0] = uniform_mutation(cube, mut_offsprings[0])
            # mut_offsprings[1] = uniform_mutation(cube, mut_offsprings[1])

            
            evaluate_solution(cube, mut_offsprings[0])
            evaluate_solution(cube, mut_offsprings[1])

            mating_candidates = mut_offsprings
            mating_candidates.sort(key=get_fit)

            mating_pool += mating_candidates

        # if new_offsprings[0]['fit'] < population[i]['fit'] and new_offsprings[0]['fit'] < population[i+1]['fit']:
        #     mating_pool.append(new_offsprings[0])
        # else:
        #     mating_pool.append(population[i])

        # if new_offsprings[1]['fit'] < population[i]['fit'] and new_offsprings[1]['fit'] < population[i+1]['fit']:
        #     mating_pool.append(new_offsprings[1])
        # else:
        #     mating_pool.append(population[i+1])

        # mating_pool += new_offsprings


    # if elite != None:
    #     population += elite

    mating_pool.sort(key=get_fit)

    offsprings = mating_pool[:POP_SIZE]

    return offsprings

def genetic_algorithm(cube):
    cube = Cube(cube)

    population = generate_pop()
    evaluate_pop(cube, population)

    i = 0
    elite = None

    # chrm = generate_chromossome()
    # pop = []

    # for i in range(4):
    #     pop.append(deepcopy(chrm))

    # for i in range(6):
    #     pop.append(generate_chromossome())

    # evaluate_pop(cube, pop)
    # pop.sort(key=get_fit)

    # print([c['fit'] for c in pop])

    # pop = social_disaster(cube, pop)

    # print([c['fit'] for c in pop])

    # print(population[0]['fit'], population[0]['val'], len(population[0]['val']))
    # m = mutation_by_random_generation(cube, population[0])
    # m = mutation_by_random_generation(cube, m)
    # print(m['fit'], m['val'], len(m['val']))
    # m = mutation_by_random_generation(cube, m)
    # print(m['fit'], m['val'], len(m['val']))
    # m = mutation_by_random_generation(cube, m)
    # print(m['fit'], m['val'], len(m['val']))

    

            # if group_count > 5:

    while i < N_GENERATIONS:#population[0]['fit'] != 0:
        evaluate_pop(cube, population)

        elite = deepcopy(population[:int(POP_SIZE * 0.1)])

        # Selections
        parents = deepcopy(roullete_selection(cube, population))
        # parents = deepcopy(tournment_selection(cube, population, 2))

        population = apply_genetic_operators(cube, parents, elite)

        # population.sort(key=get_fit)
        population = random_kill(cube, population, int(POP_SIZE * 0.05))
        population += elite
        population.sort(key=get_fit)
        population = social_disaster(cube, population)


        population = repair(population)
        evaluate_pop(cube, population)
        population.sort(key=get_fit)

        population = population[:POP_SIZE]

        if population[0]['fit'] == 0: break
        print("GENERATION", i, "   Curr best fit:", population[0]['fit'], "    Len: ", len(population), "    N moves", cube.n_moves, "    parents", len(parents))
        print([c['fit'] for c in population])
        # for c in population[:5]:
        #     print(c)
        # print(population[0]['val'])
        # print(population[1]['val'])
        i += 1

    print([c['fit'] for c in population])

    # print(population)
    print([c['fit'] for c in population])
    print("\nBest fit: ", population[0]['fit'])
    print(' '.join(population[0]['val']))
    m = ["b2", "u", "d2", "f", "r2", "f2", "d2", "u2", "f'", "u2", "f2", "u2", "r2", "d2", "r", "b'", "d'", "u2", "b'", "r'", "b2"]

    population = repair(population)
    evaluate_pop(cube, population)
    print("\nBest fit: ", population[0]['fit'])
    print(' '.join(population[0]['val']))
    print("\nScramble: ")
    print(' '.join(m))





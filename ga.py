import os
from cube import Cube
from random import randint, random, uniform
from math import exp
from copy import deepcopy

N_GENERATIONS = 500
POP_SIZE = 100
CROSSOVER_PROB = 0.8
MUTATION_PROB = 0.2
CHROMOSSOME_SIZE = 25


def get_fit(chromossome):
    return chromossome['fit']

def generate_chromossome():
    moves = ["u", "u'", "f", "f'", "l", "l'", "r", "r'", "d", "d'", "b", "b'", 'u2', 'b2', 'f2', 'l2', 'r2', 'd2']
    chromossome = []

    for h in range(CHROMOSSOME_SIZE):
        if len(chromossome) > 0:
            while (chromossome[h-1][0] == move[0] and chromossome[h-1] + "'" == move
            or chromossome[h-1] == move):
                move = moves[randint(0, len(moves)-1)]
        else:
            move = moves[randint(0, len(moves)-1)]
        
        chromossome.append(move)

    return {
        'fit': 0,
        'val': chromossome
    }

def generate_pop():
    population = []

    for i in range(POP_SIZE):
        chromossome = generate_chromossome()
        population.append(chromossome)
    return population

def evaluate_solution(cube, chromossome):
    cube = Cube(cube)
    
    for move in chromossome['val']:
        cube.make_move(move)

    cube.calc_fitness()

    chromossome['fit'] = cube.fitness

def evaluate_pop(cube, population):
    for chromossome in population:
        evaluate_solution(cube, chromossome)

def roullete_selection(cube, population):
    fitness_sum = 0
    normalized_fits = []
    selected_population = []
    population.sort(key=get_fit, reverse=True)

    # Get fitness_sum
    for chromossome in population:
        fitness_sum += chromossome['fit']

    total_norm_sum = 0

    # Normalize fitness
    for chromossome in population:
        total_norm_sum += chromossome['fit'] / fitness_sum
        normalized_fits.append(total_norm_sum)

    # print(normalized_fits)

    # Spin roullete
    for i in range(int(POP_SIZE)):
        roullete_num = random()#uniform(0.8, 1)
        selected_offspring = None

        for h in range(len(normalized_fits)-1):
            if roullete_num >= normalized_fits[h] and roullete_num < normalized_fits[h+1]:
                selected_offspring = population[h]

        if selected_offspring == None:
            selected_offspring = population[len(population)-1]

        selected_population.append(selected_offspring)


    return selected_population

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

def mutation(chromossome):
    moves = ["u", "u'", "f", "f'", "l", "l'", "r", "r'", "d", "d'", "b", "b'", 'u2', 'b2', 'f2', 'l2', 'r2', 'd2']
    random_pos = randint(0, len(chromossome))

    new_move = moves[randint(0, len(moves)-1)]
    
    if random_pos == 0:
        # while (chromossome['val'][random_pos+1] == new_move
        # or ("'" in new_move and new_move[0] == chromossome['val'][random_pos+1]) 
        # or ("'" not in new_move and chromossome['val'][random_pos+1] == new_move + "'") ):
        while chromossome['val'][random_pos+1][0] in new_move:
            new_move = moves[randint(0, len(moves)-1)]

    elif random_pos == len(chromossome)-1:
        # while (chromossome['val'][random_pos-1] == new_move
        # or ("'" in new_move and new_move[0] == chromossome['val'][random_pos-1]) 
        # or ("'" not in new_move and chromossome['val'][random_pos-1] == new_move + "'") ):
        #     new_move = moves[randint(0, len(moves)-1)]


        while chromossome['val'][random_pos-1][0] in new_move:
            new_move = moves[randint(0, len(moves)-1)]
    else:
        # while (chromossome['val'][random_pos+1] == new_move
        # or chromossome['val'][random_pos-1] == new_move
        # or ("'" in new_move and new_move[0] == chromossome['val'][random_pos+1]) 
        # or ("'" not in new_move and chromossome['val'][random_pos+1] == new_move + "'") 
        # or ("'" in new_move and new_move[0] == chromossome['val'][random_pos-1]) 
        # or ("'" not in new_move and chromossome['val'][random_pos-1] == new_move + "'") ):
        #     new_move = moves[randint(0, len(moves)-1)]

        while chromossome['val'][random_pos-1][0] in new_move and chromossome['val'][random_pos+1][0] in new_move:
            new_move = moves[randint(0, len(moves)-1)]

    chromossome['val'][random_pos] = new_move
    return chromossome

def mutation_exchange(chromossome):
    # moves = ["u", "u'", "f", "f'", "l", "l'", "r", "r'", "d", "d'", "b", "b'", 'u2', 'b2', 'f2', 'l2', 'r2', 'd2']
    random_pos = randint(0, len(chromossome))
    random_pos1 = random_pos

    while random_pos == random_pos1:
        random_pos1 = randint(0, len(chromossome))

    chromossome['val'][random_pos], chromossome['val'][random_pos1] = chromossome['val'][random_pos1], chromossome['val'][random_pos]
    return chromossome


def apply_genetic_operators(cube, population, elite):
    mating_pool = []

    for i in range(0, POP_SIZE, 2):
        new_offsprings = [deepcopy(population[i]), deepcopy(population[i+1])]
        if random() < CROSSOVER_PROB:
            cross_offsprings = deepcopy(new_offsprings)
            cross_offsprings = crossover_1_point(cross_offsprings[0], cross_offsprings[1])
            evaluate_solution(cube, cross_offsprings[0])
            evaluate_solution(cube, cross_offsprings[1])

            mating_candidates = [deepcopy(population[i]), deepcopy(population[i+1])] + cross_offsprings
            mating_candidates.sort(key=get_fit)

            mating_pool += mating_candidates
        
        if random() < MUTATION_PROB:
            mut_offsprings = deepcopy(new_offsprings)
            # mut_offsprings[0] = mutation_exchange(mut_offsprings[0])
            # mut_offsprings[1] = mutation_exchange(mut_offsprings[1])
            mut_offsprings[0] = mutation(mut_offsprings[0])
            mut_offsprings[1] = mutation(mut_offsprings[1])
            evaluate_solution(cube, mut_offsprings[0])
            evaluate_solution(cube, mut_offsprings[1])

            mating_candidates = [deepcopy(population[i]), deepcopy(population[i+1])] + mut_offsprings
            mating_candidates.sort(key=get_fit)

            mating_pool += mating_candidates

    if elite != None:
        mating_pool += elite

    mating_pool.sort(key=get_fit)

    offsprings = mating_pool[:POP_SIZE]

    return offsprings

def get_best_fit_index(cube, chromossome):
    cube = Cube(cube)
    best_fit = cube.max_fitness
    best_index = 0

    for i in range(len(chromossome['val'])):
        move = chromossome['val'][i]
        cube.make_move(move)
        tmp_fit = cube.calc_fitness()
        if tmp_fit < best_fit:
            best_fit = tmp_fit
            best_index = i

    return best_index


# 1 1 1 1 2 2 3 3 3 4 

def social_disaster(cube, population):
    chromossome_ver = population[0]
    n_occurences = 0
    new_population = []

    # best_fit = population[0]['fit']
    # i = 0
    # while population[i]['fit'] <= best_fit:
    #     i += 1

    # new_population.append(population[0])
    # new_population += population[i:]

    # for h in range(i):
    #     new_chromossome = generate_chromossome()
    #     evaluate_solution(cube, new_chromossome)
    #     new_population.append(new_chromossome)



    # i = 1
    # first_appearance_index = 0
    # group_count = 0

    # while i < len(population):
    #     if population[i]['fit'] == population[first_appearance_index]['fit']:
    #         group_count += 1
    #     else:
    #         if group_count > 2:
    #             new_population.append(population[first_appearance_index])
    #             for h in range(group_count):
    #                 if group_count < 8:
    #                     random_chromossome = generate_chromossome()
    #                     best_fit_index = randint(0, CHROMOSSOME_SIZE) # get_best_fit_index(cube, population[first_appearance_index+1])
    #                     new_chromossome = {
    #                         'fit': 0,
    #                         'val': population[first_appearance_index+1]['val'][:best_fit_index+1] + random_chromossome['val'][best_fit_index+1:]
    #                     }
    #                 else:
    #                     new_chromossome = generate_chromossome()
                        
    #                 evaluate_solution(cube, new_chromossome)
    #                 new_population.append(new_chromossome)
    #         else:
    #             new_population += population[first_appearance_index:i]                    
    #         first_appearance_index = i
    #         group_count = 0
        

    #     i += 1
                    
    # new_population += population[first_appearance_index:i]                    

    fit_mean = sum([chrm['fit'] for chrm in population])

    if fit_mean / len(population) == population[0]['fit']:
        new_population.append(deepcopy(population[0]))
        for i in range(len(population)-1):
            new_chromossome = generate_chromossome()
            evaluate_solution(cube, new_chromossome)
            new_population.append(new_chromossome)

    else: return population
    print("SOCIAL DISASTER")
    print([c['fit'] for c in new_population[:10]])

    new_population.sort(key=get_fit)

    return new_population[:POP_SIZE]
    

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

    


    while i < N_GENERATIONS:#population[0]['fit'] != 0:
        evaluate_pop(cube, population)
        parents = deepcopy(roullete_selection(cube, population))
        population = apply_genetic_operators(cube, parents, elite)
        population = social_disaster(cube, population)
        elite = deepcopy(population[:int(POP_SIZE * 0.1)])
        if population[0]['fit'] == 0: break
        print("GENERATION", i, "   Curr best fit:", population[0]['fit'], "    Len: ", len(population), "    N moves", cube.n_moves)
        print([c['fit'] for c in population])
        print(population[0]['val'])
        print(population[1]['val'])
        i += 1


    print(population)
    # print(population)
    print([c['fit'] for c in population])
    print("Best fit: ", population[0]['fit'])
    print(population[0]['val'])



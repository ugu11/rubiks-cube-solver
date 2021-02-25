import os
from cube import Cube
from random import randint, random, uniform, shuffle
from math import exp
from copy import deepcopy


N_GENERATIONS = 1000
POP_SIZE = 300
CROSSOVER_PROB = 0.8
MUTATION_PROB = 0.2
CHROMOSSOME_SIZE = 30

def get_fit(chromossome):
    return chromossome['fit']

def generate_chromossome():
    moves = ["u", "u'", "f", "f'", "l", "l'", "r", "r'", "d", "d'", "b", "b'", 'u2', 'b2', 'f2', 'l2', 'r2', 'd2', 'n']
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
        if not move[0] == 'n':
            cube.make_move(move)

    cube.calc_fitness()

    chromossome['fit'] = cube.fitness

def evaluate_pop(cube, population):
    for chromossome in population:
        evaluate_solution(cube, chromossome)

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

def social_disaster(cube, population):
    chromossome_ver = population[0]
    n_occurences = 0
    new_population = []

    i = 1
    first_appearance_index = 0
    group_count = 0

    while i < len(population):
        if population[i]['fit'] == population[first_appearance_index]['fit']:
            group_count += 1
        else:
            if group_count > 2:
                new_population.append(population[first_appearance_index])
                for h in range(group_count):
                    if group_count >= 3:
                        random_chromossome = generate_chromossome()
                        best_fit_index = randint(0, CHROMOSSOME_SIZE) # get_best_fit_index(cube, population[first_appearance_index+1])
                        if best_fit_index == CHROMOSSOME_SIZE:
                            new_chromossome1 = {
                                'fit': 0,
                                'val': population[first_appearance_index]['val'][:best_fit_index] + random_chromossome['val'][best_fit_index:]
                            }
                            new_chromossome2 = {
                                'fit': 0,
                                'val': random_chromossome['val'][:best_fit_index] + population[first_appearance_index]['val'][best_fit_index:]
                            }
                        else:
                            new_chromossome1 = generate_chromossome()
                            new_chromossome2 = generate_chromossome()
                    else:
                        new_chromossome1 = generate_chromossome()
                        new_chromossome2 = generate_chromossome()
                        
                    evaluate_solution(cube, new_chromossome1)
                    evaluate_solution(cube, new_chromossome2)
                    new_population.append(new_chromossome1)
                    new_population.append(new_chromossome2)
            else:
                new_population += population[first_appearance_index:i]                    
            first_appearance_index = i
            group_count = 0
        

        i += 1
                    
    new_population += population[first_appearance_index:i]                    

    print("SOCIAL DISASTER")
    print([c['fit'] for c in new_population[:10]])

    return new_population[:POP_SIZE]


def random_kill(cube, population, n_kill):
    indexes_to_kill = [randint(0, len(population)-1) for i in range(n_kill)]

    shuffle(population)

    for index in indexes_to_kill:
        new_chromossome = generate_chromossome()
        evaluate_solution(cube, new_chromossome)
        population[index] = new_chromossome

    population.sort(key=get_fit)

    return population

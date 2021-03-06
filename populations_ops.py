import os
from cube import Cube
from random import randint, random, uniform, shuffle
from math import exp
from copy import deepcopy
from chromossomes import *
from mutations import *
from collections import Counter

def generate_pop(size=None, chrom_size=None):
    population = []

    if size == None:
        size = POP_SIZE

    for i in range(size):
        chromossome = generate_chromossome(chrom_size)
        population.append(chromossome)
    return population

def social_disaster(cube, population):
    chromossome_ver = population[0]
    n_occurences = 0
    new_population = []

    i = 1
    first_appearance_index = 0
    group_count = 0

    while i < len(population):
        chr1 = deepcopy(population[i])
        chr1['val'].sort(key=is_move_none)
        if 'n' in chr1['val']:
            chr1_n_pos = chr1['val'].index('n')
            chr1['val'] = chr1['val'][:chr1_n_pos]
        chr2 = deepcopy(population[first_appearance_index])
        chr2['val'].sort(key=is_move_none)
        if 'n' in chr2['val']:
            chr2_n_pos = chr2['val'].index('n')
            chr2['val'] = chr2['val'][:chr2_n_pos]

        if chr1 == chr2:
            group_count += 1
        else:
            if group_count >= 2:
                # print("Social disaster")
                new_population.append(population[first_appearance_index])
                for h in range(group_count):
                    new_chromossome1 = mutation_by_random_generation(cube, population[first_appearance_index])
                    # new_chromossome1 = mutation_by_random_generation
                    evaluate_solution(cube, new_chromossome1)
                    new_population.append(new_chromossome1)
            else:
                new_population += population[first_appearance_index:i]                    
            first_appearance_index = i
            group_count = 0
        
        i += 1
                    
    new_population += population[first_appearance_index:i]                    

    return new_population#[:POP_SIZE]


def random_kill(cube, population, n_kill):
    indexes_to_kill = [randint(0, len(population)-1) for i in range(n_kill)]

    shuffle(population)

    for index in indexes_to_kill:
        new_chromossome = generate_chromossome()
        evaluate_solution(cube, new_chromossome)
        population[index] = new_chromossome

    population.sort(key=get_fit)

    return population

def best_overtake(cube, population):
    available_moves = Cube.available_moves
    bestest = population[:int(POP_SIZE * 0.15)]
    worstest =  population[int(POP_SIZE * 0.9):]
    new_population = []
    uni_mut = []
    mrg = []

    for chromossome in bestest:
        # uni_mut.append(uniform_mutation(cube, chromossome))
        mrg.append(mutation_by_random_generation(cube, chromossome))

    new_population += bestest + uni_mut + mrg
    
    for chromossome in population:
        number_moves = randint(1, 3)
        if len(chromossome['val']) + number_moves < 35:
            copy_chrom = deepcopy(chromossome)
            copy_chrom['val'] += ['n'] * number_moves

            new_population.append(copy_chrom)

    new_population += worstest

    evaluate_pop(cube, new_population)

    return new_population

def is_move_none(m): return m == 'n'

def repair_chromossome(chromossome):
    cube = Cube()
    chromossome_val = chromossome['val']
    i = 0
    repaired = False

    while i < len(chromossome_val)-2:
        if chromossome_val[i][0] == chromossome_val[i+1][0] and chromossome_val[i][0] != 'n' and chromossome_val[i+1][0] != 'n':
            if '2' in chromossome_val[i]:
                if '2' in chromossome_val[i+1]:
                    chromossome_val[i] = 'n'
                    chromossome_val[i+1] = 'n'
                elif "'" in chromossome_val[i+1]:
                    chromossome_val[i] = chromossome_val[i][0]
                    chromossome_val[i+1] = 'n'
                else:
                    chromossome_val[i] = chromossome_val[i][0] + "'"
                    chromossome_val[i+1] = 'n'
                repaired = True
            elif chromossome_val[i] == chromossome_val[i+1]:
                chromossome_val[i] = chromossome_val[i][0] + '2'
                chromossome_val[i+1] = 'n'
                repaired = True
            elif '2' in chromossome_val[i+1]:
                if '2' in chromossome_val[i]:
                    chromossome_val[i] = 'n'
                    chromossome_val[i+1] = 'n'
                elif "'" in chromossome_val[i]:
                    chromossome_val[i] = chromossome_val[i][0]
                    chromossome_val[i+1] = 'n'
                else:
                    chromossome_val[i] = chromossome_val[i][0] + "'"
                    chromossome_val[i+1] = 'n'
                repaired = True
            elif (("'" not in chromossome_val[i] and not "2" in chromossome_val[i] and "'" in chromossome_val[i+1])
            or ("'" in chromossome_val[i] and "'" not in chromossome_val[i+1] and not "2" in chromossome_val[i+1])):
                chromossome_val[i] = 'n'
                chromossome_val[i+1] = 'n'
                repaired = True
        elif (i <= len(chromossome_val)-2
        and chromossome_val[i][0] != 'n' and chromossome_val[i+2][0] != 'n'
        and (chromossome_val[i+1][0] == 'n' or chromossome_val[i][0] == cube.oposite_face[chromossome_val[i+1][0]]) and i+2 <= len(chromossome_val)-1):
            if '2' in chromossome_val[i]:
                if '2' in chromossome_val[i+2]:
                    chromossome_val[i] = 'n'
                    chromossome_val[i+2] = 'n'
                elif "'" in chromossome_val[i+2]:
                    chromossome_val[i] = chromossome_val[i][0]
                    chromossome_val[i+2] = 'n'
                else:
                    chromossome_val[i] = chromossome_val[i][0] + "'"
                    chromossome_val[i+2] = 'n'
                repaired = True
            elif chromossome_val[i] == chromossome_val[i+2]:
                chromossome_val[i] = chromossome_val[i][0] + '2'
                chromossome_val[i+2] = 'n'
                repaired = True
            elif chromossome_val[i][0] == chromossome_val[i+2][0] and (("'" not in chromossome_val[i] and "'" in chromossome_val[i+2])
            or ("'" in chromossome_val[i] and "'" not in chromossome_val[i+2])) and not "2" in chromossome_val[i+2]:
                chromossome_val[i] = 'n'
                chromossome_val[i+2] = 'n'
                repaired = True
            elif '2' in chromossome_val[i+2]:
                if '2' in chromossome_val[i]:
                    chromossome_val[i] = 'n'
                    chromossome_val[i+2] = 'n'
                elif "'" in chromossome_val[i]:
                    chromossome_val[i] = chromossome_val[i][0]
                    chromossome_val[i+2] = 'n'
                else:
                    chromossome_val[i] = chromossome_val[i][0] + "'"
                    chromossome_val[i+2] = 'n'
                repaired = True

        if ((chromossome_val[i][0] == 'l' and chromossome_val[i+1][0] == 'r')
        or (chromossome_val[i][0] == 'b' and chromossome_val[i+1][0] == 'f')
        or (chromossome_val[i][0] == 'd' and chromossome_val[i+1][0] == 'u')):
            chromossome_val[i], chromossome_val[i+1] = chromossome_val[i+1], chromossome_val[i]
            repaired = True

        i += 1

    # chromossome_val[i] += '-'

    # chromossome_val.sort(key=is_move_none)
    last_index = len(chromossome_val)-1
    # print(last_index, chromossome_val)


    if len(chromossome_val) == 2 and chromossome_val[0][0] == chromossome_val[1][0]:
        chromossome_val = generate_chromossome(2)['val']
        repaired = True
    elif len(chromossome_val) > 1 and chromossome_val[last_index][0] == chromossome_val[last_index-1][0] and chromossome_val[last_index][0] != 'n' and chromossome_val[last_index-1][0] != 'n':
        if '2' in chromossome_val[last_index] or (("'" in chromossome_val[last_index-1] and "'" not in chromossome_val[last_index])
        or "'" not in chromossome_val[last_index-1] and "'" in chromossome_val[last_index]):
            chromossome_val[last_index-1] = 'n'
            chromossome_val[last_index] = 'n'
        else:
            chromossome_val[last_index-1] = chromossome_val[last_index-1][0] + '2'
            chromossome_val[last_index] = 'n'
        repaired = True
    
    if ((chromossome_val[last_index-1][0] == 'l' and chromossome_val[last_index][0] == 'r')
    or (chromossome_val[last_index-1][0] == 'b' and chromossome_val[last_index][0] == 'f')
    or (chromossome_val[last_index-1][0] == 'd' and chromossome_val[last_index][0] == 'u')):
        chromossome_val[last_index-1], chromossome_val[last_index] = chromossome_val[last_index], chromossome_val[last_index-1]
        repaired = True

    while 'n' in chromossome_val:
        chromossome_val.remove('n')


    if chromossome['fit'] <= 110:
        new_chrom_val = chromossome_val + (['n'] * (CHROMOSSOME_SIZE - len(chromossome_val)))
    else:
        new_chrom_val = chromossome_val + generate_chromossome(CHROMOSSOME_SIZE - len(chromossome_val))['val']
    chromossome['val'] = new_chrom_val

    return chromossome, repaired

def fix_empty_moves(chromossome):
    cube = Cube()
    chromossome = deepcopy(chromossome)
    new_chromossomes = []
    n_count = 0
    moves = Cube.available_moves
    chromossome_val = deepcopy(chromossome['val'])

    for i in range(len(chromossome_val)-1, 0, -1):
        if chromossome_val[i] == 'n':
            n_count += 1
        else: break
    last_move = chromossome_val[len(chromossome_val) - n_count - 2]
    second_last_move = chromossome_val[len(chromossome_val) - n_count - 3]
    # new_chrom = {
    #     'fit': 0,
    #     'val': chromossome_val[:len(chromossome_val) - n_count] #[:len(chromossome_val) - n_count + i + 1]
    # }

    for i in range(n_count):
        new_move = last_move
        while (new_move[0] == last_move[0] or (new_move[0] == second_last_move[0] and last_move[0] == cube.oposite_face[new_move[0]])):
            new_move = moves[randint(0, len(moves)-1)]
        chromossome_val[len(chromossome_val) - n_count + i] = new_move
        new_chrom = {
            'fit': 0,
            'val': deepcopy(chromossome_val)[:len(chromossome_val) - n_count + i + 1]
        }
        second_last_move, last_move = last_move, new_move
        new_chromossomes.append(new_chrom)

    return new_chromossomes


def repair(population):
    new_population = []
    population = deepcopy(population)

    for i in range(len(population)):
        was_repaired = True
        while was_repaired == True:
            population[i], was_repaired = repair_chromossome(population[i])
            
        if len(population[i]['val']) > 0:
            moves_count = Counter(population[i]['val'])
            if 'n' in moves_count.keys() and moves_count['n'] == len(population[i]['val']):
                population[i] = generate_chromossome()
            else:
                new_chromossomes = fix_empty_moves(deepcopy(population[i]))
                new_population += new_chromossomes

    population += new_population

    return population

def renovate_half(cube, population):
    for i in range(2, len(population)):
        population[i] = generate_chromossome()
        evaluate_solution(cube, population[i])

    return population

def growup(cube, population):
    new_population = []

    for i in range(len(population)):
        for h in range(400):
            new_chrom_body = generate_chromossome(8)
            new_chrom = {
                'fit': 0,
                'val': population[i]['val'] + new_chrom_body['val']
            }

            new_population.append(new_chrom)
    
    evaluate_pop(cube, new_population)

    return population + new_population
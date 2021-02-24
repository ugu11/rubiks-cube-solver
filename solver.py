from cube import Cube
from sa import simulated_anealing
from ga import genetic_algorithm

def solve():
    cube = Cube()
    cube.scramble()
    # original_cube = Cube(cube)
    # cube.calc_fitness()

    # simulated_anealing(cube)

    genetic_algorithm(cube)

def main():
    solve()

main()
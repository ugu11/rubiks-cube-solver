import os
from cube import Cube
from Tree import Tree
from copy import deepcopy

def solve():
    cube = Cube()
    cube.scramble()
    original_cube = deepcopy(cube)
    # cube.calc_fitness()
    print("Initial fitness: ", cube.fitness)

    moves = ["u", "u'", "f", "f'", "l", "l'", "r", "r'", "d", "d'", "b", "b'", 'u2', 'b2', 'f2', 'l2', 'r2', 'd2']
    move_list = []
    tree = Tree(cube, None, None, cube.fitness)
    curr_node = tree
    curr_fit = 0
    curr_move = ''
    # tree_head = tree
    i = 0

    while curr_fit >= 0 and i < 100:
        print("Iter ", i, "    Curr fitness", curr_fit, "    Curr cube fit", curr_node.cube.fitness, "    Children len", len(curr_node.children), "   Curr Move", curr_node.move)
        # curr_node.print()

        curr_node.children.clear()

        # print(moves)
        curr_node.print()
        for move in moves:
            # if not move == curr_node.move: #move_list[len(move_list)-1]:
            # print(curr_node.move == None, ('2' in curr_node.move and not move == curr_node.move), ("'" in curr_node.move and not move == curr_node.move[0]), (not "'" in curr_node.move and not move == str(curr_node.move[0] + "'")))

            # if (curr_node.move == None):
            # (('2' in curr_node.move and move != curr_node.move) and 
            # ("'" in curr_node.move and move != curr_node.move[0]) and  
            # (not "'" in curr_node.move and move != str(curr_node.move[0] + "'")))): #move_list[len(move_list)-1]:
                # print("CUrr move", curr_node.move, "   move", move)
            buff_cube = deepcopy(cube)

            buff_cube.make_move(move)
            # print(buff_cube.fitness, curr_node.cube.fitness, buff_cube.fitness,curr_fit)
            print(move, buff_cube.fitness, curr_node.cube.fitness, curr_fit)
            if buff_cube.fitness <= curr_node.cube.fitness or (curr_fit > 0 and buff_cube.fitness >= curr_fit):
                # print(move, buff_cube.fitness)
                curr_node.append_node(Tree(buff_cube, move, curr_node, buff_cube.fitness))

        # print("LEN ", len(curr_node.children), [t.cube.fitness for t in curr_node.children])
        if len(curr_node.children) > 0:
            min_node = curr_node.children[0]
            for node in curr_node.children:
                if node.cube.fitness <= min_node.cube.fitness:
                    min_node = node

                # print("NODEE ", len(node.children))

            cube = deepcopy(min_node.cube)
            move_list.append(min_node.move)
            curr_node = min_node
            curr_fit = 0
        else:
            if curr_node.parent == None: break
            curr_fit = curr_node.cube.fitness
            curr_move = curr_node.move
            curr_node.parent.children.remove(curr_node)
            curr_node = curr_node.parent

        i += 1

    tree.print()
    curr_node.print()

    move_list.clear()

    while not curr_node.parent == None:
        # curr_node.print()
        move_list.insert(0, curr_node.move)
        curr_node = curr_node.parent

    print(move_list)
    cube.print()        

def main():
    solve()

main()
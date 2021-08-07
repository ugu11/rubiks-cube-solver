import os
import random
from copy import deepcopy
from math import exp

BLOCK_COST = 6
LINE_COST = 3
PAIR_BLOCK_COST = 2
LINE_BLOCK_COST = 4
PAIR_COST = 1

class Cube():
    faces = {}
    fitness = 0
    max_fitness = 9 * BLOCK_COST * 6
    n_moves = 1
    available_moves = ["u", "u'", "f", "f'", "l", "l'", "r", "r'", "d", "d'", "b", "b'"]
    # available_moves = ["u", "u'", "f", "f'", "l", "l'", "r", "r'", "d", "d'", "b", "b'", 'u2', 'b2', 'f2', 'l2', 'r2', 'd2', 'n']
    oposite_move = {
        "u": "u'",
        "u'": "u",
        "f": "f'", 
        "f'": "f", 
        "l": "l'",
        "l'": "l",
        "r": "r'",
        "r'": "r",
        "d": "d'",
        "d'": "d",
        "b": "b'",
        "b'": "b",
        'u2': 'u2',
        'f2': 'f2',
        'r2': 'r2',
        'l2': 'l2',
        'd2': 'd2',
        'b2': 'b2',
        'n': 'n'
    }
    oposite_face = {
        'u': 'd',
        'd': 'u',
        'l': 'r',
        'r': 'l',
        'f': 'b',
        'b': 'f',
        'n': 'm'
    }

    def __init__(self, cube=None):
        if cube == None:
            self.generate_cube()
            self.calc_fitness()
        else:
            self.fitness = cube.fitness
            self.faces = deepcopy(cube.faces)

    def generate_cube(self):
        faces_labels = ['u', 'f', 'r', 'b', 'l', 'd']

        for i in faces_labels:
            face = []
            for r in range(3):
                row = []
                for c in range(3):
                    row.append(i + str(r) + str(c))
                face.append(row)
            
            self.faces[i] = face

    def make_move(self, move):
        if move[0] == 'n': return
        face = self.faces[move[0]]


        # Double move
        if len(move) > 1 and move[1] == '2':
            self.make_move(move[0])
            self.make_move(move[0])
            self.n_moves -= 1

            return True
        else:
            self.n_moves += 1
            if "'" in move:
                # rotate corners
                face[0][0], face[0][2], face[2][2], face[2][0] = face[0][2], face[2][2], face[2][0], face[0][0]
                # rotate edges
                face[0][1], face[1][2], face[2][1], face[1][0] = face[1][2], face[2][1], face[1][0], face[0][1]
            else:
                # rotate corners
                face[0][0], face[0][2], face[2][2], face[2][0] = face[2][0], face[0][0], face[0][2], face[2][2]
                # rotate edges  
                face[0][1], face[1][2], face[2][1], face[1][0] = face[1][0], face[0][1], face[1][2], face[2][1]
            
            # self.faces[move[0]] = face

            if move == 'u':
                self.faces['r'][0], self.faces['f'][0], self.faces['l'][0], self.faces['b'][0] = self.faces['b'][0], self.faces['r'][0], self.faces['f'][0], self.faces['l'][0]
            elif move == "u'":
                self.faces['r'][0], self.faces['f'][0], self.faces['l'][0], self.faces['b'][0] = self.faces['f'][0], self.faces['l'][0], self.faces['b'][0], self.faces['r'][0]
            elif move == 'f':
                (self.faces['u'][2],
                [self.faces['r'][0][0], self.faces['r'][1][0], self.faces['r'][2][0]],
                self.faces['d'][0],
                [self.faces['l'][0][2], self.faces['l'][1][2], self.faces['l'][2][2]]) = (
                    [self.faces['l'][2][2], self.faces['l'][1][2], self.faces['l'][0][2]],
                    self.faces['u'][2],
                    [self.faces['r'][2][0], self.faces['r'][1][0], self.faces['r'][0][0]],
                    self.faces['d'][0]
                )
            elif move == "f'":
                (self.faces['u'][2],
                [self.faces['r'][2][0], self.faces['r'][1][0], self.faces['r'][0][0]],
                self.faces['d'][0],
                [self.faces['l'][2][2], self.faces['l'][1][2], self.faces['l'][0][2]]) = (
                    [self.faces['r'][0][0], self.faces['r'][1][0], self.faces['r'][2][0]],
                    self.faces['d'][0],
                    [self.faces['l'][0][2], self.faces['l'][1][2], self.faces['l'][2][2]],
                    self.faces['u'][2]
                )
            elif move == 'r':
                ([self.faces['u'][0][2], self.faces['u'][1][2], self.faces['u'][2][2]],
                [self.faces['b'][0][0], self.faces['b'][1][0], self.faces['b'][2][0]],
                [self.faces['d'][0][2], self.faces['d'][1][2], self.faces['d'][2][2]],
                [self.faces['f'][0][2], self.faces['f'][1][2], self.faces['f'][2][2]]) = (
                    [self.faces['f'][0][2], self.faces['f'][1][2], self.faces['f'][2][2]],
                    [self.faces['u'][2][2], self.faces['u'][1][2], self.faces['u'][0][2]],
                    [self.faces['b'][2][0], self.faces['b'][1][0], self.faces['b'][0][0]],
                    [self.faces['d'][0][2], self.faces['d'][1][2], self.faces['d'][2][2]]
                )
            elif move == "r'":
                ([self.faces['u'][2][2], self.faces['u'][1][2], self.faces['u'][0][2]],
                [self.faces['b'][0][0], self.faces['b'][1][0], self.faces['b'][2][0]],
                [self.faces['d'][0][2], self.faces['d'][1][2], self.faces['d'][2][2]],
                [self.faces['f'][0][2], self.faces['f'][1][2], self.faces['f'][2][2]]) = (
                    [self.faces['b'][0][0], self.faces['b'][1][0], self.faces['b'][2][0]],
                    [self.faces['d'][2][2], self.faces['d'][1][2], self.faces['d'][0][2]],
                    [self.faces['f'][0][2], self.faces['f'][1][2], self.faces['f'][2][2]],
                    [self.faces['u'][0][2], self.faces['u'][1][2], self.faces['u'][2][2]]
                )
            elif move == 'b':
                (self.faces['u'][0],
                [self.faces['r'][0][2], self.faces['r'][1][2], self.faces['r'][2][2]],
                [self.faces['d'][2][2], self.faces['d'][2][1], self.faces['d'][2][0]],
                [self.faces['l'][2][0], self.faces['l'][1][0], self.faces['l'][0][0]]) = (
                    [self.faces['r'][0][2], self.faces['r'][1][2], self.faces['r'][2][2]],
                    [self.faces['d'][2][2], self.faces['d'][2][1], self.faces['d'][2][0]],
                    [self.faces['l'][2][0], self.faces['l'][1][0], self.faces['l'][0][0]],
                    self.faces['u'][0]
                )
            elif move == "b'":
                (self.faces['u'][0],
                [self.faces['r'][0][2], self.faces['r'][1][2], self.faces['r'][2][2]],
                [self.faces['d'][2][2], self.faces['d'][2][1], self.faces['d'][2][0]],
                [self.faces['l'][2][0], self.faces['l'][1][0], self.faces['l'][0][0]]) = (
                    [self.faces['l'][2][0], self.faces['l'][1][0], self.faces['l'][0][0]],
                    self.faces['u'][0],
                    [self.faces['r'][0][2], self.faces['r'][1][2], self.faces['r'][2][2]],
                    [self.faces['d'][2][2], self.faces['d'][2][1], self.faces['d'][2][0]]
                )
            elif move == 'l':
                ([self.faces['u'][0][0], self.faces['u'][1][0], self.faces['u'][2][0]],
                [self.faces['f'][0][0], self.faces['f'][1][0], self.faces['f'][2][0]],
                [self.faces['d'][0][0], self.faces['d'][1][0], self.faces['d'][2][0]],
                [self.faces['b'][2][2], self.faces['b'][1][2], self.faces['b'][0][2]]) = (
                    [self.faces['b'][2][2], self.faces['b'][1][2], self.faces['b'][0][2]],
                    [self.faces['u'][0][0], self.faces['u'][1][0], self.faces['u'][2][0]],
                    [self.faces['f'][0][0], self.faces['f'][1][0], self.faces['f'][2][0]],
                    [self.faces['d'][0][0], self.faces['d'][1][0], self.faces['d'][2][0]]
                )
            elif move == "l'":
                ([self.faces['u'][0][0], self.faces['u'][1][0], self.faces['u'][2][0]],
                [self.faces['f'][0][0], self.faces['f'][1][0], self.faces['f'][2][0]],
                [self.faces['d'][0][0], self.faces['d'][1][0], self.faces['d'][2][0]],
                [self.faces['b'][2][2], self.faces['b'][1][2], self.faces['b'][0][2]]) = (
                    [self.faces['f'][0][0], self.faces['f'][1][0], self.faces['f'][2][0]],
                    [self.faces['d'][0][0], self.faces['d'][1][0], self.faces['d'][2][0]],
                    [self.faces['b'][2][2], self.faces['b'][1][2], self.faces['b'][0][2]],
                    [self.faces['u'][0][0], self.faces['u'][1][0], self.faces['u'][2][0]]
                )
            elif move == 'd':
                self.faces['r'][2], self.faces['f'][2], self.faces['l'][2], self.faces['b'][2] = self.faces['f'][2], self.faces['l'][2], self.faces['b'][2], self.faces['r'][2]
            elif move == "d'":
                self.faces['r'][2], self.faces['f'][2], self.faces['l'][2], self.faces['b'][2] = self.faces['b'][2], self.faces['r'][2], self.faces['f'][2], self.faces['l'][2]
            else:
                return False


            return True


    def scramble(self):
        moves = ["u", "u'", "f", "f'", "l", "l'", "r", "r'", "d", "d'", "b", "b'", 'u2', 'b2', 'f2', 'l2', 'r2', 'd2']
        number_moves = random.randint(20, 30)

        scramble_moves = []
        m = ["b2", "u", "d2", "f", "r2", "f2", "d2", "u2", "f'", "u2", "f2", "u2", "r2", "d2", "r", "b'", "d'", "u2", "b'", "r'", "b2"]
        for move in m:
            # print("-----------------------", move)
            self.make_move(move)
            scramble_moves.append(move)
            # self.print()

        # for i in range(number_moves):
        #     move = moves[random.randint(0, len(moves)-1)]
        #     self.make_move(move)
        #     scramble_moves.append(move)

        print("Scramble ", scramble_moves)

        
        self.n_moves = 0
        self.calc_fitness()
        self.print()
        
        return self.faces

    def print(self):
        for i in range(3):
            print('               ', self.faces['u'][i])
        print(" ")

        for i in range(3):
            print(self.faces['l'][i], self.faces['f'][i], self.faces['r'][i], self.faces['b'][i])

        print(" ")

        for i in range(3):
            print('               ', self.faces['d'][i])
        
    def calc_lines_fitness(self):
        fit = 0

        for face in self.faces:
            for i in range(0, 3):
                # Check for horizontal lines
                if self.check_is_line(self.faces[face], (i, 0), (i, 2)) and self.faces[face][1][1][0] != self.faces[face][i][0][0]:
                    fit += LINE_COST * 3
                # Check for vertival lines
                if self.check_is_line(self.faces[face], (0, i), (2, i)) and not self.faces[face][1][1][0] == self.faces[face][0][i][0]:
                    fit += LINE_COST * 3

        return fit

    def check_is_line(self, face, line_start, line_end):
        i1, j1 = line_start
        i2, j2 = line_end
        is_horizontal = abs(i1 - i2) == 0 and abs(j1 - j2) == 2
        is_vertical = abs(i1 - i2) == 2 and abs(j1 - j2) == 0
        center_piece = face[1][1][0]


        if is_horizontal:
            line = face[i1][j1:j2+1]
            left_edge_face = self.faces[self.get_face_on_left(center_piece)][i1][2]
            right_edge_face = self.faces[self.get_face_on_right(center_piece)][i1][0]

            is_line_valid = line[0][0] ==  line[1][0] and line[0][0] ==  line[2][0]

            if i1 == 0: # is top line
                if center_piece == 'f':
                    adjacent_line = self.faces['u'][2]
                elif center_piece == 'b':
                    adjacent_line = self.faces['u'][0]
                elif center_piece == 'l':
                    adjacent_line = [self.faces['u'][i][0] for i in range(3)]
                elif center_piece == 'r':
                    adjacent_line = [self.faces['u'][i][2] for i in range(3)]
                elif center_piece == 'u':
                    adjacent_line = self.faces['b'][0]
                elif center_piece == 'd':
                    adjacent_line = self.faces['f'][2]

                is_adjacent_line_valid = adjacent_line[0][0] == adjacent_line[1][0] and adjacent_line[0][0] == adjacent_line[2][0]
            elif i1 == 2: # is bottom line
                if center_piece == 'f':
                    adjacent_line = self.faces['d'][0]
                elif center_piece == 'b':
                    adjacent_line = self.faces['d'][2]
                elif center_piece == 'l':
                    adjacent_line = [self.faces['d'][i][0] for i in range(3)]
                elif center_piece == 'r':
                    adjacent_line = [self.faces['d'][i][2] for i in range(3)]
                elif center_piece == 'u':
                    adjacent_line = self.faces['f'][0]
                elif center_piece == 'd':
                    adjacent_line = self.faces['b'][2]

                is_adjacent_line_valid = adjacent_line[0][0] == adjacent_line[1][0] and adjacent_line[0][0] == adjacent_line[2][0]
            else: is_adjacent_line_valid = True

            return is_line_valid and is_adjacent_line_valid and left_edge_face[0] == self.oposite_face[right_edge_face[0]]

        elif is_vertical:
            line = [face[i][j1] for i in range(len(face))]

            is_line_valid = line[0][0] ==  line[1][0] and line[0][0] ==  line[2][0]

            if j1 == 0: # is left line
                if center_piece == 'u':
                    adjacent_line = self.faces['l'][0]
                    top_edge_face = self.faces['b'][0][2]
                    bottom_edge_face = self.faces['f'][0][0]
                elif center_piece == 'd':
                    adjacent_line = self.faces['l'][2]
                    top_edge_face = self.faces['f'][2][0]
                    bottom_edge_face = self.faces['b'][2][2]
                else: # Side faces
                    left_face = self.get_face_on_left(center_piece)
                    adjacent_line = [self.faces[left_face][i][2] for i in range(3)]

                    if center_piece == 'f':
                        top_edge_face = self.faces['u'][2][0]
                        bottom_edge_face = self.faces['d'][0][0]
                    elif center_piece == 'r':
                        top_edge_face = self.faces['u'][2][2]
                        bottom_edge_face = self.faces['d'][0][2]
                    elif center_piece == 'b':
                        top_edge_face = self.faces['u'][0][2]
                        bottom_edge_face = self.faces['d'][2][2]
                    elif center_piece == 'l':
                        top_edge_face = self.faces['u'][0][0]
                        bottom_edge_face = self.faces['d'][2][0]

                is_adjacent_line_valid = adjacent_line[0][0] == adjacent_line[1][0] and adjacent_line[0][0] == adjacent_line[2][0]
            elif j1 == 2: # is right line
                if center_piece == 'u':
                    adjacent_line = self.faces['r'][0]
                    top_edge_face = self.faces['b'][0][0]
                    bottom_edge_face = self.faces['f'][0][2]
                elif center_piece == 'd':
                    adjacent_line = self.faces['r'][2]
                    top_edge_face = self.faces['f'][2][2]
                    bottom_edge_face = self.faces['b'][2][0]
                else: # Side faces
                    right_face = self.get_face_on_right(center_piece)
                    adjacent_line = [self.faces[right_face][i][0] for i in range(3)]

                    if center_piece == 'f':
                        top_edge_face = self.faces['u'][2][2]
                        bottom_edge_face = self.faces['d'][0][2]
                    elif center_piece == 'r':
                        top_edge_face = self.faces['u'][0][2]
                        bottom_edge_face = self.faces['d'][2][2]
                    elif center_piece == 'b':
                        top_edge_face = self.faces['u'][0][0]
                        bottom_edge_face = self.faces['d'][2][0]
                    elif center_piece == 'l':
                        top_edge_face = self.faces['u'][2][0]
                        bottom_edge_face = self.faces['d'][0][0]

                is_adjacent_line_valid = adjacent_line[0][0] == adjacent_line[1][0] and adjacent_line[0][0] == adjacent_line[2][0]
            else:
                is_adjacent_line_valid = True
                if center_piece == 'u':
                    top_edge_face = self.faces['b'][0][1]
                    bottom_edge_face = self.faces['f'][0][1]
                elif center_piece == 'd':
                    top_edge_face = self.faces['f'][2][1]
                    bottom_edge_face = self.faces['b'][2][1]
                else: # Side faces
                    if center_piece == 'f':
                        top_edge_face = self.faces['u'][2][1]
                        bottom_edge_face = self.faces['d'][0][1]
                    elif center_piece == 'r':
                        top_edge_face = self.faces['u'][1][2]
                        bottom_edge_face = self.faces['d'][1][2]
                    elif center_piece == 'b':
                        top_edge_face = self.faces['u'][0][1]
                        bottom_edge_face = self.faces['d'][2][1]
                    elif center_piece == 'l':
                        top_edge_face = self.faces['u'][1][0]
                        bottom_edge_face = self.faces['d'][1][0]

            return is_line_valid and is_adjacent_line_valid and top_edge_face[0] == self.oposite_face[bottom_edge_face[0]]


        return False

    def get_face_on_left(self, face_label):
        if face_label == 'f': return 'l'
        elif face_label == 'l': return 'b'
        elif face_label == 'b': return 'r'
        elif face_label == 'r': return 'f'
        elif face_label == 'u': return 'l'
        elif face_label == 'd': return 'l'

    def get_face_on_right(self, face_label):
        if face_label == 'f': return 'r'
        elif face_label == 'r': return 'b'
        elif face_label == 'b': return 'l'
        elif face_label == 'l': return 'f'
        elif face_label == 'u': return 'r'
        elif face_label == 'd': return 'r'

    def check_is_pair(self, face, pos_piece1, pos_piece2):
        center_piece = face[1][1][0]
        i1, j1 = pos_piece1
        i2, j2 = pos_piece2
        is_pair_on_curr_face = face[i1][j1][0] == face[i2][j2][0]

        if j1 == 1 and j2 == 1 or i1 == 1 and i2 == 1:
            return is_pair_on_curr_face
        elif i1 == 0 and i2 == 0:
            if center_piece == 'f':
                is_pair_on_top_face = self.faces['u'][2][j1][0] == self.faces['u'][2][j2][0]
            elif center_piece == 'b':
                is_pair_on_top_face = self.faces['u'][0][2-j1][0] == self.faces['u'][0][2-j2][0]
            elif center_piece == 'l':
                is_pair_on_top_face = self.faces['u'][j1][0][0] == self.faces['u'][j2][0][0]
            elif center_piece == 'r':
                is_pair_on_top_face = self.faces['u'][2-j1][2][0] == self.faces['u'][2-j2][2][0]
            elif center_piece == 'u':
                is_pair_on_top_face = self.faces['b'][0][2-j1][0] == self.faces['b'][0][2-j2][0]
            elif center_piece == 'd':
                is_pair_on_top_face = self.faces['f'][2][j1][0] == self.faces['f'][2][j2][0]
                

            if is_pair_on_curr_face and is_pair_on_top_face: return True
            else: return False
        elif i1 == 2 and i2 == 2:
            if center_piece == 'f':
                is_pair_on_bottom_face = self.faces['d'][0][j1][0] == self.faces['d'][0][j2][0]
            elif center_piece == 'b':
                is_pair_on_bottom_face = self.faces['d'][2][2-j1][0] == self.faces['d'][2][2-j2]
            elif center_piece == 'l':
                is_pair_on_bottom_face = self.faces['d'][2-j1][0][0] == self.faces['d'][2-j2][0][0]
            elif center_piece == 'r':
                is_pair_on_bottom_face = self.faces['d'][j1][2][0] == self.faces['d'][j2][2][0]
            elif center_piece == 'u':
                is_pair_on_bottom_face = self.faces['f'][0][j1][0] == self.faces['f'][0][j2][0]
            elif center_piece == 'd':
                is_pair_on_bottom_face = self.faces['b'][2][2-j1][0] == self.faces['b'][2][2-j2][0]

            if is_pair_on_curr_face and is_pair_on_bottom_face: return True
            else: return False
        elif j1 == 0 and j2 == 0:
            face_on_left = self.faces[self.get_face_on_left(center_piece)]
            if center_piece == 'u':
                is_pair_on_left_face = face_on_left[0][i1][0] == face_on_left[0][i2][0]
            elif center_piece == 'd':
                is_pair_on_left_face = face_on_left[2][2-j1][0] == face_on_left[2][2-j2][0]
            else:
                is_pair_on_left_face = face_on_left[i1][2][0] == face_on_left[i2][2][0]
            
            if is_pair_on_curr_face and is_pair_on_left_face: return True
            else: return False
        elif j1 == 2 and j2 == 2:
            face_on_right = self.faces[self.get_face_on_right(center_piece)]
            if center_piece == 'u':
                is_pair_on_right_face = face_on_right[0][2-i1][0] == face_on_right[0][2-i2][0]
            elif center_piece == 'd':
                is_pair_on_right_face = face_on_right[2][j1][0] == face_on_right[2][j2][0]
            else:
                is_pair_on_right_face = face_on_right[i1][0][0] == face_on_right[i2][0][0]

            if is_pair_on_curr_face and is_pair_on_right_face: return True
            else: return False
        
        return False


    def calc_pairs_fitness(self):
        fit = 0

        for face_label in self.faces:
            face = self.faces[face_label]
            for i in range(0, 3):
                # Check for horizontal pairs
                if (self.check_is_pair(face, (i, 0), (i, 1)) or self.check_is_pair(face, (i, 1), (i, 2))) and not face[i][0][0] == face[i][2][0] and not face[1][1][0] == face[i][1][0]:
                    fit += 2 * PAIR_COST
                # Check for vertical pairs
                if (self.check_is_pair(face, (0, i), (1, i)) or self.check_is_pair(face, (1, i), (2, i))) and not face[0][i][0] == face[2][i][0] and not face[1][1][0] == face[1][i][0]:
                    fit += 2 * PAIR_COST
        return fit

    def check_is_face_solved(self, face):
        return self.check_is_line(face, (0, 0), (0, 2)) and self.check_is_line(face, (1, 0), (1, 2)) and self.check_is_line(face, (2, 0), (2, 2)) and face[0][1][0] == face[1][1][0] and face[1][1][0] == face[2][1][0]

    def get_n_correct_pieces(self, face):
        center_piece = face[1][1][0]
        n_correct_pieces = 0

        for row in face:
            for piece in row:
                if piece[0] == center_piece:
                    n_correct_pieces += 1

        return n_correct_pieces

    def calc_3x2p_blocks_fitness(self, face):
        fit = 0
        center_piece = face[1][1][0]
        # Check for horizontal middle line
        if self.check_is_line(face, (1, 0), (1, 2)):
            # Check for horizontal top line
            if self.check_is_line(face, (0, 0), (0, 2)) and face[0][0][0] == center_piece:
                fit += 6 * BLOCK_COST
                # Check for pair on bottom row
                if (self.check_is_pair(face, (2, 0), (2, 1)) or self.check_is_pair(face, (2, 1), (2, 2))) and face[2][1][0] == center_piece:
                    fit += 2 * BLOCK_COST

            # Check for horizontal bottom line
            elif self.check_is_line(face, (2, 0), (2, 2)) and face[2][0][0] == center_piece:
                fit += 6 * BLOCK_COST
                # Check for pair on top row
                if (self.check_is_pair(face, (0, 0), (0, 1)) or self.check_is_pair(face, (0, 1), (0, 2))) and face[0][1][0] == center_piece:
                    fit += 2 * BLOCK_COST

        # Check for vertical middle line
        elif self.check_is_line(face, (0, 1), (2, 1)):
            # Check for vertical left line
            if self.check_is_line(face, (0, 0), (2, 0)) and face[0][0][0] == center_piece:
                fit += 6 * BLOCK_COST
                # Check for pair on right column
                if (self.check_is_pair(face, (0, 2), (1, 2)) or self.check_is_pair(face, (1, 2), (2, 2))) and face[1][2][0] == center_piece:
                    fit += 2 * BLOCK_COST
            # Check for vertical right line
            elif self.check_is_line(face, (0, 2), (2, 2)) and face[0][2][0] == center_piece:
                fit += 6 * BLOCK_COST
                # Check for pair on left column
                if (self.check_is_pair(face, (0, 0), (1, 0)) or self.check_is_pair(face, (1, 0), (2, 0))) and face[1][0][0] == center_piece:
                    fit += 2 * BLOCK_COST
        return fit

    def calc_2x2_blocks_fitness(self, face):
        fit = 0
        center_piece = face[1][1][0]

        # Check for block on the left side of the face
        if self.check_is_pair(face, (1, 0), (1, 1)):
            if(self.check_is_pair(face, (0, 0), (0, 1)) and not face[0][2][0] == center_piece and not face[2][0][0] == center_piece or
            self.check_is_pair(face, (2, 0), (2, 1)) and not face[2][2][0] == center_piece and not face[0][0][0] == center_piece):
                fit += 2 * BLOCK_COST

        # Check for block on the right side of the face
        if self.check_is_pair(face, (1, 1), (1, 2)):
            if(self.check_is_pair(face, (0, 1), (0, 2)) and not face[0][0][0] == center_piece and not face[2][2][0] == center_piece or
            self.check_is_pair(face, (2, 1), (2, 2)) and not face[2][0][0] == center_piece and not face[0][2][0] == center_piece):
                fit += 2 * BLOCK_COST

        if not fit == 0:
            fit += 3

        return 0

    def calc_line_blocks_fitness(self, face):
        fit = 0

        if self.check_is_line(face, (1, 0), (1, 2)):
            fit += 2 * LINE_BLOCK_COST
        if self.check_is_line(face, (0, 1), (2, 1)):
            fit += 2 * LINE_BLOCK_COST
        
        if fit > 0: fit += 3

        return fit

    def calc_pairs_blocks_fitness(self, face):
        fit = 0

        if self.check_is_pair(face, (1, 1), (0, 1)):
            fit += PAIR_BLOCK_COST
        if self.check_is_pair(face, (1, 1), (2, 1)):
            fit += PAIR_BLOCK_COST
        if self.check_is_pair(face, (1, 1), (1, 0)):
            fit += PAIR_BLOCK_COST
        if self.check_is_pair(face, (1, 1), (1, 2)):
            fit += PAIR_BLOCK_COST

        fit += PAIR_BLOCK_COST

        return fit

    def calc_blocks_fitness(self):
        fit = 0

        for face_label in self.faces:
            face = self.faces[face_label]
            big_blocks_fit = 0
            small_blocks_fit = 0
            line_blocks_fit = 0
            pair_blocks_fit = 0

            # Check if face is solved
            if self.check_is_face_solved(face):
                fit += 9 * BLOCK_COST
            else:
                big_blocks_fit += self.calc_3x2p_blocks_fitness(face)
                if big_blocks_fit == 0:
                    small_blocks_fit += self.calc_2x2_blocks_fitness(face)

                    if small_blocks_fit == 0:
                        line_blocks_fit += self.calc_line_blocks_fitness(face)

                        if line_blocks_fit == 0:
                            pair_blocks_fit += self.calc_pairs_blocks_fitness(face)

            fit += big_blocks_fit + small_blocks_fit + line_blocks_fit + pair_blocks_fit

        return fit

    def calc_fitness(self):
        fit = 0

        if self.fitness >= 180 or self.fitness == 0:
            fit += self.calc_blocks_fitness()
            fit += self.calc_lines_fitness()
            fit += self.calc_pairs_fitness()
            self.max_fitness = 9 * BLOCK_COST * 6

        else:
            if self.fitness >= 35:
                self.max_fitness = (1 * 4 + 2 * 5) * 6
            else:
                self.max_fitness = 9 * 6
        
            for face_label in self.faces:
                face = self.faces[face_label]
                for row in range(3):
                    for col in range(3):
                        piece = face[row][col]
                        if piece[0] == face_label and int(piece[1]) == row and int(piece[2]) == col:
                            if '1' in piece and self.fitness >= 35:
                                fit += 2
                            else:
                                fit += 1

        # fit += self.n_moves

        # self.fitness = (self.max_fitness - fit) * (1/self.n_moves)
        self.fitness = self.max_fitness - fit
        return self.fitness
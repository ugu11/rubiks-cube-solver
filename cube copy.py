import os
import random

class Cube:
    faces = {}
    fitness = 0

    def __init__(self):
        self.generate_cube()
        self.calc_fitness()

    def generate_cube(self):
        faces_labels = ['u', 'f', 'r', 'b', 'l', 'd']

        for i in faces_labels:
            face = [[i, i, i], [i, i, i], [i, i, i]]
            self.faces[i] = face

    def make_move(self, move):
        # faces_labels = ['u', 'f', 'r', 'b', 'l', 'd']
        face = self.faces[move[0]]

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
        
        self.faces[move[0]] = face

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
            ([self.faces['u'][2][2], self.faces['u'][1][2], self.faces['u'][0][2]],
            [self.faces['b'][0][0], self.faces['b'][1][0], self.faces['b'][2][0]],
            [self.faces['d'][0][2], self.faces['d'][1][2], self.faces['d'][2][2]],
            [self.faces['f'][0][2], self.faces['f'][1][2], self.faces['f'][2][2]]) = (
                [self.faces['f'][0][2], self.faces['f'][1][2], self.faces['f'][2][2]],
                [self.faces['u'][2][2], self.faces['u'][1][2], self.faces['u'][0][2]],
                [self.faces['b'][0][0], self.faces['b'][1][0], self.faces['b'][2][0]],
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

        # Double move
        elif move[1] == '2':
            self.make_move(move[0])
            self.make_move(move[0])

        self.calc_fitness()


    def scramble(self):
        moves = ["u", "u'", "f", "f'", "l", "l'", "r", "r'", "d", "d'", "b", "b'", 'u2', 'b2', 'f2', 'l2', 'r2', 'd2']
        number_moves = random.randint(20, 30)

        # for i in range(number_moves):
        #     self.make_move(moves[random.randint(0, len(moves)-1)])

        # Test scramble 1
        # self.make_move('r')
        # self.make_move('u')
        # self.make_move('l')
        # self.make_move('d')
        # self.make_move('f')
        # self.make_move("d'")

        # Test scramble 3x2 blocks 1
        # self.make_move('r')
        # self.make_move('r')
        # self.make_move('u')
        # self.make_move('l')
        # self.make_move('u')

        # Test scramble 3x2 + pair blocks 2
        self.make_move('r2')
        self.make_move('u')
        self.make_move('l2')
        self.make_move("u'")
        

        self.print()
        
        return self.faces

    def print(self):
        for i in range(3):
            print('               ', self.faces['u'][i])

        for i in range(3):
            print(self.faces['l'][i], self.faces['f'][i], self.faces['r'][i], self.faces['b'][i])

        for i in range(3):
            print('               ', self.faces['d'][i])
        
    def calc_lines_fitness(self):
        fit = 0

        for face in self.faces:
            for i in range(0, 3):
                # Check for horizontal lines
                if self.check_is_line(self.faces[face][i]) and self.faces[face][1][1] != self.faces[face][i][0]:
                    fit += 2 * 3
                # Check for vertival lines
                if self.check_is_line([self.faces[face][0][i], self.faces[face][1][i], self.faces[face][2][i]]) and not self.faces[face][1][1] == self.faces[face][0][i]:
                    fit += 2 * 3

        return fit

    def check_is_line(self, line):
        return line[0] ==  line[1] and  line[0] ==  line[2]

    def check_is_pair(self, pair):
        return pair[1] == pair[0]

    def calc_pairs_fitness(self):
        fit = 0

        for face_label in self.faces:
            face = self.faces[face_label]
            for i in range(0, 3):
                # Check for horizontal pairs
                
                if (self.check_is_pair(face[i][0:2]) or self.check_is_pair(face[i][1:3])) and not face[i][0] == face[i][2] and not face[1][1] == face[i][1]:
                    fit += 2
                # Check for vertical pairs
                if (self.check_is_pair([face[0][i], face[1][i]]) or self.check_is_pair([face[1][i], face[2][i]])) and not face[0][i] == face[2][i] and not face[1][1] == face[1][i]:
                    fit += 2
        return fit

    def check_is_face_solved(self, face):
        return self.check_is_line(face[0]) and self.check_is_line(face[1]) and self.check_is_line(face[2])

    def get_n_correct_pieces(self, face):
        center_piece = face[1][1]
        n_correct_pieces = 0

        for row in face:
            for piece in row:
                if piece == center_piece:
                    n_correct_pieces += 1

        return n_correct_pieces

    def calc_3x2p_blocks_fitness(self, face):
        fit = 0
        center_piece = face[1][1]
        # Check for horizontal middle line
        if self.check_is_line(face[1]):
            # Check for horizontal top line
            if self.check_is_line(face[0]) and face[0][0] == center_piece:
                fit += 6 * 3
                # Check for pair on bottom row
                if (self.check_is_pair(face[2][0:2]) or self.check_is_pair(face[2][1:3])) and face[2][1] == center_piece:
                    fit += 2 * 3
            # Check for horizontal bottom line
            elif self.check_is_line(face[2]) and face[2][0] == center_piece:
                fit += 6 * 3
                # Check for pair on top row
                if (self.check_is_pair(face[0][0:2]) or self.check_is_pair(face[0][1:3])) and face[0][1] == center_piece:
                    fit += 2 * 3

        # Check for vertical middle line
        elif self.check_is_line([face[0][1], face[1][1], face[2][1]]):
            # Check for vertical left line
            if self.check_is_line([face[0][0], face[1][0], face[2][0]]) and face[0][0] == center_piece:
                fit += 6 * 3
                # Check for pair on right column
                if (self.check_is_pair([face[0][2], face[1][2]]) or self.check_is_pair([face[1][2], face[2][2]])) and face[1][2] == center_piece:
                    fit += 2 * 3
            # Check for vertical right line
            elif self.check_is_line([face[0][2], face[1][2], face[2][2]]) and face[0][2] == center_piece:
                fit += 6 * 3
                # Check for pair on left column
                if (self.check_is_pair([face[0][0], face[1][0]]) or self.check_is_pair([face[1][0], face[2][0]])) and face[1][0] == center_piece:
                    fit += 2 * 3

        return fit

    def calc_2x2_blocks_fitness(self, face):
        fit = 0
        center_piece = face[1][1]

        # Check for block on the left side of the face
        if self.check_is_pair(face[1][0:2]):
            if(self.check_is_pair(face[0][0:2]) and not face[0][2] == center_piece and not face[2][0] == center_piece or
            self.check_is_pair(face[2][0:2]) and not face[2][2] == center_piece and not face[0][0] == center_piece):
                fit += 2 * 3

        # Check for block on the right side of the face
        if self.check_is_pair(face[1][1:3]):
            if(self.check_is_pair(face[0][1:3]) and not face[0][0] == center_piece and not face[2][2] == center_piece or
            self.check_is_pair(face[2][1:3]) and not face[2][0] == center_piece and not face[0][2] == center_piece):
                fit += 2 * 3
                
        if not fit == 0:
            fit += 3

        return 0

    def calc_line_blocks_fitness(self, face):
        fit = 0

        if self.check_is_line(face[1]):
            fit += 2 * 3
        if self.check_is_line([face[0][1], face[1][1], face[2][1]]):
            fit += 2 * 3
        
        if fit > 0: fit += 3

        return fit

    def calc_blocks_fitness(self):
        fit = 0

        for face_label in self.faces:
            face = self.faces[face_label]
            big_blocks_fit = 0
            small_blocks_fit = 0
            line_blocks_fit = 0

            # Check if face is solved
            if self.check_is_face_solved(face):
                fit += 9 * 3
            else:
                big_blocks_fit += self.calc_3x2p_blocks_fitness(face)
                if not big_blocks_fit > 0:
                    small_blocks_fit += self.calc_2x2_blocks_fitness(face)

                    if not small_blocks_fit > 0:
                        line_blocks_fit += self.calc_line_blocks_fitness(face)
            fit += big_blocks_fit + small_blocks_fit + line_blocks_fit


        return fit

    def calc_fitness(self):
        max_fitness = 9 * 3 * 6
        fit = 0
        fit += self.calc_lines_fitness()
        fit += self.calc_pairs_fitness()
        fit += self.calc_blocks_fitness()

        # for face_label in self.faces:
        #     face = self.faces[face_label]
        #     center_piece = face[1][1]

        #     for row in face:
        #         for piece in row:
        #             if not piece == center_piece:
        #                 fit += 1
            


        # self.fitness = max_fitness - fit
        self.fitness = fit

        return self.fitness
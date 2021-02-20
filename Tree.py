
class Tree:
    cube = None
    move = None
    parent = None
    children = []
    fitness = 0
    def __init__(self, cube, move, parent, fitness):
        self.cube = cube
        self.move = move
        self.parent = parent
        self.children = [].copy()
        self.fitness = fitness

    def append_node(self, node_tree):
        self.children.append(node_tree)

    def print(self):
        print("Cube", self.cube, "   Move", self.move, "   Parent", self.parent, "  children", [t.cube.fitness for t in self.children])

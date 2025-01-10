class Grid:
    def __init__(self):
        self.grid = {}

    def place(self, x, y, amino_acid):
        self.grid[(x, y)] = amino_acid

    def get_neighbors(self, x, y):
        return [
            self.grid.get((x - 1, y)),
            self.grid.get((x + 1, y)),
            self.grid.get((x, y - 1)),
            self.grid.get((x, y + 1)),
        ]
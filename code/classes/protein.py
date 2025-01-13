from .aminoacid import AminoAcid

class Protein:
    def __init__(self, sequence):
        self.sequence = [AminoAcid(char) for char in sequence]
        self.grid = {}  
        self.score = 0  

    def place_on_grid(self, x, y, amino_acid):
        self.grid[(x, y)] = amino_acid

    def calculate_score(self):
        self.score = 0
        for (x1, y1), amino1 in self.grid.items():
            for (x2, y2), amino2 in self.grid.items():
                if abs(x1 - x2) + abs(y1 - y2) == 1:  
                    self.score += self.get_bond_score(amino1, amino2)

    def get_bond_score(self, amino1, amino2):
        if amino1.type == 'H' and amino2.type == 'H':
            return -1
        if amino1.type == 'C' and amino2.type == 'C':
            return -5
        if 'C' in {amino1.type, amino2.type} and 'H' in {amino1.type, amino2.type}:
            return -1
        return 0
    
    def print_structure(self):
    
        min_x = min(pos[0] for pos in self.grid.keys())
        max_x = max(pos[0] for pos in self.grid.keys())
        min_y = min(pos[1] for pos in self.grid.keys())
        max_y = max(pos[1] for pos in self.grid.keys())

        grid_width = max_x - min_x + 1
        grid_height = max_y - min_y + 1
        grid = [[' ' for _ in range(grid_width * 2 - 1)] for _ in range(grid_height * 2 - 1)]

        for (x, y), amino_acid in self.grid.items():
            grid[(y - min_y) * 2][(x - min_x) * 2] = amino_acid.type

        for (x1, y1), amino1 in self.grid.items():
            for (x2, y2), amino2 in self.grid.items():
                if abs(x1 - x2) + abs(y1 - y2) == 1:  
                    mid_x = (x1 + x2) - min_x * 2
                    mid_y = (y1 + y2) - min_y * 2
                    if x1 == x2:  
                        grid[mid_y][mid_x * 2] = '|'
                    if y1 == y2:  
                        grid[mid_y * 2][mid_x] = '-'

        for row in reversed(grid): 
            print(''.join(row))


    def __repr__(self):
        return f"Protein(sequence='{''.join([aa.type for aa in self.sequence])}', score={self.score})"

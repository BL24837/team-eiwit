class Board:
    def __init__(self):
        self.grid = {}
        self.positions = []
        self.score = 0

    def place_amino_acid(self, amino_acid):
        self.grid[amino_acid.position] = amino_acid
        self.positions.append(amino_acid.position)

    def is_occupied(self, position):
        return position in self.grid

    def update_score(self, new_amino):
        x, y = new_amino.position
        neighbors = [
            (x + 1, y),
            (x - 1, y),
            (x, y + 1),
            (x, y - 1)
        ]
        for neighbor in neighbors:
            if neighbor in self.grid and neighbor != self.positions[-2]:
                self.score += new_amino.get_bond_strength(self.grid[neighbor])

    def plot_board(self):
        x_coords, y_coords = zip(*self.positions)
        colors = {'H': 'red', 'P': 'blue', 'C': 'green'}
        plt.figure(figsize=(6, 6))
        for position, amino_acid in self.grid.items():
            plt.scatter(position[0], position[1], color=colors[amino_acid.amino_type], s=200)
            plt.text(position[0], position[1], amino_acid.amino_type, ha='center', va='center')
        plt.plot(x_coords, y_coords, color='gray')
        plt.grid(True)
        plt.title(f"Protein Folding - Score: {self.score}")
        plt.show()
import matplotlib.pyplot as plt

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
    
    def get_valid_moves(self):
        last_x, last_y = self.board.positions[-1]
        directions = [
            (1, 0),
            (-1, 0),
            (0, 1),
            (0, -1)
        ]
        return directions
    
    def plot_board(self):
        x_coords, y_coords = zip(*self.positions)
        colors = {'H': 'red', 'P': 'blue', 'C': 'green'}
        # aangepast aan de grote van de sequence, dus minimaal 2 * de sequence alle richtingen op
        plt.figure(figsize=(6, 6))
        for position, amino_acid in self.grid.items():
            plt.scatter(position[0], position[1], color=colors[amino_acid.amino_type], s=200)
            plt.text(position[0], position[1], amino_acid.amino_type, ha='center', va='center')
        plt.plot(x_coords, y_coords, color='gray')
        plt.grid(True)
        plt.title(f"Protein Folding - Score: {self.score}")
        plt.show()
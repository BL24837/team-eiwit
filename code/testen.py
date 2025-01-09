import matplotlib.pyplot as plt

class AminoAcid:
    def __init__(self, amino_type, position):
        self.amino_type = amino_type  # 'H', 'P' of 'C'
        self.position = position

    def get_bond_strength(self, other):
        if self.amino_type == 'H' and other.amino_type == 'H':
            return -1
        elif self.amino_type == 'C' and other.amino_type == 'C':
            return -5
        elif ('C' in (self.amino_type, other.amino_type)) and ('H' in (self.amino_type, other.amino_type)):
            return -1
        return 0

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
            if neighbor in self.grid:
                # Controleer of het buur-amino niet de directe voorganger of opvolger in de keten is
                if neighbor != self.positions[-2]:  # De laatste geplaatste was direct verbonden
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


class ProteinState:
    def __init__(self, sequence):
        self.sequence = sequence
        self.board = Board()
        self.best_score = float('inf')
        self.best_board = None
        self.board.place_amino_acid(AminoAcid(sequence[0], (0, 0)))

    def get_valid_moves(self):
        last_x, last_y = self.board.positions[-1]
        directions = [
            (1, 0),   # Rechts
            (-1, 0),  # Links
            (0, 1),   # Omhoog
            (0, -1)   # Omlaag
        ]
        return directions

    def backtrack(self, index):
        print(1)
        if index == len(self.sequence):
            if self.board.score < self.best_score:
                self.best_score = self.board.score
                self.best_board = Board()
                self.best_board.grid = self.board.grid.copy()
                self.best_board.positions = self.board.positions.copy()
                self.best_board.score = self.board.score
            return

        current_aa_type = self.sequence[index]

        for dx, dy in self.get_valid_moves():
            last_x, last_y = self.board.positions[-1]
            new_pos = (last_x + dx, last_y + dy)

            if not self.board.is_occupied(new_pos):
                new_aa = AminoAcid(current_aa_type, new_pos)
                self.board.place_amino_acid(new_aa)
                previous_score = self.board.score
                self.board.update_score(new_aa)

                self.backtrack(index + 1)

                self.board.grid.pop(new_pos)
                self.board.positions.pop()
                self.board.score = previous_score

    def find_best_folding(self):

        self.backtrack(1)
        self.best_board.plot_board()

# Testen van de volledige backtracking-implementatie met visualisatie
protein = ProteinState("PPPHPHHCPPC")
protein.find_best_folding()


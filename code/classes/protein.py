from aminoacid import AminoAcid




class Protein:
    def __init__(self, sequence: str):
        self.sequence = sequence
        self.best_score = 0
        self.amino_acids = {}
        self.grid = {}
        self.make_aminoacids()

    def make_aminoacids(self):
        """
        Fills the dictionary amino acids with AminoAcid objects and places them on the grid.
        Each amino acid is placed at a unique position based on its index in the sequence.
        """
        for index, char in enumerate(self.sequence):

            x, y, z = index, 0, 0 
            
            amino_acid = AminoAcid(char, index, x, y, z)
            
            self.amino_acids[index] = amino_acid
            
            self.place_on_grid(x, y, z, char)

    def get_neighbours(self, aminoacid):
        """
        """
        neighbours = []

        for other_amino_acid in self.amino_acids.values():

            if other_amino_acid == aminoacid:
                continue

            ax, ay, az = aminoacid.position
            bx, by, bz = other_amino_acid.position

            if abs(ax - bx) + abs(ay - by) + abs(az - bz) == 1:
                neighbours.append(other_amino_acid)

        return neighbours

    def calculate_score(self):
        """
        
        """
        score = 0

        for index, amino_acid in self.amino_acids.items():

            if amino_acid.type == 'H' or amino_acid.type == 'C':
                neighbours = self.get_neighbours(amino_acid)

                for neighbour in neighbours:
                    if abs(index - neighbour.index) == 1:
                        continue
                    
                    if amino_acid.type == 'H' and neighbour.type == 'H':
                        score -= 1
                    elif (amino_acid.type == 'H' and neighbour.type == 'C') or (amino_acid.type == 'C' and neighbour.type == 'H'):
                        score -= 1
                    elif amino_acid.type == 'C' and neighbour.type == 'C':
                        score -= 5

        score = score // 2

        return score

    def get_move_value(self, amino1, amino2):
        """
        Returns the value of the move made based on the change in coordinates from start to end.
        """
        sx, sy, sz = amino1.position
        ex, ey, ez = amino2.position

        if ex > sx:
            return 1  
        elif ex < sx:
            return -1 
        elif ey > sy:
            return 2
        elif ey < sy:
            return -2
        elif ez > sz:
            return 3 
        elif ez < sz:
            return -3 

    def get_valid_moves(self, amino):
        """
        Returns a list of valid moves for the given amino acid.
        A move is valid if the resulting position is not already occupied.
        """
        x, y, z = amino.position
        potential_moves = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]
        valid_moves = []

        for dx, dy, dz in potential_moves:
            new_position = (x + dx, y + dy, z + dz)
            
            if new_position not in self.grid:
                valid_moves.append(new_position)

        return valid_moves

    def place_on_grid(self, x: int, y: int, z:int, type):
        self.grid[(x, y, z)] = type
       

if __name__ == "__main__":
    protein = Protein("HHHCHC")
    amino = protein.amino_acids[3]
    valid_moves = protein.get_valid_moves(amino)
    print(f"Valid moves for amino acid {amino}: {valid_moves}")
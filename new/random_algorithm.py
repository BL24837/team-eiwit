import random
from protein import Protein

class RandomFolding:
    """
    A class to perform random folding of a protein structure.
    """
    def __init__(self, protein: Protein):
        self.protein = protein

    def execute(self, iterations: int = 100):
        """
        Executes random folding on the protein structure.

        Args:
            iterations (int): The number of random attempts for folding.

        Returns:
            Protein: The protein structure after random folding.
        """
        directions = ['x_positive', 'x_negative', 'y_positive', 'y_negative', 'z_positive', 'z_negative']

        for _ in range(iterations):
            # Select a random pivot point
            pivot_index = random.randint(0, len(self.protein.amino_acids) - 1)

            # Select a random direction
            direction = random.choice(directions)

            # Retrieve the rotation matrix
            rotation_matrices = self.protein.get_rotation_matrices()
            rotation_matrix = rotation_matrices[direction]

            # Attempt rotation if valid
            if self.protein.is_rotation_valid(pivot_index, rotation_matrix):
                for i in range(pivot_index + 1, len(self.protein.amino_acids)):
                    self.protein.rotate_amino_acid(i, pivot_index, rotation_matrix)

        return self.protein

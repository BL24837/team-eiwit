import copy
import random
from code.classes.data_storing import DataStoring
from code.classes.protein import Protein
from code.visualisation.visualize import ProteinVisualizer
from code.visualisation.distribution import Distribution

class RandomFolding:
    """
    Implements the Random Folding algorithm to explore protein configurations.

    This algorithm generates random rotations of a protein's structure and
    evaluates their stability, retaining the configuration with the best stability
    score found during the iterations.
    """

    def __init__(self, data: DataStoring, protein: Protein):
        """
        Initializes the RandomFolding class.

        Args:
            data (DataStoring): Object to store and handle result data.
            protein (Protein): The initial protein configuration to optimize.
        """
        self.data = data
        self.protein = protein

    def execute(self, iterations: int = 10000) -> Protein:
        """
        Executes the random folding algorithm to optimize the protein structure.

        Args:
            iterations (int): Number of iterations to perform random folding.

        Returns:
            Protein: The protein configuration with the best stability found.
        """
        # Initialize the best protein and its stability
        best_protein = copy.deepcopy(self.protein)
        best_stability = best_protein.calculate_stability()
        stabilities = []  # Track stability scores for visualization

        # Perform random rotations for the specified number of iterations
        for i in range(iterations):
            print(f"Iteration {i + 1}/{iterations}, Current best stability: {best_stability}")

            # Attempt a random rotation
            success = self.perform_random_rotation()

            if success:
                # Calculate the stability of the new configuration
                stability = self.protein.calculate_stability()
                self.data.random_folding(i + 1, stability)
                stabilities.append(stability)

                # Update the best protein if a better stability is found
                if stability < best_stability:
                    best_stability = stability
                    best_protein = copy.deepcopy(self.protein)

        print(f"Final best stability: {best_stability}")

        # Visualize the stability distribution over iterations
        Distribution(stabilities)

        # Store the final results
        self.data.random_folding(iterations, stability)
        
        return best_protein

    def perform_random_rotation(self) -> bool:
        """
        Performs a single random rotation on the protein structure.

        A pivot amino acid is selected randomly, and a random direction is chosen
        for the rotation. If the rotation is valid (does not cause overlaps),
        it is applied to the protein.

        Returns:
            bool: True if the rotation was successfully applied, False otherwise.
        """
        directions = ['x_positive', 'x_negative', 'y_positive', 'y_negative', 'z_positive', 'z_negative']
        pivot_index = random.randint(0, len(self.protein.amino_acids) - 1)  # Select a random pivot
        direction = random.choice(directions)  # Choose a random direction
        rotation_matrices = self.protein.get_rotation_matrices()
        rotation_matrix = rotation_matrices[direction]

        # Validate the rotation before applying it
        if self.protein.is_rotation_valid(pivot_index, rotation_matrix):
            self.protein.rotate_protein(pivot_index, rotation_matrix)
            return True
        return False
    
    def export_data(self, folded_protein:Protein):
        self.data.random_folding_data(folded_protein)


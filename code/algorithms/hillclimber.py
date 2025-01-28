from code.classes.protein import Protein
import random
import copy

class HillClimber:
    """
    Implements the Hill Climbing algorithm to optimize protein folding.

    The algorithm starts with an initial protein configuration and iteratively 
    explores small changes (rotations) to improve its stability. It only accepts 
    configurations that lead to a better (lower) stability score, ensuring 
    incremental optimization. The process terminates after a fixed number of 
    iterations or if no further improvements are found.
    """

    def __init__(self, protein: Protein, max_iterations=1000, start = None):
        """
        Initializes the HillClimber class.

        Args:
            protein (Protein): The initial protein configuration to optimize.
            max_iterations (int): The maximum number of iterations to perform.
        """
        self.protein = protein
        self.max_iterations = max_iterations
        self.start = start

    def execute(self) -> Protein:
        """
        Executes the Hill Climbing algorithm to optimize the protein folding.

        Returns:
            Protein: The best protein configuration found during the search.
        """
        # Deep copy the initial protein to avoid modifying the original
        current_protein = copy.deepcopy(self.protein)
        best_protein = copy.deepcopy(current_protein)
        current_stability = current_protein.calculate_stability()
        best_stability = current_stability

        # Iterate up to the maximum number of allowed iterations
        for iteration in range(self.max_iterations):
            print(f"HillClimber Iteration: {iteration + 1}, Current Stability: {current_stability}, Best Stability: {best_stability}")

            # Generate a list of valid pivot points for rotations
            possible_folds = list(range(len(current_protein.amino_acids) - 1))
            if not possible_folds:
                # No valid moves available, terminate early
                break

            # Select a random pivot point and rotation direction
            pivot = random.choice(possible_folds)
            rotation_matrix = random.choice(list(current_protein.get_rotation_matrices().values()))
            new_protein = copy.deepcopy(current_protein)

            # Apply the rotation if it's valid
            if new_protein.is_rotation_valid(pivot, rotation_matrix):
                for amino_index in range(pivot + 1, len(new_protein.amino_acids)):
                    new_protein.rotate_amino_acid(amino_index, pivot, rotation_matrix)

                # Calculate the stability of the new configuration
                new_stability = new_protein.calculate_stability()

                # Accept the new configuration if stability improves
                if new_stability < current_stability:
                    current_protein = copy.deepcopy(new_protein)
                    current_stability = new_stability

                    # Update the best configuration found so far
                    if current_stability < best_stability:
                        best_protein = copy.deepcopy(new_protein)
                        best_stability = current_stability

        print("HillClimber Optimization complete.")
        print(f"Best Stability: {best_stability}")
        return best_protein

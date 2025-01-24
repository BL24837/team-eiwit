from code.classes.protein import Protein
import random
import copy

class HillClimber:
    def __init__(self, protein: Protein, max_iterations=1000):
        """
        Initialize the HillClimber class.
        """
        self.protein = protein
        self.max_iterations = max_iterations

    def execute(self) -> Protein:
        """
        Apply the hill climbing algorithm to optimize the protein folding.
        Returns the best protein configuration found.
        """
        current_protein = copy.deepcopy(self.protein)
        best_protein = copy.deepcopy(current_protein)
        current_stability = current_protein.calculate_stability()
        best_stability = current_stability

        for iteration in range(self.max_iterations):
            print(f"HillClimber Iteration: {iteration + 1}, Current Stability: {current_stability}, Best Stability: {best_stability}")

            possible_folds = list(range(len(current_protein.amino_acids) - 1))
            if not possible_folds:
                break

            pivot = random.choice(possible_folds)
            rotation_matrix = random.choice(list(current_protein.get_rotation_matrices().values()))
            new_protein = copy.deepcopy(current_protein)

            if new_protein.is_rotation_valid(pivot, rotation_matrix):
                for amino_index in range(pivot + 1, len(new_protein.amino_acids)):
                    new_protein.rotate_amino_acid(amino_index, pivot, rotation_matrix)

                new_stability = new_protein.calculate_stability()

                if new_stability < current_stability:
                    # Accept the new configuration if stability improves
                    current_protein = copy.deepcopy(new_protein)
                    current_stability = new_stability

                    if current_stability < best_stability:
                        best_protein = copy.deepcopy(new_protein)
                        best_stability = current_stability

        print("HillClimber Optimization complete.")
        print(f"Best Stability: {best_stability}")
        return best_protein

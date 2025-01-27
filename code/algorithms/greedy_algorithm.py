from code.classes.protein import Protein
from code.classes.data_storing import DataStoring
import copy
import random

class GreedyFolding:
    """
    Implements a hybrid greedy folding algorithm for protein structures.

    This algorithm starts with an exploratory random folding phase to find an 
    initial configuration with a stability score of -1 or lower. Once such a 
    configuration is found, the algorithm iteratively refines the structure by 
    testing configurations with one or more additional amino acids, using a 
    combination of random and greedy folding approaches.

    The process continues until the entire sequence is folded and optimized.
    """

    def __init__(self, data: DataStoring, protein: Protein):
        """
        Initializes the GreedyFolding algorithm.

        Args:
            data (DataStoring): Object to handle data storage and export.
            protein (Protein): The protein to be folded and optimized.
        """
        self.data = data
        self.protein = protein

    def execute(self) -> Protein:
        """
        Executes the hybrid greedy folding algorithm.

        Returns:
            Protein: The optimized protein structure with improved stability.
        """
        print("Starting exploratory random folding phase...")
        # Phase 1: Find an initial configuration with stability <= -1
        best_protein = self.find_initial_negative_stability()

        print("Starting greedy refinement phase...")
        # Phase 2: Refine the structure iteratively
        refined_protein = self.iterative_random_and_greedy_folding(best_protein)

        return refined_protein

    def find_initial_negative_stability(self) -> Protein:
        """
        Finds an initial protein configuration with a stability score <= -1.

        Randomly folds the first few amino acids until a valid configuration 
        with the desired stability is found.

        Returns:
            Protein: A protein structure with a stability score <= -1.

        Raises:
            ValueError: If no configuration with stability <= -1 is found.
        """
        for n in range(4, len(self.protein.amino_acids) + 1):
            print(f"Trying random folding with the first {n} amino acids...")
            for attempt in range(100):  # Try up to 100 configurations per size
                temp_protein = copy.deepcopy(self.protein)
                self.apply_random_folding(temp_protein, n)
                stability = temp_protein.calculate_stability()

                print(f"Attempt {attempt + 1}, Stability: {stability}, Amino acids: {n}")

                if stability <= -1:
                    print(f"Found configuration with stability <= -1 using {n} amino acids.")
                    return temp_protein

        raise ValueError("Unable to find an initial configuration with stability <= -1.")

    def apply_random_folding(self, protein: Protein, limit: int):
        """
        Applies random folding to the first `limit` amino acids.

        Args:
            protein (Protein): The protein structure to modify.
            limit (int): The number of amino acids to fold randomly.
        """
        directions = list(protein.get_rotation_matrices().keys())
        for i in range(min(limit, len(protein.amino_acids))):
            pivot_index = i
            direction = random.choice(directions)
            rotation_matrix = protein.get_rotation_matrices()[direction]
            # Check if the rotation is valid before applying it
            if protein.is_rotation_valid(pivot_index, rotation_matrix):
                for j in range(i + 1, len(protein.amino_acids)):
                    protein.rotate_amino_acid(j, i, rotation_matrix)

    def iterative_random_and_greedy_folding(self, protein: Protein) -> Protein:
        """
        Refines the protein configuration using a combination of random and greedy folding.

        Args:
            protein (Protein): The initial protein configuration.

        Returns:
            Protein: The refined protein structure.
        """
        current_protein = copy.deepcopy(protein)
        best_score = current_protein.calculate_stability()

        # Incrementally refine the structure
        for n in range(5, len(self.protein.amino_acids) + 1):
            print(f"Refining with {n} amino acids...")

            # Attempt to improve stability with greedy folding
            improved = self.test_greedy_folding_with_one_amino_acid(current_protein, n, best_score)
            if improved:
                best_score = current_protein.calculate_stability()
                print(f"Improved to stability {best_score} with {n} amino acids.")
                continue

            # If no improvement, try random folding
            print("Trying random folding for the next two amino acids...")
            improved = self.test_random_folding_with_two_amino_acids(current_protein, n, best_score)
            if improved:
                best_score = current_protein.calculate_stability()
                print(f"Improved to stability {best_score} after random folding.")

        return current_protein

    def test_greedy_folding_with_one_amino_acid(self, protein: Protein, n: int, current_best_score: int) -> bool:
        """
        Tests adding one amino acid using greedy folding.

        Args:
            protein (Protein): The current protein configuration.
            n (int): Number of amino acids to fold.
            current_best_score (int): The current best stability score.

        Returns:
            bool: True if an improvement was found, False otherwise.
        """
        directions = list(protein.get_rotation_matrices().keys())
        if n - 1 >= len(protein.amino_acids):
            print(f"Skipping: pivot index {n - 1} out of range.")
            return False

        for direction in directions:
            temp_protein = copy.deepcopy(protein)

            pivot_index = n - 1
            rotation_matrix = temp_protein.get_rotation_matrices()[direction]
            if temp_protein.is_rotation_valid(pivot_index, rotation_matrix):
                for j in range(pivot_index + 1, len(temp_protein.amino_acids)):
                    temp_protein.rotate_amino_acid(j, pivot_index, rotation_matrix)

                stability = temp_protein.calculate_stability()
                print(f"Testing one amino acid, Direction: {direction}, Stability: {stability}")

                if stability < current_best_score:
                    protein.amino_acids = temp_protein.amino_acids
                    return True

        return False

    def test_random_folding_with_two_amino_acids(self, protein: Protein, n: int, current_best_score: int) -> bool:
        """
        Tests adding two amino acids using random folding.

        Args:
            protein (Protein): The current protein configuration.
            n (int): Number of amino acids to fold.
            current_best_score (int): The current best stability score.

        Returns:
            bool: True if an improvement was found, False otherwise.
        """
        directions = list(protein.get_rotation_matrices().keys())
        if n >= len(protein.amino_acids):
            print(f"Skipping: pivot index {n} out of range.")
            return False

        for attempt in range(100):  # Test up to 100 configurations
            temp_protein = copy.deepcopy(protein)

            for i in range(max(0, n - 2), min(n + 2, len(temp_protein.amino_acids))):
                pivot_index = i
                direction = random.choice(directions)
                rotation_matrix = temp_protein.get_rotation_matrices()[direction]

                if temp_protein.is_rotation_valid(pivot_index, rotation_matrix):
                    for j in range(pivot_index + 1, len(temp_protein.amino_acids)):
                        temp_protein.rotate_amino_acid(j, pivot_index, rotation_matrix)

            stability = temp_protein.calculate_stability()
            print(f"Random folding attempt {attempt + 1}, Stability: {stability}")

            if stability < current_best_score:
                protein.amino_acids = temp_protein.amino_acids
                return True

        return False

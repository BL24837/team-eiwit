from code.classes.protein import Protein
import copy
import random

class GreedyFolding:
    """
    Combines exploratory random folding with iterative greedy refinement.
    
    The algorithm is an adapted greedy approach that starts with a random
    folding phase to find an initial configuration. Since at least four amino acids
    are required to form a potential bond and achieve a minimum stability score of -1, 
    the algorithm begins by applying random folding to the first four amino acids.
    Once a configuration with a stability score of -1 or lower is found,
    it becomes the starting structure.

    From this starting point, the algorithm proceeds iteratively.
    It first applies random folding to one additional amino acid.
    If this does not improve the stability,
    it tries random folding with two additional amino acids.
    This process continues, incrementing the number of amino acids involved
    in random folding, until a configuration with a better stability score is found.

    When a new configuration with improved stability is identified,
    the algorithm resets and repeats the process,
    starting from the last point of improvement.
    It applies random folding to one additional amino acid,
    then two, and so on, continuing until the entire sequence
    has been processed and optimized.
    """
    def __init__(self, protein: Protein):
        self.protein = protein

    def execute(self) -> Protein:
        """
        Executes the hybrid folding algorithm.

        Returns:
            Protein: The folded protein structure.
        """
        # Phase 1: Find the minimal starting point with -1 stability
        print("Starting exploratory random folding phase...")
        best_protein = self.find_initial_negative_stability()

        # Phase 2: Iterative greedy folding
        print("Starting greedy refinement phase...")
        refined_protein = self.iterative_random_and_greedy_folding(best_protein)

        return refined_protein

    def find_initial_negative_stability(self) -> Protein:
        """
        Perform random folding to find the minimal configuration with a stability of -1.

        Returns:
            Protein: The protein structure with -1 stability and minimal amino acids.
        """
        for n in range(4, len(self.protein.amino_acids) + 1):
            print(f"Trying random folding with the first {n} amino acids...")
            for attempt in range(100):  # Try up to 100 random configurations per size
                temp_protein = copy.deepcopy(self.protein)
                self.apply_random_folding(temp_protein, n)
                stability = temp_protein.calculate_stability()

                print(f"Attempt {attempt + 1}, Stability: {stability}, Amino acids: {n}")

                if stability <= -1:
                    print(f"Found configuration with stability -1 using {n} amino acids.")
                    return temp_protein

        raise ValueError("Unable to find an initial configuration with stability -1.")

    def apply_random_folding(self, protein: Protein, limit: int):
        """
        Apply random folding to the first `limit` amino acids.
        """
        directions = list(protein.get_rotation_matrices().keys())
        for i in range(min(limit, len(protein.amino_acids))):
            pivot_index = i
            direction = random.choice(directions)
            rotation_matrix = protein.get_rotation_matrices()[direction]
            if protein.is_rotation_valid(pivot_index, rotation_matrix):
                for j in range(i + 1, len(protein.amino_acids)):
                    protein.rotate_amino_acid(j, i, rotation_matrix)

    def iterative_random_and_greedy_folding(self, protein: Protein) -> Protein:
        """
        Perform iterative refinement using both random folding and greedy folding.

        Returns:
            Protein: The refined protein structure.
        """
        current_protein = copy.deepcopy(protein)
        best_score = current_protein.calculate_stability()

        for n in range(5, len(self.protein.amino_acids) + 1):
            print(f"Refining with {n} amino acids...")

            # Test adding one amino acid with greedy refinement
            improved = self.test_greedy_folding_with_one_amino_acid(current_protein, n, best_score)
            if improved:
                best_score = current_protein.calculate_stability()
                print(f"Improved to stability {best_score} with {n} amino acids.")
                continue

            # If no improvement, apply random folding to the next two amino acids
            print("Trying random folding for the next two amino acids...")
            improved = self.test_random_folding_with_two_amino_acids(current_protein, n, best_score)
            if improved:
                best_score = current_protein.calculate_stability()
                print(f"Improved to stability {best_score} after random folding.")

        return current_protein

    def test_greedy_folding_with_one_amino_acid(self, protein: Protein, n: int, current_best_score: int) -> bool:
        """
        Test folding by adding one amino acid and applying greedy refinement.

        Args:
            protein (Protein): The current protein structure.
            n (int): The number of amino acids to test.
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

            # Apply folding for the new amino acid
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
        Test random folding by adding two amino acids and exploring all possibilities.

        Args:
            protein (Protein): The current protein structure.
            n (int): The number of amino acids to test.
            current_best_score (int): The current best stability score.

        Returns:
            bool: True if an improvement was found, False otherwise.
        """
        directions = list(protein.get_rotation_matrices().keys())
        if n >= len(protein.amino_acids):
            print(f"Skipping: pivot index {n} out of range.")
            return False

        for attempt in range(100):  # Try up to 100 random configurations
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

if __name__ == "__main__":
    # Example usage
    sequence = "PPPHHPPHHPPPPPHHHHHHHPPHHPPPPHHPPHPP"  # Define the protein sequence
    protein = Protein(sequence)

    hybrid_folding = HybridFolding(protein)
    folded_protein = hybrid_folding.execute()

    print("Final structure after Hybrid Folding:")
    for aa in folded_protein.amino_acids:
        print(f"Type: {aa['type']}, Position: {aa['position']}")

    print(f"Final stability score: {folded_protein.calculate_stability()}")

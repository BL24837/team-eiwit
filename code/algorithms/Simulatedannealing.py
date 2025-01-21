from code.classes.protein import Protein
from code.algorithms.random_algorithm import RandomFolding
import numpy as np
import random
import copy
import math

class SimulatedAnnealing:
    def __init__(self, protein: Protein, initial_temp=100.0, cooling_rate=0.998, min_temp=1.0, max_attempts_per_temp=100, random_folding_iterations=1000):
        """
        Initialize the Simulated Annealing class with parameters.
        """
        self.protein = protein
        self.initial_temp = initial_temp
        self.cooling_rate = cooling_rate
        self.min_temp = min_temp
        self.max_attempts_per_temp = max_attempts_per_temp
        self.random_folding_iterations = random_folding_iterations
        self.current_protein = None  # Store the initial folded protein

    def initialize_random_protein(self) -> Protein:
        """
        Use the RandomFolding algorithm to generate a random initial protein configuration.
        """
        random_folding = RandomFolding(self.protein)
        return random_folding.execute(iterations=self.random_folding_iterations)

    def run(self) -> Protein:
        """
        Apply simulated annealing to optimize the protein folding.
        Each mutation that improves the stability score is accepted for the next iteration.
        """
        # Only generate a random initial configuration if it hasn't been done yet
        if self.current_protein is None:
            self.current_protein = self.initialize_random_protein()

        current_protein = self.current_protein.copy()
        best_protein = current_protein.copy()
        current_stability = current_protein.calculate_stability()
        best_stability = current_stability

        # Initialize the temperature
        current_temp = self.initial_temp
        iteration_count = 0

        while current_temp > self.min_temp:
            # Try random mutations per temperature
            for attempt in range(self.max_attempts_per_temp):
                print(f"Iteration: {iteration_count}, Temperature: {current_temp:.2f}, Attempt: {attempt+1}, Current Stability: {current_stability}, Best Stability: {best_stability}")

                possible_folds = list(range(len(current_protein.amino_acids) - 1))

                if not possible_folds:
                    break

                # Select a random pivot point and rotation
                pivot = random.choice(possible_folds)
                rotation_matrix = random.choice(list(current_protein.get_rotation_matrices().values()))

                # Attempt to apply the random mutation
                new_protein = current_protein.copy()

                if new_protein.is_rotation_valid(pivot, rotation_matrix):
                    for amino_index in range(pivot + 1, len(new_protein.amino_acids)):
                        new_protein.rotate_amino_acid(amino_index, pivot, rotation_matrix)
                    
                    # Calculate the stability of the new configuration
                    new_stability = new_protein.calculate_stability()

                    # Calculate the change in stability
                    delta_e = new_stability - current_stability

                    # Calculate the acceptance probability
                    probability = math.exp(-delta_e / current_temp) if delta_e > 0 else 1

                    # Accept or reject the new configuration
                    if delta_e < 0 or random.uniform(0, 1) < probability:
                        # New configuration is accepted
                        current_protein = new_protein
                        current_stability = new_stability

                        # Update the best solution
                        if current_stability < best_stability:
                            best_protein = new_protein.copy()
                            best_stability = current_stability

            # Lower the current temperature
            current_temp *= self.cooling_rate
            iteration_count += 1

        print("Optimization complete.")
        print(f"Best Stability: {best_stability}")
        return best_protein

# Example usage (only runs when this file is executed directly)
if __name__ == "__main__":
    sequence = "HCHHCHCHHHPHPHHHCHPHPPHHPHCHPHHHPCHP"
    protein = Protein(sequence)

    # Run Simulated Annealing
    sa = SimulatedAnnealing(protein)
    sa.current_protein = sa.initialize_random_protein()  # Perform random folding once
    best_protein = sa.run()

    print("Optimized Stability:", best_protein.calculate_stability())
    print("Best folded configuration:")
    for amino_acid in best_protein.amino_acids:
        print(f"Type: {amino_acid['type']}, Position: {amino_acid['position']}")

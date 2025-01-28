from code.classes.protein import Protein
from code.classes.data_storing import DataStoring
from code.algorithms.hillclimber import HillClimber
import random
import copy
import math
import matplotlib.pyplot as plt

class SimulatedAnnealing:
    """
    Implements the Simulated Annealing algorithm for protein folding optimization.

    This algorithm combines global search (via probabilistic exploration) with 
    local refinement (using the HillClimber algorithm). By starting at a high 
    "temperature" and gradually cooling, it balances exploration and exploitation, 
    enabling escape from local minima and convergence to an optimized solution.
    """

    def __init__(self, data: DataStoring, protein: Protein, max_attempts_per_temp: int = 100, hillclimber_iterations: int = 100) -> None:
        """
        Initializes the Simulated Annealing algorithm.

        Args:
            data (DataStoring): Object to store and manage result data.
            protein (Protein): The protein to optimize.
            max_attempts_per_temp (int): Number of attempts per temperature level.
            hillclimber_iterations (int): Number of iterations for the HillClimber algorithm.
        """
        self.data = data
        self.protein = protein
        self.max_attempts_per_temp = max_attempts_per_temp
        self.hillclimber_iterations = hillclimber_iterations
        self.current_protein = None  # Store the initial folded protein
        self.best_protein = None  # Track the best protein configuration found

        # Configure cooling parameters based on protein length
        protein_length = len(protein.sequence)
        if protein_length < 25:
            self.cooling_rate = 0.999
            self.initial_temp = 3.0
            self.min_temp = 1.0
        elif 25 <= protein_length < 35:
            self.cooling_rate = 0.997
            self.initial_temp = 3.0
            self.min_temp = 1.0
        elif 35 <= protein_length <= 50:
            self.cooling_rate = 0.995
            self.initial_temp = 2.0
            self.min_temp = 0.6
        else:
            self.cooling_rate = 0.990
            self.initial_temp = 3.0
            self.min_temp = 1.0

    def initialize_with_hillclimber(self) -> Protein:
        """
        Uses the HillClimber algorithm to generate an optimized initial protein configuration.

        Returns:
            Protein: The locally optimized protein structure.
        """
        hill_climber = HillClimber(protein=self.protein, max_iterations=self.hillclimber_iterations)
        return hill_climber.execute()
    
    def plot_temperature_vs_iterations(self, temperatures: list[float], iterations: list[int]) -> None:
        """
        Plots the temperature over the course of iterations.

        Args:
            temperatures (list[float]): List of temperatures recorded at each step.
            iterations (list[int]): Corresponding iteration numbers.
        """
        plt.figure(figsize=(10, 6))
        plt.plot(iterations, temperatures, label="Temperature")
        plt.xlabel("Iterations")
        plt.ylabel("Temperature")
        plt.title("Temperature vs Iterations")
        plt.legend()
        plt.grid(True)
        plt.show()

    def execute(self) -> Protein:
        """
        Executes the Simulated Annealing algorithm.

        Returns:
            Protein: The best protein configuration found during optimization.
        """
        # Initialize with HillClimber if not already done
        if self.current_protein is None:
            self.current_protein = self.initialize_with_hillclimber()

        current_protein = copy.deepcopy(self.current_protein)
        self.best_protein = copy.deepcopy(current_protein)
        current_stability = current_protein.calculate_stability()
        best_stability = current_stability

        current_temp = self.initial_temp
        iteration_count = 0

        iteration_data = []# Track iteration counts for plotting

        while current_temp > self.min_temp:
            for attempt in range(self.max_attempts_per_temp):
                print(f"Iteration: {iteration_count}, Temperature: {current_temp:.6f}, Attempt: {attempt + 1}, Current Stability: {current_stability}, Best Stability: {best_stability}")

                # Generate a list of valid pivot points
                possible_folds = list(range(len(current_protein.amino_acids) - 1))
                if not possible_folds:
                    break

                # Randomly select a pivot point and rotation
                pivot = random.choice(possible_folds)
                rotation_matrix = random.choice(list(current_protein.get_rotation_matrices().values()))
                new_protein = copy.deepcopy(current_protein)

                # Apply rotation if valid
                if new_protein.is_rotation_valid(pivot, rotation_matrix):
                    for amino_index in range(pivot + 1, len(new_protein.amino_acids)):
                        new_protein.rotate_amino_acid(amino_index, pivot, rotation_matrix)

                    # Calculate the stability difference
                    new_stability = new_protein.calculate_stability()
                    delta_e = new_stability - current_stability

                    # Determine acceptance based on stability and temperature
                    if delta_e < 0:
                        accept = True  # Always accept improvements
                    else:
                        probability = math.exp(-delta_e / current_temp)
                        accept = random.uniform(0, 1) < probability

                    if accept:
                        current_protein = copy.deepcopy(new_protein)
                        current_stability = new_stability

                        # Periodically refine using HillClimber
                        if iteration_count % 10 == 0:
                            hill_climber = HillClimber(protein=current_protein, max_iterations=10)
                            current_protein = hill_climber.execute()
                            current_stability = current_protein.calculate_stability()

                        # Update the best configuration found
                        if current_stability < best_stability:
                            self.best_protein = copy.deepcopy(current_protein)
                            best_stability = current_stability
            iteration = iteration_count
            temp = current_temp
            stability= current_stability

            # Update temperature and iteration tracking
            iteration_data.append((iteration, temp, stability))

            # Reduce temperature based on the cooling rate
            current_temp *= self.cooling_rate
            iteration_count += 1

        self.export_results(iteration_data)

        # Return the best configuration found
        return self.best_protein
    
    def export_results(self, iteration_data: list[tuple[int, float, float]]) -> None:
        """
        Exports the results to a file in the appropriate format.

        Args:
            data (list[str]): List of data points to export.
        """
        self.data.simulatedannealing_data(iteration_data)

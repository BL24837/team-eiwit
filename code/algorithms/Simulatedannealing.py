from code.classes.protein import Protein
from code.classes.data_storing import DataStoring
from code.algorithms.random_algorithm import RandomFolding
from code.experiment.si_graph import SiGraph
import numpy as np
import random, copy, math
import matplotlib.pyplot as plt

class SimulatedAnnealing:
    def __init__(self, data: DataStoring, protein: Protein, initial_temp=5.0, cooling_rate=0.9995, min_temp=0.1, max_attempts_per_temp=100, random_folding_iterations=1000):
        """
        Initialize the Simulated Annealing class with parameters.
        """
        self.data = data
        self.protein = protein
        self.initial_temp = initial_temp
        self.cooling_rate = cooling_rate
        self.min_temp = min_temp
        self.max_attempts_per_temp = max_attempts_per_temp
        self.random_folding_iterations = random_folding_iterations
        self.current_protein = None  # Store the initial folded protein
        self.best_protein = None  # Track the best protein configuration found

    def initialize_random_protein(self) -> Protein:
        """
        Use the RandomFolding algorithm to generate a random initial protein configuration.
        """
        random_folding = RandomFolding(data=self.data, protein=self.protein)
        return random_folding.execute(iterations=self.random_folding_iterations)
    
    def plot_temperature_vs_iterations(self, temperatures, iterations):
        """
        Plot the temperature against the number of iterations.
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
        Apply simulated annealing to optimize the protein folding.
        Always returns the best found protein configuration.
        """
        if self.current_protein is None:
            self.current_protein = self.initialize_random_protein()

        current_protein = copy.deepcopy(self.current_protein)
        self.best_protein = copy.deepcopy(current_protein)
        current_stability = current_protein.calculate_stability()
        best_stability = current_stability

        current_temp = self.initial_temp
        iteration_count = 0
        si_graph = []

        temperatures = []
        iterations = []

        si_graph.append(f"{best_stability},{iteration_count}")

        while current_temp > self.min_temp:
            for attempt in range(self.max_attempts_per_temp):
                print(f"Iteration: {iteration_count}, Temperature: {current_temp:.6f}, Attempt: {attempt+1}, Current Stability: {current_stability}, Best Stability: {best_stability}")

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
                    delta_e = new_stability - current_stability

                    if delta_e < 0:
                        # Always accept improvements
                        accept = True
                    else:
                        # Accept worse solutions with a probability
                        probability = math.exp(-delta_e / current_temp)
                        accept = random.uniform(0, 1) < probability

                    if accept:
                        current_protein = copy.deepcopy(new_protein)
                        current_stability = new_stability

                        if current_stability < best_stability:
                            self.best_protein = copy.deepcopy(new_protein)
                            best_stability = current_stability
                            si_graph.append(f"{best_stability},{iteration_count}")

            temperatures.append(current_temp)
            iterations.append(iteration_count)

            # exponential cooling influenced by cooling_rate
            current_temp *= self.cooling_rate
            iteration_count += 1

        si_graph.append(f"{best_stability},{iteration_count}")

        si_graph = SiGraph(
            si_graph,  # Contains the stability and iteration data
            protein_params={  # Pass the configuration parameters used for this run
                'protein_sequence': self.protein.sequence,
                'initial_temp': self.initial_temp,
                'cooling_rate': self.cooling_rate,
                'min_temp': self.min_temp,
                'max_attempts_per_temp': self.max_attempts_per_temp,
                'random_folding_iterations': self.random_folding_iterations
            }
        )

        self.plot_temperature_vs_iterations(temperatures, iterations)

        print("Optimization complete.")
        print(f"Best Stability: {best_stability}")
        return self.best_protein

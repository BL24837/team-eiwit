from code.classes.protein import Protein
from code.classes.data_storing import DataStoring
from code.algorithms.hillclimber import HillClimber  # Importeer HillClimber
from code.experiment.si_graph import SiGraph
import random, copy, math
import matplotlib.pyplot as plt

class SimulatedAnnealing:
    def __init__(self, data: DataStoring, protein: Protein, max_attempts_per_temp=100, hillclimber_iterations=1000):
        """
        Initialize the Simulated Annealing class with parameters.
        Uses the HillClimber algorithm as part of the optimization process.
        """
        self.data = data
        self.protein = protein
        self.max_attempts_per_temp = max_attempts_per_temp
        self.hillclimber_iterations = hillclimber_iterations
        self.current_protein = None  # Store the initial folded protein
        self.best_protein = None  # Track the best protein configuration found

        # Adjust cooling rate and initial temperature based on protein length
        protein_length = len(protein.sequence)
        if protein_length < 25:
            self.cooling_rate = 0.999
            self.initial_temp = 3.0
            self.min_temp = 1
        elif 25 <= protein_length < 35:
            self.cooling_rate = 0.997
            self.initial_temp = 3.0
            self.min_temp = 1
        elif 35 <= protein_length <= 50:
            self.cooling_rate = 0.95
            self.initial_temp = 2
            self.min_temp = 0.6
        else:
            self.cooling_rate = 0.990
            self.initial_temp = 3.0
            self.min_temp = 1

    def initialize_with_hillclimber(self) -> Protein:
        """
        Use the HillClimber algorithm to generate an optimized initial protein configuration.
        """
        hill_climber = HillClimber(protein=self.protein, max_iterations=self.hillclimber_iterations)
        return hill_climber.execute()
    
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
        Uses HillClimber for intermediate local optimization.
        Always returns the best found protein configuration.
        """
        # Use HillClimber for the initial configuration
        if self.current_protein is None:
            self.current_protein = self.initialize_with_hillclimber()

        current_protein = copy.deepcopy(self.current_protein)
        self.best_protein = copy.deepcopy(current_protein)
        current_stability = current_protein.calculate_stability()
        best_stability = current_stability

        current_temp = self.initial_temp
        iteration_count = 0
        si_graph = []

        temperatures = []
        iterations = []

        best_stabillity_hundred = []
        data = []

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

                        # Apply HillClimber locally every few iterations
                        if iteration_count % 10 == 0:
                            hill_climber = HillClimber(protein=current_protein, max_iterations=10)
                            current_protein = hill_climber.execute()
                            current_stability = current_protein.calculate_stability()

                        if current_stability < best_stability:
                            self.best_protein = copy.deepcopy(current_protein)
                            best_stability = current_stability
                            si_graph.append(f"{best_stability},{iteration_count}")
                
                best_stabillity_hundred.append(current_stability)

                if (attempt + 1) % 100 == 0:
                    best_stabillity_hundred.append(current_stability)
                    data.append(f"{iteration_count}, {min(best_stabillity_hundred)}, {current_temp}")
                    best_stabillity_hundred = []

            temperatures.append(current_temp)
            iterations.append(iteration_count)

            current_temp *= self.cooling_rate
            iteration_count += 1

        self.export_results(data)

        return self.best_protein
    
    def export_results(self, data):
        """
        Exporteer de resultaten in het juiste format naar een bestand.
        """
        self.data.simulatedannealing(data)


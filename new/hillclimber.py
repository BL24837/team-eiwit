from random_algorithm import RandomFolding
from protein import Protein
import matplotlib.pyplot as plt
from visualize import ProteinVisualizer
from random_algorithm import RandomFolding

import copy
import random

class HillClimb:
    def __init__(self, protein: Protein):
        self.protein = protein 
        self.best_folding = None 

    def execute(self, iteration: int):
        best_protein = copy.deepcopy(self.protein)  # Maak een kopie om de beste vouwing te bewaren
        best_stability = best_protein.calculate_stability()

        directions = ['x_positive', 'x_negative', 'y_positive', 'y_negative', 'z_positive', 'z_negative']

        stabilities = [] 

        for _ in range(iteration):
            random_folding = self.random_fold()

            length_random_folding = len(random_folding.sequence)

            # Walks from the back of the brotein to the starting point
            for i in range(length_random_folding - 1, 0, -1):
                pivot_index = i
                for direction in directions:
                    rotation_matrices = random_folding.get_rotation_matrices()
                    rotation_matrix = rotation_matrices[direction]

                    if random_folding.is_rotation_valid(pivot_index, rotation_matrix):
                        temp_folding = random_folding

                        for j in range(pivot_index + 1, len(random_folding.amino_acids)):
                            temp_folding.rotate_amino_acid(j, pivot_index, rotation_matrix)
                        
                        if temp_folding.calculate_stability() < best_stability:
                            best_stability = temp_folding.calculate_stability()
                            best_protein = copy.deepcopy(temp_folding)

            if random_folding.calculate_stability() < best_stability:
                best_stability = random_folding.calculate_stability()
                best_protein = copy.deepcopy(random_folding)

            stabilities.append(best_stability)

            print(f"op dit moment best stability: {best_stability}")
        
        visualizer = ProteinVisualizer(best_protein)

        self.protein = best_protein

        plot_stability_distribution(stabilities)

        visualizer.display()



    def random_fold(self):
        random_object = RandomFolding(self.protein)

        random_folding = random_object.execute(iterations=10)

        return random_folding
    
def plot_stability_distribution(stabilities):
    """
    Plot de distributie van stabiliteit over de verschillende iteraties.
    
    Args:
        stabilities (list): Lijst van stabiliteitswaarden per iteratie.
    """
    plt.hist(stabilities, bins=30, edgecolor='black')
    plt.title('Distributie van stabiliteit bij random folding')
    plt.xlabel('Stabiliteit')
    plt.ylabel('Frequentie')
    plt.show()
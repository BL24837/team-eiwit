import copy
import random
import matplotlib.pyplot as plt
from code.visualisation.visualize import ProteinVisualizer

class RandomFolding:
    def __init__(self, protein):
        self.protein = protein

    def execute(self, iterations):
        """
        Executes random folding on the protein structure while keeping track 
        of the best folding based on stability.
        
        Args:
            iterations (int): The number of random attempts for folding.
        
        Returns:
            Protein: The protein structure with the best stability found.
        """
        best_protein = copy.deepcopy(self.protein)  # Maak een kopie om de beste vouwing te bewaren
        best_stability = best_protein.calculate_stability()

        directions = ['x_positive', 'x_negative', 'y_positive', 'y_negative', 'z_positive', 'z_negative']

        stabilities = [] 

        for _ in range(iterations):
            print(f"Current best stability: {best_stability}")
            pivot_index = random.randint(0, len(self.protein.amino_acids) - 1)
            direction = random.choice(directions)
            rotation_matrices = self.protein.get_rotation_matrices()
            rotation_matrix = rotation_matrices[direction]

            if self.protein.is_rotation_valid(pivot_index, rotation_matrix):
                for i in range(pivot_index + 1, len(self.protein.amino_acids)):
                    self.protein.rotate_amino_acid(i, pivot_index, rotation_matrix)
                
                stability = self.protein.calculate_stability()
                stabilities.append(stability)

                if stability < best_stability:  
                    best_stability = stability
                    best_protein = copy.deepcopy(self.protein) 
    
        print(f"Final best stability: {best_stability}")

        visualizer = ProteinVisualizer(best_protein)

        plot_stability_distribution(stabilities)

        visualizer.display()

        return best_protein
    
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
from visualize import ProteinVisualizer
import copy
import random
import matplotlib.pyplot as plt

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
        best_protein = copy.deepcopy(self.protein)  # Copy to store the best folding
        best_stability = best_protein.calculate_stability()

        directions = ['x_positive', 'x_negative', 'y_positive', 'y_negative', 'z_positive', 'z_negative']

        stabilities = []

        for iteration in range(iterations):
            # Generate a new seed for each iteration
            seed1 = random.randint(1, 1000)
            seed2 = random.randint(1, 1000)
            seed = seed1 * seed2
            random.seed(seed)

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

        # visualizer = ProteinVisualizer(best_protein)

        # plot_stability_distribution(stabilities)

        # visualizer.display()

        return best_protein
    
def plot_stability_distribution(stabilities):
        """
        Plot the distribution of stability over the iterations.
        
        Args:
            stabilities (list): List of stability values for each iteration.
        """
        plt.hist(stabilities, bins=30, edgecolor='black')
        plt.title('Distribution of Stability during Random Folding')
        plt.xlabel('Stability')
        plt.ylabel('Frequency')
        plt.show()

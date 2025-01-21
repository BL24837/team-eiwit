import copy
import random
from code.visualisation.visualize import ProteinVisualizer
from code.visualisation.distribution import Distribution

class RandomFolding:
    def __init__(self, protein):
        self.protein = protein

    def execute(self, iterations):
        """
        Voert het random folding-algoritme uit en zoekt naar de beste stabiliteit.

        Args:
            iterations (int): Aantal iteraties voor het random algoritme.

        Returns:
            Protein: Het eiwit met de beste gevonden stabiliteit.
        """
        best_protein = copy.deepcopy(self.protein)
        best_stability = best_protein.calculate_stability()
        stabilities = []

        for _ in range(iterations):
            print(f"Iteration {_ + 1}/{iterations}, Current best stability: {best_stability}")
            print(f"Current best stability: {best_stability}")

            success = self.perform_random_rotation()

            if success:
                stability = self.protein.calculate_stability()
                stabilities.append(stability)

                if stability < best_stability:
                    best_stability = stability
                    best_protein = copy.deepcopy(self.protein)

        print(f"Final best stability: {best_stability}")

        # Visualisatie
        Distribution(stabilities)
        visualizer = ProteinVisualizer(best_protein)
        visualizer.display()
        return best_protein
    
    def perform_random_rotation(self):
        """
        Voert een willekeurige rotatie uit op het eiwit.

        Returns:
            bool: True als de rotatie succesvol was, anders False.
        """
        directions = ['x_positive', 'x_negative', 'y_positive', 'y_negative', 'z_positive', 'z_negative']
        pivot_index = random.randint(0, len(self.protein.amino_acids) - 1)
        direction = random.choice(directions)
        rotation_matrices = self.protein.get_rotation_matrices()
        rotation_matrix = rotation_matrices[direction]

        if self.protein.is_rotation_valid(pivot_index, rotation_matrix):
            self.protein.rotate_protein(pivot_index, rotation_matrix)
            return True
        return False
        
    def check_rotation(self, pivot_index, rotation_matrix):
        """
        Checks if the rotation of the protein structure is valid.
        
        Args:
            pivot_index (int): The index of the pivot point.
            rotation_matrix (numpy.ndarray): The rotation matrix to rotate the protein.
        
        Returns:
            bool: True if the rotation is valid, False otherwise.
        """
        if self.protein.is_rotation_valid(pivot_index, rotation_matrix):
            self.protein.rotate_protein(pivot_index, rotation_matrix)
            return True
        return False
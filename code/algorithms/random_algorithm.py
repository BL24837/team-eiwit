import copy
import random
from code.classes.data_storing import DataStoring
from code.classes.protein import Protein
from code.visualisation.visualize import ProteinVisualizer
from code.visualisation.distribution import Distribution

class RandomFolding:
    def __init__(self, data, protein):
        self.data = data
        self.protein = protein

    def execute(self, iterations=10000):
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

        for i in range(iterations):
            print(f"Iteration {i + 1}/{iterations}, Current best stability: {best_stability}")
            print(f"Current best stability: {best_stability}")

            success = self.perform_random_rotation()

            if success:
                stability = self.protein.calculate_stability()
                self.data.random_folding(i + 1, stability)
                
                stabilities.append(stability)

                if stability < best_stability:
                    best_stability = stability
                    best_protein = copy.deepcopy(self.protein)

        print(f"Final best stability: {best_stability}")

        # Visualisatie
        Distribution(stabilities)

        self.data.random_folding(iterations, stability)
        
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
import copy
import random
import matplotlib.pyplot as plt
from code.visualisation.visualize import ProteinVisualizer
from code.visualisation.distribution import Distribution
from code.classes.protein import Protein

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

        for i in range(iterations):
            print(f"Iteration {i + 1}/{iterations}, Current best stability: {best_stability}")

            success = self.perform_random_rotation()

            if success:
                stability = self.protein.calculate_stability()
                stabilities.append(stability)

                if stability < best_stability:
                    best_stability = stability
                    best_protein = copy.deepcopy(self.protein)
            else:
                # Voeg de huidige beste stabiliteit toe aan de lijst, zelfs als de rotatie niet succesvol was
                stabilities.append(best_stability)

        print(f"Final best stability: {best_stability}")

        # Visualisatie van de distributie
        Distribution(stabilities)

        # Plot stabiliteit per iteratie
        self.plot_stability_per_iteration(stabilities)

        return best_protein

    def plot_stability_per_iteration(self, stabilities):
        """
        Maakt een plot met op de x-as het aantal iteraties en op de y-as de stabiliteit.

        Args:
            stabilities (list): Lijst van stabiliteitswaarden per iteratie.
        """
        plt.figure(figsize=(10, 6))
        plt.plot(range(1, len(stabilities) + 1), stabilities, marker='o', linestyle='-')
        plt.title("Stabiliteit per Iteratie bij Random Folding")
        plt.xlabel("Aantal Iteraties")
        plt.ylabel("Stabiliteit")
        plt.grid(True)
        plt.show()

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

if __name__ == "__main__":
    # Definieer de aminozuursequentie (voorbeeldsequentie)
    sequence = "HHPHHHPP"

    # Maak een Protein-object aan met de gegeven sequentie
    protein = Protein(sequence)

    # Initialiseer een RandomFolding-object met het eiwit
    random_folding = RandomFolding(protein)

    # Voer het algoritme uit en plot de resultaten
    best_protein = random_folding.execute(iterations=10000)


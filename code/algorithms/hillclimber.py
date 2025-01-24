from code.algorithms.random_algorithm import RandomFolding
from code.visualisation.visualize import ProteinVisualizer
from code.classes.data_storing import DataStoring
import copy
import random
import matplotlib.pyplot as plt

class HillClimber:
    def __init__(self, data: DataStoring, protein):
        """
        Initialiseer de HillClimber met een gegeven eiwit.
        
        Args:
            protein (Protein): Het eiwit dat zal worden geoptimaliseerd.
        """
        self.data = data
        self.protein = protein

    def execute(self, iterations, random_folding_iterations=1000):
        """
        Voer het HillClimber-algoritme uit om een eiwitvouwingsstructuur met optimale stabiliteit te vinden.

        Args:
            iterations (int): Het maximale aantal iteraties voor hill climbing.
            random_folding_iterations (int): Het aantal iteraties voor het random folding-algoritme om de startconfiguratie te genereren.

        Returns:
            Protein: De eiwitstructuur met de beste stabiliteit die is gevonden.
        """
        # Gebruik RandomFolding om een initiële configuratie te genereren
        print("Initializing with RandomFolding...")
        random_folding = RandomFolding(self.protein)
        best_protein = random_folding.execute(random_folding_iterations)
        best_stability = best_protein.calculate_stability()
        stabilities = [best_stability]

        print(f"Starting Hill Climber with initial stability: {best_stability}")

        for iteration in range(iterations):
            print(f"Iteration {iteration + 1}/{iterations}, Current best stability: {best_stability}")

            # Maak een willekeurige rotatie
            pivot_index, rotation_matrix = self.get_random_rotation(best_protein)
            if pivot_index is None or rotation_matrix is None:
                continue   # Sla over als de rotatie ongeldig is

            # Pas de rotatie tijdelijk toe
            original_state = copy.deepcopy(best_protein)
            best_protein.rotate_amino_acid(pivot_index, pivot_index, rotation_matrix)
            new_stability = best_protein.calculate_stability()

            # Accepteer de rotatie als de stabiliteit verbetert
            if new_stability < best_stability:
                best_stability = new_stability
            else:
                # Keer terug naar de vorige staat als er geen verbetering is
                best_protein = original_state

            stabilities.append(best_stability)

        print(f"Final best stability: {best_stability}")

        # Visualiseer de resultaten
        self.plot_stability_progress(stabilities)
        visualizer = ProteinVisualizer(best_protein)
        visualizer.display()

        return best_protein

    def get_random_rotation(self, protein):
        """
        Genereer een willekeurige rotatiematrix en pivotindex voor het eiwit.

        Args:
            protein (Protein): Het eiwit waarvoor de rotatie wordt berekend.

        Returns:
            tuple: De pivotindex en de rotatiematrix.
        """
        directions = list(protein.get_rotation_matrices().keys())
        pivot_index = random.randint(0, len(protein.amino_acids) - 1)
        direction = random.choice(directions)
        rotation_matrices = protein.get_rotation_matrices()
        rotation_matrix = rotation_matrices[direction]

        if protein.is_rotation_valid(pivot_index, rotation_matrix):
            return pivot_index, rotation_matrix
        return None, None

    def plot_stability_progress(self, stabilities):
        """
        Visualiseer de voortgang van de stabiliteit gedurende de iteraties.

        Args:
            stabilities (list): Een lijst van stabiliteitswaarden per iteratie.
        """
        plt.plot(stabilities, label="Stability Progress")
        plt.xlabel("Iteration")
        plt.ylabel("Stability")
        plt.title("Hill Climber Stability Progress")
        plt.legend()
        plt.show()
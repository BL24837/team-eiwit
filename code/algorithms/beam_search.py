import csv
import numpy as np
import matplotlib.pyplot as plt
from code.classes.data_storing import DataStoring
from code.visualisation.visualize import *
from code.classes.protein import *
from code.visualisation.timer import Timer

import copy

class BeamSearchProteinFolding:
    """
    Implements the Beam Search algorithm for optimizing protein folding.
    This algorithm balances exploration and exploitation by maintaining a fixed number
    of candidate configurations (beam width) at each step.

    Attributes:
        data (DataStoring): Object to store and handle result data.
        sequence (str): Protein sequence to be folded.
        beam_width (int): Number of top configurations to retain at each step.
        directions (list): List of possible movement directions in 3D space.
        stabilities (list): Stability scores of all generated configurations.
    """
    
    def __init__(self, data, sequence, beam_width):
        """
        Initializes the Beam Search class with the given protein sequence and beam width.

        Args:
            data (DataStoring): Object for managing data storage.
            sequence (str): Protein sequence to be folded.
            beam_width (int): Number of top configurations to keep at each step.
        """
        self.data = data
        self.sequence = sequence
        self.beam_width = beam_width
        self.directions = [
            np.array([0, 1, 0]),  # Move up
            np.array([1, 0, 0]),  # Move right
            np.array([0, -1, 0]), # Move down
            np.array([-1, 0, 0]), # Move left
            np.array([0, 0, 1]),  # Move forward
            np.array([0, 0, -1])  # Move backward
        ]
        self.stabilities = []  # Storage for stability scores of generated candidates

    def execute(self, plot_distribution=True):
        """
        Executes the Beam Search algorithm to find an optimal protein configuration.

        Args:
            plot_distribution (bool): Whether to plot the stability distribution after execution.

        Returns:
            Protein: The best protein configuration found.
        """
        # Create the initial protein object
        protein = Protein(self.sequence)
        n = len(protein.amino_acids)  # Number of amino acids in the sequence

        # Initialize the beam with the starting configuration
        beam = [protein]

        # Iterate over each amino acid (excluding the first, which is fixed)
        for step in range(1, n):
            candidates = []  # Stores candidate configurations for the current step

            # Generate new configurations from the current beam
            for current_protein in beam:
                last_pos = current_protein.amino_acids[step - 1]["position"]  # Last placed amino acid's position

                # Try placing the next amino acid in all possible directions
                for direction_index, direction in enumerate(self.directions):
                    new_pos = last_pos + direction

                    # Ensure the new position is valid (not overlapping)
                    if not any(np.array_equal(new_pos, aa["position"]) for aa in current_protein.amino_acids[:step]):
                        # Create a new protein object with the updated position
                        new_protein = copy.deepcopy(current_protein)
                        new_protein.amino_acids[step]["position"] = new_pos
                        stability = new_protein.calculate_stability()  # Compute stability score
                        candidates.append((stability, new_protein))  # Store candidate

            # Keep only the top candidates based on stability (lower is better)
            candidates.sort(key=lambda x: x[0])  # Sort by stability
            beam = [protein for _, protein in candidates[:self.beam_width]]  # Retain top candidates

            # Save stability scores for visualization
            self.stabilities.extend([stability for stability, _ in candidates])

        # Optionally plot the stability distribution
        if plot_distribution:
            self.plot_stability_distribution()

        # Return the best configuration from the final beam
        best_protein = min(beam, key=lambda protein: protein.calculate_stability())
        return best_protein

    def plot_stability_distribution(self):
        """
        Plots the distribution of stability scores across all generated configurations.
        """
        if not self.stabilities:
            print("No stability scores to visualize. Run the algorithm first.")
            return

        # Plot histogram of stability scores
        plt.hist(self.stabilities, bins=30, edgecolor='black')
        plt.title('Distribution of Stability Scores in Beam Search')
        plt.xlabel('Stability Score')
        plt.ylabel('Frequency')
        plt.show()

    def export_results(self, protein, score, elapsed_time):
        """
        Exports the results of the Beam Search to a file.

        Args:
            protein (Protein): The final protein configuration.
            score (float): The stability score of the final configuration.
            elapsed_time (float): The time taken to execute the algorithm.
        """
        self.data.beam_search_data(protein, score, elapsed_time)

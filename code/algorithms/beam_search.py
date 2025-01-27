import csv
import numpy as np
import matplotlib.pyplot as plt
from code.classes.data_storing import DataStoring
from code.visualisation.visualize import *
from code.classes.protein import *
from code.visualisation.timer import Timer
from datetime import datetime, timedelta
from helpers import *

import time

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
    
    def __init__(self, data, protein, beam_width):
        """
        Initializes the Beam Search class with the given protein sequence and beam width.

        Args:
            data (DataStoring): Object for managing data storage.
            sequence (str): Protein sequence to be folded.
            beam_width (int): Number of top configurations to keep at each step.
        """
        self.data = data
        self.protein = protein
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
        protein = Protein(self.protein.sequence)
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
    
    def execute_with_dynamic_beam_width(self, end_time):
        """
        Voert Beam Search uit met dynamische beam widths tot de opgegeven eindtijd.
        Retourneert de beste vouwing en logt gegevens via DataStoring.

        :param end_time: Eindtijd voor de uitvoering.
        :return: Best gevonden Protein.
        """
        n = len(self.protein.amino_acids)

        beam_width = 1
        best_protein = None
        best_stability = float('inf')
        beam_data = []

        while datetime.now() < end_time:
            protein = Protein(self.protein.sequence)
            # Initialiseer de beam met de startconfiguratie
            beam = [protein]

            timer = Timer()
            timer.start()

            for step in range(1, n):
                candidates = []

                # Genereer nieuwe configuraties vanuit de huidige beam
                for current_protein in beam:
                    last_pos = current_protein.amino_acids[step - 1]["position"]
                    for direction in self.directions:
                        new_pos = last_pos + direction

                        # Controleer of de nieuwe positie geldig is
                        if not any(np.array_equal(new_pos, aa["position"]) for aa in current_protein.amino_acids[:step]):
                            new_protein = copy.deepcopy(current_protein)
                            new_protein.amino_acids[step]["position"] = new_pos
                            stability = new_protein.calculate_stability()
                            candidates.append((stability, new_protein))

                # Behoud alleen de beste configuraties
                candidates.sort(key=lambda x: x[0])
                beam = [protein for _, protein in candidates[:beam_width]]

            # Zoek de beste configuratie in de huidige beam
            current_best_protein = min(beam, key=lambda protein: protein.calculate_stability())
            current_stability = current_best_protein.calculate_stability()

            if current_stability < best_stability:
                best_stability = current_stability
                best_protein = current_best_protein

                    # Voeg gegevens toe voor deze beam width
            timer.stop()
            elapsed_time = timer.elapsed_time()
            beam_data.append((beam_width, elapsed_time, current_stability))


            # Verhoog de beam width voor de volgende iteratie
            beam_width += 1

        # Log alle verzamelde beam search gegevens via DataStoring
        # self.data.log_beam_search(beam_data)


        return best_protein, beam_data

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

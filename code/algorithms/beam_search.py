from code.classes.data_storing import DataStoring
from code.classes.protein import Protein
from code.classes.protein import Protein
from code.visualisation.timer import Timer
from datetime import datetime

import copy
import numpy as np

class BeamSearchProteinFolding:
    """
    Implements the Beam Search algorithm for optimizing protein folding.
    Maintains a fixed number of candidate configurations (beam width) at each step.
    """

    def __init__(self, data: DataStoring, protein: Protein, beam_width: int):
        """
        Initializes the Beam Search class.

        Args:
            data (DataStoring): Object for managing data storage.
            protein (Protein): The protein object to fold.
            beam_width (int): Number of top configurations to keep at each step.
        """
        self.data = data
        self.protein = protein
        self.beam_width = beam_width
        self.directions = [
            np.array([0, 1, 0]), np.array([1, 0, 0]), np.array([0, -1, 0]),
            np.array([-1, 0, 0]), np.array([0, 0, 1]), np.array([0, 0, -1])
        ]
        self.stabilities = []  # Stores stability scores of configurations

    def execute(self) -> Protein:
        """
        Executes the Beam Search algorithm to find an optimal protein configuration.

        Args:
            plot_distribution (bool): Whether to plot the stability distribution after execution.

        Returns:
            Protein: The best protein configuration found.
        """
        beam_data=[]
        protein = Protein(self.protein.sequence)
        n = len(protein.amino_acids)

        beam = [protein]  # Initialize the beam with the starting configuration
        timer = Timer()
        timer.start()

        for step in range(1, n):
            candidates = []  # Store candidate configurations for the current step
            

            for current_protein in beam:
                last_pos = current_protein.amino_acids[step - 1]["position"]

                # Try placing the next amino acid in all possible directions
                for direction in self.directions:
                    new_pos = last_pos + direction

                    if not any(np.array_equal(new_pos, aa["position"]) for aa in current_protein.amino_acids[:step]):
                        new_protein = copy.deepcopy(current_protein)
                        new_protein.amino_acids[step]["position"] = new_pos
                        stability = new_protein.calculate_stability()
                        candidates.append((stability, new_protein))

            candidates.sort(key=lambda x: x[0])  # Sort by stability (lower is better)
            beam = [protein for _, protein in candidates[:self.beam_width]]  # Retain top candidates

            # Save stability scores for visualization
            self.stabilities.extend([stability for stability, _ in candidates])

            timer.stop()
            elapsed_time = timer.elapsed_time()
            beam_data.append((self.beam_width, elapsed_time, stability))
        
            self.export_results(beam_data)

        # Return the best configuration
        best_protein = min(beam, key=lambda protein: protein.calculate_stability())
        return best_protein

    def execute_with_dynamic_beam_width(self, end_time: datetime) -> tuple[Protein, list[tuple[int, float, float]]]:
        """
        Executes Beam Search with dynamically increasing beam widths until a given end time.

        Args:
            end_time (datetime): The time to stop execution.

        Returns:
            tuple: The best found Protein and a list of tuples with beam data.
        """
        n = len(self.protein.amino_acids)

        beam_width = 1
        best_protein = None
        best_stability = float('inf')
        beam_data = []

        while datetime.now() < end_time:
            protein = Protein(self.protein.sequence)
            beam = [protein]  # Initialize the beam
            timer = Timer()
            timer.start()

            for step in range(1, n):
                candidates = []

                for current_protein in beam:
                    last_pos = current_protein.amino_acids[step - 1]["position"]
                    for direction in self.directions:
                        new_pos = last_pos + direction

                        if not any(np.array_equal(new_pos, aa["position"]) for aa in current_protein.amino_acids[:step]):
                            new_protein = copy.deepcopy(current_protein)
                            new_protein.amino_acids[step]["position"] = new_pos
                            stability = new_protein.calculate_stability()
                            candidates.append((stability, new_protein))

                candidates.sort(key=lambda x: x[0])
                beam = [protein for _, protein in candidates[:beam_width]]

            current_best_protein = min(beam, key=lambda protein: protein.calculate_stability())
            current_stability = current_best_protein.calculate_stability()

            if current_stability < best_stability:
                best_stability = current_stability
                best_protein = current_best_protein

            timer.stop()
            elapsed_time = timer.elapsed_time()
            beam_data.append((beam_width, elapsed_time, current_stability))

            beam_width += 5  # Increase the beam width for the next iteration

            self.export_results(beam_data)
            beam_data = []

        return best_protein

    def export_results(self, beam_data:list[tuple[int, float, float]]) -> None:
        
        """
        Exports the results of the Beam Search to a file.

        Args:
            protein (Protein): The final protein configuration.
            score (float): The stability score of the final configuration.
            elapsed_time (float): The time taken to execute the algorithm.
        """
        self.data.beam_search_data(beam_data)

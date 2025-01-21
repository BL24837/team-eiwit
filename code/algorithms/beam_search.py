import numpy as np

from code.visualisation.visualize import *
from code.classes.protein import *
import copy

class BeamSearchProteinFolding:
    def __init__(self, sequence, beam_width):
        """
        Initialiseert de Beam Search klasse met een sequentie en een beam width.
        """
        self.sequence = sequence
        self.beam_width = beam_width
        self.directions = [
            np.array([0, 1, 0]), np.array([1, 0, 0]), np.array([0, -1, 0]), np.array([-1, 0, 0]),
            np.array([0, 0, 1]), np.array([0, 0, -1])
        ]

    def run(self):
        """
        Voert beam search uit om de stabiliteit van een eiwitconfiguratie te optimaliseren.
        """
        protein = Protein(self.sequence)
        n = len(protein.amino_acids)

        # Initialiseer de beam met de startconfiguratie
        beam = [protein]

        # Itereer over alle aminozuren (behalve de eerste)
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
            beam = [protein for _, protein in candidates[:self.beam_width]]

        # Retourneer de beste configuratie
        best_protein = min(beam, key=lambda protein: protein.calculate_stability())
        return best_protein
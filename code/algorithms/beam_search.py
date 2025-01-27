import csv
import numpy as np
import matplotlib.pyplot as plt
from code.classes.data_storing import DataStoring
from code.visualisation.visualize import *
from code.classes.protein import *
from code.visualisation.timer import Timer
from helpers import *

import copy

class BeamSearchProteinFolding:
    def __init__(self, data: DataStoring , protein:Protein, beam_width):
        """
        Initialiseert de Beam Search klasse met een sequentie en een beam width.
        """
        self.data = data
        self.protein = protein
        self.beam_width = beam_width
        self.directions = [
            np.array([0, 1, 0]), np.array([1, 0, 0]), np.array([0, -1, 0]), np.array([-1, 0, 0]),
            np.array([0, 0, 1]), np.array([0, 0, -1])
        ]
        self.stabilities = []  # Opslag voor stabiliteit van kandidaten

    def execute(self, plot_distribution=True):
        """
        Voert beam search uit om de stabiliteit van een eiwitconfiguratie te optimaliseren.
        """
        n = len(self.protein.amino_acids)

        # Initialiseer de beam met de startconfiguratie
        beam = [protein]

        # Itereer over alle aminozuren (behalve de eerste)
        for step in range(1, n):
            candidates = []

            # Genereer nieuwe configuraties vanuit de huidige beam
            for current_protein in beam:
                last_pos = current_protein.amino_acids[step - 1]["position"]
                for direction_index, direction in enumerate(self.directions):
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

            # Stabiliteit van alle kandidaten opslaan
            self.stabilities.extend([stability for stability, _ in candidates])

        # Plot de distributie als dit is aangevraagd
        # if plot_distribution:
        #     self.plot_stability_distribution()

        # Retourneer de beste configuratie
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
            # Initialiseer de beam met de startconfiguratie
            beam = [protein]

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
            elapsed_time = (datetime.now() - end_time).total_seconds()  # Bereken de tijd
            beam_data.append((beam_width, elapsed_time, current_stability))


            # Verhoog de beam width voor de volgende iteratie
            beam_width += 1

        # Log alle verzamelde beam search gegevens via DataStoring
        self.data.log_beam_search(beam_data)


        return best_protein

    def plot_stability_distribution(self):
        """
        Plot de distributie van stabiliteit over de verschillende iteraties.
        """
        if not self.stabilities:
            print("Geen stabiliteitsscores om te visualiseren. Voer eerst het algoritme uit.")
            return
        
        plt.hist(self.stabilities, bins=30, edgecolor='black')
        plt.title('Distributie van stabiliteit bij Beam Search')
        plt.xlabel('Stabiliteit')
        plt.ylabel('Frequentie')
        plt.show()

    def export_results(self, protein, score, elapsed_time):
        """
        Exporteer de resultaten in het juiste format naar een bestand.
        """
        self.data.beam_search_data(protein, score, elapsed_time)
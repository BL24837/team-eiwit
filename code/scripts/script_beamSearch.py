import numpy as np
import matplotlib.pyplot as plt
import sys
import os
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from ..algorithms.beam_search import BeamSearchProteinFolding

def score_vs_beam_width(sequence):
    """
    Plot op de x-as de score en op de y-as de beam_width
    """
    # Bereken scores voor verschillende beam widths
    beam_widths = range(1, 10, 2)
    scores = []

    for width in beam_widths:
        beam_search = BeamSearchProteinFolding(sequence, width)
        best_protein = beam_search.run()
        scores.append(best_protein.calculate_stability())

    # Plot de resultaten
    plt.figure(figsize=(10, 6))
    plt.plot(beam_widths, scores, marker='o', linestyle='-', label=f"Sequence: {sequence}")
    plt.title("Beam Width vs. Stability Score")
    plt.xlabel("Beam Width")
    plt.ylabel("Score")
    plt.legend()
    plt.grid()
    plt.show()

def time_vs_beam_width(sequence):
    # Bereken tijden voor verschillende beam widths
    beam_widths = range(1, 4, 1)
    times = []

    for width in beam_widths:
        beam_search = BeamSearchProteinFolding(sequence, width)
        
        # Meet de tijd
        start_time = time.time()
        best_protein = beam_search.run()
        end_time = time.time()
        
        # Bereken de tijdsduur
        elapsed_time = end_time - start_time
        times.append(elapsed_time)

        # Plot de resultaten
    plt.figure(figsize=(10, 6))
    plt.plot(beam_widths, times, marker='o', linestyle='-', label=f"Sequence: {sequence}")
    plt.title("Beam Width vs. Execution Time")
    plt.xlabel("Beam Width")
    plt.ylabel("Execution Time (seconds)")
    plt.xticks(beam_widths)
    plt.legend()
    plt.grid()
    plt.show()

time_vs_beam_width("HHHPH")




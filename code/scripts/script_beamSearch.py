import numpy as np
import matplotlib.pyplot as plt
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from code.algorithms.beam_search import BeamSearchProteinFolding

def main():
    sequence = "HHPHPH"

    # Bereken scores voor verschillende beam widths
    beam_widths = range(1, 1002, 50)
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

if __name__ == "__main__":
    main()
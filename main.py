from code.visualisation.visualize import ProteinVisualizer
from code.visualisation.timer import Timer
from code.classes.protein import Protein
from code.classes.data_storing import DataStoring
from code.algorithms.beam_search import *

import helpers
import os


def main():
    # choice, algorithm = helpers.get_algorithm()
    # sequence = None

    # if not choice == "7":
    #     sequence = helpers.get_sequence()
    #     protein = Protein(sequence)
    #     filename = helpers.get_filename()
    #     folded_protein = helpers.run_algorithm(choice=choice, protein=protein, algorithm=algorithm, filename=filename)

    # elif choice == "7":
        
    #     choice_menu = helpers.get_choise_menu()

    #     helpers.run_choise_menu(choice_menu, protein)

    # else:
    #     print("Invalid choice. Please select 1, 2, 3, 4, or 5.")
    #     return

    # print("1: Stabillity")
    # print("2: Visualizer")
    # print("3: Both")
    # choice = input("Enter your choice (1, 2 or 3): ").strip()

    # if choice == "1":
    #     # Stabillity
    #     stability = folded_protein.calculate_stability()
    #     print(f"Protein Stability after folding: {stability}")

    # elif choice == "2":
    #     # Visualize protein
    #     visualizer = ProteinVisualizer(folded_protein)
    #     visualizer.display()

    # elif choice == "3":
    #     # Stabillity en visualize protein
    #     stability = folded_protein.calculate_stability()
    #     print(f"Protein Stability after folding: {stability}")
    #     visualizer = ProteinVisualizer(folded_protein)
    #     visualizer.display()
    while(True):
        algorithm = "Beam search folding"
        sequence = "CPPCHPPCHPPCPPHHHHHHCCPCHPPCPCHPPHPC"
        protein = Protein(sequence)
        filename = os.path.join(os.path.dirname(__file__), 'results', 'bb_exp2.csv')
        data = DataStoring(algorithm=algorithm, filename=filename)
        sequence = protein.sequence
        beam_width = 10
        timer = Timer()
        timer.start()
        beam_search = BeamSearchProteinFolding(data, sequence, beam_width)
        folded_protein = beam_search.execute() # extra optie plot_distribution = False
        timer.stop()
        elapsed = timer.elapsed_time()
        score = folded_protein.calculate_stability()
        print(elapsed)
        beam_search.export_results(folded_protein, score, elapsed)

if __name__ == "__main__":
    main()

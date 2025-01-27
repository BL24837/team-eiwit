from code.visualisation.visualize import *
from code.visualisation.timer import Timer
from code.classes.protein import Protein
from helpers import *
import pandas as pd
import matplotlib.pyplot as plt
from code.algorithms.greedy_algorithm import *
from code.algorithms.random_algorithm import *
from code.algorithms.hillclimber import *
from code.algorithms.beam_search import *
from code.algorithms.Simulatedannealing import *


def main():
    choice, algorithm = helpers.get_algorithm()
    sequence = None

    if not choice == "7":
        # Vraag de gebruiker om de sequentie en maak het Protein-object
        sequence = helpers.get_sequence()
        protein = Protein(sequence)

        # Vraag de gebruiker om de naam van het CSV-bestand
        filename = helpers.get_filename()

        # Vraag of de gebruiker een enkele run wil of 30 minuten
        print("1: Single run")
        print("2: loop algorithme")
        execution_mode = input("Enter your choice (1 or 2): ").strip()
        print("How many minutes you want to loop")
        x_times = input(" ").strip()
        x_times = int(x_times)

        if execution_mode == "1":
            # Voer een enkele run uit
            folded_protein = helpers.run_algorithm(choice=choice, protein=protein, algorithm=algorithm, filename=filename)

            print("1: Stability")
            print("2: Visualizer")
            print("3: Both")
            choice = input("Enter your choice (1, 2 or 3): ").strip()

            if choice == "1":
                # Stabiliteit tonen
                stability = folded_protein.calculate_stability()
                print(f"Protein Stability after folding: {stability}")

            elif choice == "2":
                # Protein visualiseren
                visualizer = ProteinVisualizer(folded_protein)
                visualizer.display()

            elif choice == "3":
                # Stabiliteit en visualisatie
                stability = folded_protein.calculate_stability()
                print(f"Protein Stability after folding: {stability}")
                visualizer = ProteinVisualizer(folded_protein)
                visualizer.display()

        elif execution_mode == "2":
            # Voer het algoritme 30 minuten uit
            run_algorithm_for_x_minutes(choice, protein, algorithm, filename,x_times)



        else:
            print("Invalid execution mode selected.")

    elif choice == "7":
        # Speciale menu-opties
        choice_menu = helpers.get_choise_menu()
        helpers.run_choise_menu(choice_menu, protein)

    else:
        print("Invalid choice. Please select 1, 2, 3, 4, or 5.")
        return
    
if __name__ == "__main__":
    print("Hello, welcome to the protein folding application!")
    main()

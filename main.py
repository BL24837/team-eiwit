from code.visualisation.visualize import *
from code.classes.protein import Protein
from helpers import *
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

        # Maakt het proteine object aan
        protein = Protein(sequence)

        # Vraag de gebruiker om de naam van het CSV-bestand
        filename = helpers.get_filename()

        # Vraag of de gebruiker een enkele run wil of 30 minuten
        sort_run = helpers.get_sort_run()

        if sort_run == "1":
            # Voer een enkele run uit
            folded_protein = helpers.run_algorithm(choice=choice, protein=protein, algorithm=algorithm, filename=filename)

            sub_menu = helpers.get_sub_menu

            if sub_menu == "1":
                # Stabiliteit tonen
                stability = folded_protein.calculate_stability()
                print(f"Protein Stability after folding: {stability}")

            elif sub_menu == "2":
                # Protein visualiseren
                visualizer = ProteinVisualizer(folded_protein)
                visualizer.display()

            elif sub_menu == "3":
                # Stabiliteit en visualisatie
                stability = folded_protein.calculate_stability()
                print(f"Protein Stability after folding: {stability}")
                visualizer = ProteinVisualizer(folded_protein)
                visualizer.display()

        elif sort_run == "2":
            minutes = helpers.get_minutes()
            run_algorithm_for_x_minutes(choice, protein, algorithm, filename, minutes)

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

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
        # Ask the user for the sequence and create the Protein object
        sequence = helpers.get_sequence()

        # Create the Protein object
        protein = Protein(sequence)

        # Ask the user for the name of the CSV file
        filename = helpers.get_filename()
        
        # Ask the user if they want to run a single execution or for multiple minutes
        sort_run = helpers.get_sort_run()

        if sort_run == "1":
            # Perform a single execution
            folded_protein = helpers.run_algorithm(choice=choice, protein=protein, algorithm=algorithm, filename=filename)

            sub_menu = helpers.get_sub_menu()

            if sub_menu == "1":
                # Display stability
                stability = folded_protein.calculate_stability()
                print(f"Protein Stability after folding: {stability}")

            elif sub_menu == "2":
                # Visualize the protein
                visualizer = ProteinVisualizer(folded_protein)
                visualizer.display()

            elif sub_menu == "3":
                # Display stability and visualize the protein
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
        # Special menu options
        choice_menu = helpers.get_choise_menu()
        helpers.run_choise_menu(choice_menu, protein)

    else:
        print("Invalid choice. Please select 1, 2, 3, 4, or 5.")
        return
    
if __name__ == "__main__":
    print("Hello, welcome to the protein folding application!")
    main()

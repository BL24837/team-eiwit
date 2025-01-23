from code.visualisation.visualize import ProteinVisualizer
from code.classes.protein import *
import helpers

def main():
    choice, algorithm = helpers.get_algorithm()

    if not choice == "6":
        sequence = helpers.get_sequence()
        protein = Protein(sequence)
        dimension = helpers.get_dimension()
        filename = helpers.get_filename()
        folded_protein = helpers.run_algorithm(choice, protein, dimension, algorithm, filename)

    elif choice == "6":
        
        choice_menu = helpers.get_choise_menu()

        helpers.run_choise_menu(choice_menu, protein)

    else:
        print("Invalid choice. Please select 1, 2, 3, 4, or 5.")
        return

    print("1: Stabillity")
    print("2: Visualizer")
    print("3: Both")
    choice = input("Enter your choice (1, 2 or 3): ").strip()

    if choice == "1":
        # Stabillity
        stability = folded_protein.calculate_stability()
        print(f"Protein Stability after folding: {stability}")

    elif choice == "2":
        # Visualize protein
        visualizer = ProteinVisualizer(folded_protein)
        visualizer.display()

    elif choice == "3":
        # Stabillity en visualize protein
        stability = folded_protein.calculate_stability()
        print(f"Protein Stability after folding: {stability}")
        visualizer = ProteinVisualizer(folded_protein)
        visualizer.display()

if __name__ == "__main__":
    main()

from code.algorithms.greedy_algorithm import *
from code.algorithms.random_algorithm import *
from code.algorithms.hillclimber import *
from code.algorithms.beam_search import *
from code.algorithms.Simulatedannealing import *
from code.visualisation.data import Data
from code.visualisation.visualize import ProteinVisualizer
from code.classes.protein import *

def main():
    # Fill in your sequence
    sequence = "PPCHHPPCHPPPPCHHHHCHHPPHHPPPPHHPPHPP"

    # Create a Protein object
    protein = Protein(sequence)

    # Select folding algorithm
    print("Select folding algorithm:")
    print("1: Random Folding")
    print("2: Hillclimber")
    print("3: Greedy Folding")
    print("4: Beam search folding")
    print("5: Simulatedannealing folding")
    print("6: Other options")
    choice = input("Enter your choice (1, 2 ,3 ,4, 5 or 6): ").strip()

    if choice == "1":
        # Perform random folding
        iterations = int(input("Enter the number of iterations for random folding: ").strip())
        random_folding = RandomFolding(protein)
        folded_protein = random_folding.execute(iterations=iterations)
    
    elif choice == "2":
        # Perform hillclimber folding
        iterations = int(input("Enter the number of iterations for hillclimber folding: ").strip())
        hillclimber_folding = HillClimber(protein)
        folded_protein = hillclimber_folding.execute(iterations=iterations)
    
    elif choice == "3":
        # Perform greedy folding
        greedy_folding = GreedyFolding(protein)
        folded_protein = greedy_folding.execute()

    elif choice == "4":
        # Perform beam search
        beam_width = int(input("Enter the beam width for beam search folding: ").strip())
        beam_search = BeamSearchProteinFolding(sequence, beam_width)
        folded_protein = beam_search.run()

    elif choice == "5":
        # Perform simulated annealing
        sa = SimulatedAnnealing(protein)
        folded_protein = sa.run()

    elif choice == "6":
        print("1: Length of protein")

        choice = input("Enter your choice (1, 2 ,3 ,4 or 5): ").strip()

        if choice == "1":
            print(f"Length of protein: {len(protein.amino_acids)}")
            return
        
        else:
            print("Invalid choice. Please select 1, 2, 3, 4, or 5.")
            return
    
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

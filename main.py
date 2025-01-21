from code.algorithms.greedy_algorithm import *
from code.algorithms.random_algorithm import *
from code.algorithms.hillclimber import *
from code.algorithms.beam_search import *
from code.algorithms.Simulatedannealing import *
from code.visualisation.visualize import ProteinVisualizer
from code.classes.protein import *

def main():
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
    choice = input("Enter your choice (1, 2 ,3 ,4 or 5): ").strip()

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
        greedy_folding = HybridFolding(protein)
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

    else:
        print("Invalid choice. Please select 1, 2, 3, 4, or 5.")
        return

    # Calculate the stability of the protein
    stability = folded_protein.calculate_stability()
    print(f"Protein Stability after folding: {stability}")

    # Initialize the visualizer
    visualizer = ProteinVisualizer(folded_protein)

    # Show the 3D visualization of the protein
    visualizer.display()

if __name__ == "__main__":
    main()


from code.algorithms.greedy_algorithm import *
from code.algorithms.random_algorithm import *
from code.algorithms.hillclimber import *
from code.visualisation.visualize import ProteinVisualizer
from code.classes.protein import *

def main():
    sequence = "HHPHHHPHPHHHPH"

    # Create a Protein object
    protein = Protein(sequence)

    # Select folding algorithm
    print("Select folding algorithm:")
    print("1: Random Folding")
    print("2: Hillclimber")
    print("3: Greedy Folding")
    choice = input("Enter your choice (1, 2 or 3): ").strip()

    if choice == "1":
        # Perform random folding
        iterations = int(input("Enter the number of iterations for random folding: ").strip())
        random_folding = RandomFolding(protein)
        folded_protein = random_folding.execute(iterations=iterations)
    
    if choice == "2":
        # Perform random folding
        iteration = int(input("Enter the number of iterations for hillclimber folding: ").strip())
        hillclimber_folding = HillClimb(protein)
        folded_protein = hillclimber_folding.execute(iteration=iteration)
    
    elif choice == "3":
        # Perform greedy folding
        greedy_folding = HybridFolding(protein)
        folded_protein = greedy_folding.execute()
    
    else:
        print("Invalid choice. Please select 1, 2, or 3.")
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

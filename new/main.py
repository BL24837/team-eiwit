from protein import Protein
from visualize import ProteinVisualizer
from random_algorithm import RandomFolding

def main():
    # Define a protein sequence
    sequence = "HHPHHHPH"

    # Create a Protein object
    protein = Protein(sequence)

    # Perform random folding
    random_folding = RandomFolding(protein)
    folded_protein = random_folding.execute(iterations=10000)

    # Calculate the stability of the protein
    stability = folded_protein.calculate_stability()
    print(f"Protein Stability after random folding: {stability}")

    # Initialize the visualizer
    visualizer = ProteinVisualizer(folded_protein)

    # Show the 3D visualization of the protein
    visualizer.display()

if __name__ == "__main__":
    main()

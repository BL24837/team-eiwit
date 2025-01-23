import numpy as np
from visualize import *
from protein import *
import copy

def beam_search_protein_folding_with_class(sequence, beam_width):
    """
    Perform beam search for protein folding using the Protein class.
    """
    directions = [
        np.array([0, 1, 0]), np.array([1, 0, 0]), np.array([0, -1, 0]), np.array([-1, 0, 0]),
        np.array([0, 0, 1]), np.array([0, 0, -1])
    ]  # 3D grid directions

    protein = Protein(sequence)
    n = len(protein.amino_acids)

    # Initialize beam with the starting configuration
    beam = [protein]

    # Loop over alle aminozuren in het eiwit (behalve de eerste)
    for step in range(1, n):
        candidates = []
        # Itereer over huidige configuraties in de beam
        for current_protein in beam:
            last_pos = current_protein.amino_acids[step - 1]["position"]
            for direction in directions:
                new_pos = last_pos + direction

                # Controleert of de nieuwe positie niet al bezet is door een eerder geplaatst aminozuur.
                if not any(np.array_equal(new_pos, aa["position"]) for aa in current_protein.amino_acids[:step]):
                    # Create a new protein configuration
                    new_protein = copy.deepcopy(current_protein)
                    new_protein.amino_acids[step]["position"] = new_pos
                    stability = new_protein.calculate_stability()
                    candidates.append((stability, new_protein))

        # Soreer de scores en behoud alleen de beste configuraties
        candidates.sort(key=lambda x: x[0])
        beam = [protein for _, protein in candidates[:beam_width]]

    # Return de beste configuratie
    best_protein = min(beam, key=lambda protein: protein.calculate_stability())
    return best_protein


# Example usage
sequence = "HCPHPHPHCHHHHPCCPPHPPPHPPPPCPPPHPPPHPHHHHCHPHPHPHH"
beam_width = 10 # Het maximaal aantal configuraties dat per stap wordt bijgehouden (breedte van de beam).
best_protein = beam_search_protein_folding_with_class(sequence, beam_width)

# Visualize the result
visualizer = ProteinVisualizer(best_protein)
visualizer.display()
print("Final Protein Configuration:")

# Print stability score
print("Best Stability Score:", best_protein.calculate_stability())
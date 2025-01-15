from code.classes.protein import Protein
from code.visualisation.board import *
from code.classes.visualize import Visualize
from code.classes.utils import utils

import random

protein = Protein("HCHC")  # Sample sequence
best_score = protein.random_fold(iterations=1000)
print(f"Best score found: {best_score}")


# # random fold algoritme
# def random_fold_protein(sequence):
#     protein = Protein(sequence)
#     x, y, z = 0, 0, 0
#     i = 0

#     for amino_acid in protein.sequence:
#         amino_acid_obj = AminoAcid(amino_acid, i, x, y, z, 0)
#         protein.add_aminoacid(amino_acid_obj)
#         grid.place_on_grid(x, y, z, amino_acid_obj)

#         if i == 0:
#             i += 1
#             continue

#         valid_move = False
#         while not valid_move:
#             move = random.choice([(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0)])
#             new_x, new_y, new_z = x + move[0], y + move[1], z + move[2]
            
#             # Check if the new position is already occupied
#             if grid.grid.get((new_x, new_y, new_z)) is None:
#                 # Update position and add amino acid
#                 x, y, z = new_x, new_y, new_z
#                 grid.place_on_grid(x, y, z, amino_acid_obj)
#                 valid_move = True
#                 i += 1

#     score = grid.calculate_score()
#     print(f"Final score: {score}")
#     return score

# if __name__ == "__main__":
#     sequence = "HHPHHHPH"

#     for char in range(1000000):
#         random_fold_protein(sequence)


































# def fold_protein(sequence):
#     protein = Protein(sequence)
#     x, y = 0, 0
#     for amino in protein.sequence:
#         protein.place_on_grid(x, y, amino)
#         x += 1  
#     protein.calculate_score()
#     return protein








    # sequences = utils.read_sequences(f"data/sequences.csv")
    

    # for seq_data in sequences:
    #     protein = fold_protein(seq_data['sequence'])
    #     print(f"Protein ID: {seq_data['id']}")
    #     print(f"Sequence: {seq_data['sequence']}")
    #     print(f"Score: {protein.score}")
    #     print("Structure:")
    #     protein.print_structure()
    #     print("---")
    #     Visualize.visualize_protein(protein)

    #     for seq_data in sequences:
    #         protein = fold_protein(seq_data['sequence'])
    #         output_file = f"results/output.csv"
    #         utils.export_results_to_csv(protein, output_file)
    #         print(f"Results for {seq_data['id']} written to {output_file}")
    #         break
    #     break





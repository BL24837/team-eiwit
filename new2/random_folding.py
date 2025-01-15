from aminoacid import *
from board import *
from protein import *
import matplotlib.pyplot as plt

def fold_protein(protein_state):
    for index in range(1, len(protein_state.sequence)):
        current_aa_type = protein_state.sequence[index]
        valid_moves = protein_state.get_valid_moves()
        random.shuffle(valid_moves)

        for dx, dy in valid_moves:
            last_x, last_y = protein_state.board.positions[-1]
            new_pos = (last_x + dx, last_y + dy)

            if not protein_state.board.is_occupied(new_pos):
                new_aa = AminoAcid(current_aa_type, new_pos)
                protein_state.board.place_amino_acid(new_aa)
                protein_state.board.update_score(new_aa)
                break

def random_folding(sequence):
    protein = ProteinState(sequence)
    fold_protein(protein)
    #protein.board.plot_board()
    return protein.board.score
    print(f"Final score: {protein.board.score}")

def run_multiple_random_foldings(sequence, iterations=1000):
    scores = [random_folding(sequence) for _ in range(iterations)]
    min_score = min(scores)  # Bepaal de minimale score uit de lijst
    bins = list(range(min_score, 2))  # Bins op basis van de minimale score
    plt.hist(scores, bins=bins, edgecolor='black', align='left')
    plt.xticks(bins)

    plt.title(f'Distribution of scores voor {sequence} met {iterations} iteraties')
    plt.xlabel('Score')
    plt.ylabel('Frequency')
    plt.show()

# Voorbeeldgebruik
string = "HHPHHHPH"
run_multiple_random_foldings(string)
#random_folding(string)
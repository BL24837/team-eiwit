from aminoacid import *
from board import *
from protein import *
import random
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
    return int(protein.board.score)

def exhaustive_folding(sequence):
    protein = ProteinState(sequence)
    solutions = []

    def backtrack(index):
        if index == len(sequence):
            solutions.append((protein.board.score, protein.board.grid.copy(), protein.board.positions.copy()))
            return

        current_aa_type = sequence[index]
        for dx, dy in protein.get_valid_moves():
            last_x, last_y = protein.board.positions[-1]
            new_pos = (last_x + dx, last_y + dy)

            if not protein.board.is_occupied(new_pos):
                new_aa = AminoAcid(current_aa_type, new_pos)
                protein.board.place_amino_acid(new_aa)
                protein.board.update_score(new_aa)
                backtrack(index + 1)
                protein.board.grid.pop(new_pos)
                protein.board.positions.pop()
                protein.board.score -= abs(new_aa.get_bond_strength(new_aa))

    backtrack(1)
    best_solution = min(solutions, key=lambda x: x[0])
    protein.board.grid = best_solution[1]
    protein.board.positions = best_solution[2]
    print(f"Number of solutions: {len(solutions)}")
    #print(f"Best solution score: {best_solution[0]}") # WERKT NIET
    protein.board.plot_board()

# Example usage:
string = "HPHPPHHPHPPHPHHPPHPH"
exhaustive_folding(string)

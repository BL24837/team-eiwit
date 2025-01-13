from code.classes.protein import Protein
from code.visualisation.board import *
from code.classes.visualize import Visualize
from code.classes.utils import utils
from code.classes.grid import *

def fold_protein(sequence):
    protein = Protein(sequence)
    x, y = 0, 0
    for amino in protein.sequence:
        protein.place_on_grid(x, y, amino)
        x += 1  
    protein.calculate_score()
    return protein

if __name__ == "__main__":

    sequences = utils.read_sequences(f"data/sequences.csv")
    

    for seq_data in sequences:
        protein = fold_protein(seq_data['sequence'])
        print(f"Protein ID: {seq_data['id']}")
        print(f"Sequence: {seq_data['sequence']}")
        print(f"Score: {protein.score}")
        print("Structure:")
        protein.print_structure()
        print("---")
        Visualize.visualize_protein(protein)

        for seq_data in sequences:
            protein = fold_protein(seq_data['sequence'])
            output_file = f"results/output.csv"
            utils.export_results_to_csv(protein, output_file)
            print(f"Results for {seq_data['id']} written to {output_file}")
            break
        break

def fold_protein(sequence):
    protein = Protein(sequence)
    x, y = 0, 0
    for amino in protein.sequence:
        protein.place_on_grid(x, y, amino)
        x += 1  
    protein.calculate_score()
    return protein

if __name__ == "__main__":
    sequences = read_sequences('sequences.csv')
    

    for seq_data in sequences:
        protein = fold_protein(seq_data['sequence'])
        print(f"Protein ID: {seq_data['id']}")
        print(f"Sequence: {seq_data['sequence']}")
        print(f"Score: {protein.score}")
        print("Structure:")
        protein.print_structure()
        print("---")
        visualize_protein(protein)

        for seq_data in sequences:
            protein = fold_protein(seq_data['sequence'])
            output_file = f"output.csv"
            export_results_to_csv(protein, output_file)
            print(f"Results for {seq_data['id']} written to {output_file}")
            break
        break

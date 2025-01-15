# random fold algoritme
def random_fold_protein(sequence):
    protein = Protein(sequence)
    x, y = 0, 0
    protein.place_on_grid(x, y, protein.sequence[0])  # Startpositie

    for amino_acid in protein.sequence[1:]:
        valid_move = False
        while not valid_move:
            move = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])  # Random richting kiezen
            new_x, new_y = x + move[0], y + move[1]

            if (new_x, new_y) not in protein.grid:
                protein.place_on_grid(new_x, new_y, amino_acid)
                x, y = new_x, new_y
                valid_move = True

    protein.calculate_score()
    return protein
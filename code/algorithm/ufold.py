# Splits de string op in 2 delen zodoende dat 
# de helft van de H's in EVEN(S) in deel 1 zit 
# en de helft van de H's in ODD(S) in deel 2.
# S[i] = 1 als aminoacid is H
# EVEN(S) = {i: i is even en S[i] = 1}
# ODD(S) = {i: is oneven en S[i] = 1}

def u_fold_algorithm(sequence):
    protein = Protein(sequence)
    x, y = 0, 0
    protein.place_on_grid(x, y, protein.sequence[0])  # Startpositie
    midden = len(protein.sequence) // 2
    prefix = protein.sequence[:midden]
    suffix = protein.sequence[midden:]






    for i in range(len(EVEN)):
        if i % 2 == 0:
            deel1.append(EVEN[i])
        else:
            deel2.append(EVEN[i])
    for i in range(len(ODD)):
        if i % 2 == 0:
            deel1.append(ODD[i])
        else:
            deel2.append(EVEN[i])

    


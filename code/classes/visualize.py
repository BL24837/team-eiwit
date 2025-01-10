import matplotlib.pyplot as plt

def visualize_protein(protein):
    
    x_coords = []
    y_coords = []
    colors = []
    labels = {'H': 'red', 'P': 'blue', 'C': 'green'}

    for (x, y), amino_acid in protein.grid.items():
        x_coords.append(x)
        y_coords.append(y)
        colors.append(labels[amino_acid.type])  
    
    plt.figure(figsize=(8, 8))
    plt.scatter(x_coords, y_coords, c=colors, s=100, zorder=2)

    for i in range(len(x_coords) - 1):
        plt.plot(
            [x_coords[i], x_coords[i + 1]],
            [y_coords[i], y_coords[i + 1]],
            'k-', zorder=1
        )

    plt.title("Protein Folding Visualization")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.grid(True)
    plt.axis('equal')  # Ensure grid squares are equal
    plt.show()

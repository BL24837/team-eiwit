
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

class ProteinVisualizer:
    def __init__(self, protein):
        self.protein = protein

    def display(self, return_figure=False):
        """
        Visualize the 3D structure of the protein using matplotlib.
        """
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        # Extract positions and types
        positions = np.array([aa["position"] for aa in self.protein.amino_acids])
        types = [aa["type"] for aa in self.protein.amino_acids]

        # Map amino acid types to colors
        color_map = {"H": "red", "P": "blue","C": "green"}
        colors = [color_map.get(t, "gray") for t in types]

        # Plot the positions
        for i, (pos, color) in enumerate(zip(positions, colors)):
            ax.scatter(pos[0], pos[1], pos[2], color=color, s=100, label=f"{types[i]}" if i == 0 else "")

        # Connect the points to form the protein chain
        for i in range(len(positions) - 1):
            ax.plot(
                [positions[i][0], positions[i + 1][0]],
                [positions[i][1], positions[i + 1][1]],
                [positions[i][2], positions[i + 1][2]],
                color="black"
            )

        # Set labels and title
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")
        ax.set_title("3D Visualization of Protein Structure")

        x_min, x_max = positions[:, 0].min(), positions[:, 0].max()
        y_min, y_max = positions[:, 1].min(), positions[:, 1].max()
        z_min, z_max = positions[:, 2].min(), positions[:, 2].max()

        max_range = max(x_max - x_min, y_max - y_min, z_max - z_min)
        ax.set_xlim(x_min, x_min + max_range)
        ax.set_ylim(y_min, y_min + max_range)
        ax.set_zlim(z_min, z_min + max_range)

        ax.set_xticks(np.arange(x_min, x_min + max_range + 1, 1))
        ax.set_yticks(np.arange(y_min, y_min + max_range + 1, 1))
        ax.set_zticks(np.arange(z_min, z_min + max_range + 1, 1))
        ax.grid(True)
        
        plt.legend()
        

        if return_figure:
            return fig, ax
        else:
            plt.show()

    

import numpy as np

class Protein:
    def __init__(self, sequence=None):
        self.sequence = sequence
        self.amino_acids = []  # List to hold amino acid information
        self.initialize_protein_structure()

    def initialize_protein_structure(self):
        """
        Initializes the protein structure with default positions in 3D space.
        """
        if self.sequence:
            for index, amino_acid in enumerate(self.sequence):
                self.amino_acids.append({
                    "type": amino_acid,
                    "position": np.array([index, 0, 0]),
                    "index": index
                })

    def calculate_neighbors(self, position):
        """
        Calculate the neighbor positions in 3D space for a given position.
        """
        offsets = np.array([
            [0, 1, 0], [1, 0, 0], [0, 0, 1],  # Positive directions
            [0, -1, 0], [-1, 0, 0], [0, 0, -1]  # Negative directions
        ])
        return [position + offset for offset in offsets]

    def calculate_stability(self):
        """
        Calculate the stability score of the protein structure.
        """
        stability_score = 0
        for amino_acid in self.amino_acids:
            if amino_acid["type"] in ["H", "C"]:
                neighbors = self.calculate_neighbors(amino_acid["position"])
                for neighbor in neighbors:
                    for other in self.amino_acids:
                        if np.array_equal(other["position"], neighbor):
                            if abs(amino_acid["index"] - other["index"]) > 1:
                                bond_score = self.calculate_bond_score(
                                    amino_acid["type"], other["type"])
                                stability_score += bond_score
        return stability_score // 2

    def calculate_bond_score(self, type1, type2):
        """
        Calculate the bond score between two amino acid types.
        """
        if {type1, type2} == {"H"} or {type1, type2} == {"C", "H"}:
            return -1
        elif {type1, type2} == {"C"}:
            return -5
        return 0

    def rotate_amino_acid(self, amino_index, pivot_index, rotation_matrix):
        """
        Rotates an amino acid around a pivot using the specified rotation matrix.
        """
        pivot_position = self.amino_acids[pivot_index]["position"]
        relative_position = self.amino_acids[amino_index]["position"] - pivot_position
        rotated_position = np.dot(rotation_matrix, relative_position)
        self.amino_acids[amino_index]["position"] = rotated_position + pivot_position

    def rotate_protein(self, pivot_index, rotation_matrix):
        """
        Rotates the whole protein around a pivot using the specified rotation matrix.
        """
        for i in range(pivot_index + 1, len(self.amino_acids)):
            self.rotate_amino_acid(i, pivot_index, rotation_matrix)

    def find_valid_rotations(self, pivot_index):
        """
        Find valid rotation options for a pivot point.
        """
        valid_rotations = []
        rotation_matrices = self.get_rotation_matrices()
        for label, matrix in rotation_matrices.items():
            if self.is_rotation_valid(pivot_index, matrix):
                valid_rotations.append(label)
        return valid_rotations

    def is_rotation_valid(self, pivot_index, rotation_matrix):
        """
        Check if a rotation is valid for a given pivot and rotation matrix.
        """
        pivot_position = self.amino_acids[pivot_index]["position"]
        for amino_acid in self.amino_acids:
            if amino_acid["index"] > pivot_index:
                original_position = amino_acid["position"]
                relative_position = original_position - pivot_position
                rotated_position = np.dot(rotation_matrix, relative_position) + pivot_position
                if any(
                    np.array_equal(rotated_position, other["position"])
                    for other in self.amino_acids
                ):
                    return False
        return True

    def get_rotation_matrices(self):
        """
        Define and return rotation matrices for all possible directions.
        """
        return {
            "x_positive": np.array([[1, 0, 0], [0, 0, 1], [0, -1, 0]]),
            "x_negative": np.array([[1, 0, 0], [0, 0, -1], [0, 1, 0]]),
            "y_positive": np.array([[0, 0, -1], [0, 1, 0], [1, 0, 0]]),
            "y_negative": np.array([[0, 0, 1], [0, 1, 0], [-1, 0, 0]]),
            "z_positive": np.array([[0, -1, 0], [1, 0, 0], [0, 0, 1]]),
            "z_negative": np.array([[0, 1, 0], [-1, 0, 0], [0, 0, 1]])
        }
    
    def copy(self):
        new_protein = Protein(self.sequence)
        new_protein.amino_acids = self.amino_acids.copy()  # Maak een kopie van de lijst
        return new_protein

# Example usage
sequence = "HCHHCHC"
protein = Protein(sequence)
print("Stability:", protein.calculate_stability())

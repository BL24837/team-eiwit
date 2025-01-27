import numpy as np

class Protein:
    """
    Represents a protein structure and provides methods for manipulation,
    rotation, and stability calculation in a 3D space.
    """

    def __init__(self, sequence: str = None):
        """
        Initializes the protein object.

        Args:
            sequence (str): The protein sequence consisting of amino acids.
        """
        self.sequence = sequence
        self.amino_acids = []  # Stores amino acid positions and types
        self.initialize_protein_structure()

    def initialize_protein_structure(self) -> None:
        """
        Initializes the protein structure with default positions in 3D space.
        Each amino acid is placed along the x-axis initially.
        """
        if self.sequence:
            for index, amino_acid in enumerate(self.sequence):
                self.amino_acids.append({
                    "type": amino_acid,
                    "position": np.array([index, 0, 0]),
                    "index": index
                })

    def calculate_neighbors(self, position: np.ndarray) -> list:
        """
        Calculate the neighbor positions in 3D space for a given position.

        Args:
            position (np.array): The position of the amino acid.

        Returns:
            list: List of neighboring positions in 3D space.
        """
        offsets = np.array([
            [0, 1, 0], [1, 0, 0], [0, 0, 1],  # Positive directions
            [0, -1, 0], [-1, 0, 0], [0, 0, -1]  # Negative directions
        ])
        return [position + offset for offset in offsets]

    def calculate_stability(self) -> int:
        """
        Calculate the stability score of the protein structure.
        Bonds between hydrophobic (H) and/or cysteine (C) amino acids contribute
        to the stability score.

        Returns:
            int: The total stability score of the protein.
        """
        stability_score = 0
        for amino_acid in self.amino_acids:
            if amino_acid["type"] in ["H", "C"]:
                neighbors = self.calculate_neighbors(amino_acid["position"])
                for neighbor in neighbors:
                    for other in self.amino_acids:
                        if np.array_equal(other["position"], neighbor):
                            # Exclude bonds between adjacent amino acids in the sequence
                            if abs(amino_acid["index"] - other["index"]) > 1:
                                bond_score = self.calculate_bond_score(
                                    amino_acid["type"], other["type"]
                                )
                                stability_score += bond_score
        return stability_score // 2  # Each bond is counted twice, so divide by 2

    def calculate_bond_score(self, type1: str, type2: str) -> int:
        """
        Calculate the bond score between two amino acid types.

        Args:
            type1 (str): Type of the first amino acid.
            type2 (str): Type of the second amino acid.

        Returns:
            int: Bond score based on the types of amino acids.
        """
        if {type1, type2} == {"H"} or {type1, type2} == {"C", "H"}:
            return -1
        elif {type1, type2} == {"C"}:
            return -5
        return 0

    def rotate_amino_acid(self, amino_index: int, pivot_index: int, rotation_matrix: np.ndarray) -> None:
        """
        Rotates a single amino acid around a pivot using a rotation matrix.

        Args:
            amino_index (int): Index of the amino acid to rotate.
            pivot_index (int): Index of the pivot amino acid.
            rotation_matrix (np.array): Rotation matrix to apply.
        """
        pivot_position = self.amino_acids[pivot_index]["position"]
        relative_position = self.amino_acids[amino_index]["position"] - pivot_position
        rotated_position = np.dot(rotation_matrix, relative_position)
        self.amino_acids[amino_index]["position"] = rotated_position + pivot_position

    def rotate_protein(self, pivot_index: int, rotation_matrix: np.ndarray) -> None:
        """
        Rotates the entire protein around a pivot point.

        Args:
            pivot_index (int): Index of the pivot amino acid.
            rotation_matrix (np.array): Rotation matrix to apply.
        """
        for i in range(pivot_index + 1, len(self.amino_acids)):
            self.rotate_amino_acid(i, pivot_index, rotation_matrix)

    def find_valid_rotations(self, pivot_index: int) -> list:
        """
        Finds all valid rotations for a given pivot point.

        Args:
            pivot_index (int): Index of the pivot amino acid.

        Returns:
            list: List of valid rotation labels.
        """
        valid_rotations = []
        rotation_matrices = self.get_rotation_matrices()
        for label, matrix in rotation_matrices.items():
            if self.is_rotation_valid(pivot_index, matrix):
                valid_rotations.append(label)
        return valid_rotations

    def is_rotation_valid(self, pivot_index: int, rotation_matrix: np.ndarray) -> bool:
        """
        Checks if a rotation is valid for a given pivot and rotation matrix.

        Args:
            pivot_index (int): Index of the pivot amino acid.
            rotation_matrix (np.array): Rotation matrix to validate.

        Returns:
            bool: True if the rotation is valid, False otherwise.
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

    def get_rotation_matrices(self) -> dict:
        """
        Returns predefined rotation matrices for x, y, and z axes.

        Returns:
            dict: Dictionary of rotation matrices with labels.
        """
        return {
            "x_positive": np.array([[1, 0, 0], [0, 0, 1], [0, -1, 0]]),
            "x_negative": np.array([[1, 0, 0], [0, 0, -1], [0, 1, 0]]),
            "y_positive": np.array([[0, 0, -1], [0, 1, 0], [1, 0, 0]]),
            "y_negative": np.array([[0, 0, 1], [0, 1, 0], [-1, 0, 0]]),
            "z_positive": np.array([[0, -1, 0], [1, 0, 0], [0, 0, 1]]),
            "z_negative": np.array([[0, 1, 0], [-1, 0, 0], [0, 0, 1]])
        }

    def copy(self) -> "Protein":
        """
        Creates a copy of the protein object.

        Returns:
            Protein: A copy of the current protein object.
        """
        new_protein = Protein(self.sequence)
        new_protein.amino_acids = self.amino_acids.copy()
        return new_protein

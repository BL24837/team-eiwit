from aminoacid import *
from board import *
import time
import random

class ProteinState:
    def __init__(self, sequence):
        self.sequence = sequence
        self.board = Board()
        self.board.place_amino_acid(AminoAcid(sequence[0], (0, 0)))

    def get_valid_moves(self):
        last_x, last_y = self.board.positions[-1]
        directions = [
            (1, 0),   # Rechts
            (-1, 0),  # Links
            (0, 1),   # Omhoog
            (0, -1)   # Omlaag
        ]
        return directions

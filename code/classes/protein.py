from protein import Board

class Aminozuur:
    def __init__(self, type: str, index: int, position: ):
        self.amino_type = type
        self.index = index
        self.position = position

    def get_score_stabiliteit(self, other):
        if self.amino_type == "H" and other.amino_type == "H":
            return -1
        elif self.amino_type == "C" and other.amino_type == "C":
            return -5
        elif (self.amino_type == "C" and other.amino_type == "H") or (self.amino_type == "H" and other.amino_type == "C"):
            return -1
        return 0

class Eiwit:
    def __init__(self, sequence: str):
        self.sequence = sequence
        self.board = Board()
        self.aminozuren = []
        self.best_stabillity = float()
        self.best_board = None

    def get_valid_moves(self):
        
        directions = [
            (1, 0),
            (-1, 0),
            (0, 1),
            (0, -1)
        ]

        return directions


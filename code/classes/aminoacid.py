

class AminoAcid:
    def __init__(self, type):
        self.type = type  # 'H', 'P', or 'C'
        self.coordinates = [0, 0, 0]

    def __repr__(self):
        return f"AminoAcid(type='{self.type}')"

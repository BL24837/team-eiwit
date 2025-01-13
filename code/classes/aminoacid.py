
class AminoAcid:
    def __init__(self, type_):
        self.type = type_  # 'H', 'P', or 'C'

    def __repr__(self):
        return f"AminoAcid(type='{self.type}')"

class AminoAcid:
    def __init__(self, amino_type, position):
        self.amino_type = amino_type
        self.position = position

    def get_bond_strength(self, other):
        if self.amino_type == 'H' and other.amino_type == 'H':
            return -1
        elif self.amino_type == 'C' and other.amino_type == 'C':
            return -5
        elif ('C' in (self.amino_type, other.amino_type)) and ('H' in (self.amino_type, other.amino_type)):
            return -1
        return 0
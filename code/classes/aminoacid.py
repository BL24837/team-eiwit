class AminoAcid:
    def __init__(self, type_: str, index_: int, x: int, y: int, z:int):
        self.type = type_
        self.index = index_
        self.position = (x, y, z)

    def add_neighbour(self, aminoacid):
        self.neighbours[aminoacid.index] = aminoacid
   
    def __repr__(self):
        return f"AminoAcid(type='{self.type}')"

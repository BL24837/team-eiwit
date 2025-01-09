

class Aminozuur:
    def __init__(self):
        self.amino_type = # H, C, P;
        self.index = # plaatst in sequentie;
        self.x = # x coordinaat;
        self.y = # y coordinaat;

    def get_score_stabiliteit(self, other):
        if self.amino_type == "H" and other.amino_type == "H":
            return -1
        elif self.amino_type == "C" and other.amino_type == "C":
            return -5
        elif (self.amino_type == "C" and other.amino_type == "H") or (self.amino_type == "H" and other.amino_type == "C"):
            return -1
        return 0

class Eiwit:
    def __init__(self):
        self.sequentie = ;
        self.aminozuren = []
        self.grid_size = #lengte van de sequentie alle kanten op;



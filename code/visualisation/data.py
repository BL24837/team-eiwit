
class Data():
    def __init__(self, protein):
        self.protein = protein

    def get_movement_directions(self):
        """
        Calculates movement directions based on positions of consecutive amino acids.
        """
        directions = []
        for i in range(1, len(self.protein.amino_acids)):
            delta = self.protein.amino_acids[i]["position"] - self.protein.amino_acids[i - 1]["position"]
            if delta[0] != 0:
                directions.append(int(delta[0]))
            elif delta[1] != 0:
                directions.append(int(delta[1]) * 2)
            elif delta[2] != 0:
                directions.append(int(delta[2]) * 3)
        return directions

    def generate_output(self, score):
        """
        Generates the formatted output for the protein.
        :param score: The score to display in the output.
        """
        directions = self.get_movement_directions()
        output = []

        # Add header
        output.append(f"HEADER score: {score}")

        # Add amino acid information
        for i, amino_acid in enumerate(self.protein.amino_acids):
            # Het eerste element krijgt een beweging vanuit directions
            if i == 0:
                movement = directions[0] if directions else 0
            # Het laatste element heeft geen beweging
            elif i == len(self.protein.amino_acids) - 1:
                movement = 0
            # Alle andere elementen krijgen beweging vanuit directions
            else:
                movement = directions[i - 1]
            output.append(f"{amino_acid['type']}, {movement}")

        # Add footer
        output.append(f"FOOTER score: {score}")

        return "\n".join(output)
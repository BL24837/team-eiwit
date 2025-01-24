import csv
import os
import re

class DataStoring:
    def __init__(self, 
                 algorithm: str = None, 
                 parameters: dict = None, 
                 best_protein: object = None, 
                 filename: str = None):
        self.csv_directory = os.path.join(os.path.dirname(__file__), '../..', 'results')
        self.algorithm = algorithm
        self.filename = filename
        self.parameters = parameters
        self.protein = best_protein

    def beam_search_data(self, protein, score, elapsed_time):
        """
        Schrijft de gegenereerde output en elapsed_time naar de CSV-bestand.
        """
        self.protein = protein  # Set de huidige protein
        full_path = self.get_path()  # Verkrijg het pad naar de CSV-bestand

        # Genereer de output van generate_output
        output = self.generate_output(score)

        # Voeg elapsed_time toe aan het output
        output += f"\nTIME elapsed: {elapsed_time:.2f} seconds"

        # Zorg dat de output wordt toegevoegd aan de CSV zonder de huidige inhoud te overschrijven
        with open(full_path, mode='a', newline='') as csv_file:
            csv_file.write("\n")  # Voeg een lege regel toe om data te scheiden
            csv_file.write(output)  # Schrijf de gegenereerde output naar de CSV
            csv_file.write("\n")  
  
    def get_path(self):  
        # Controleer of de bestandsnaam geldig is
        if not self.filename or not self.filename.endswith('.csv'):
            raise ValueError("Geef een bestandsnaam op met de extensie '.csv'.")
        
        # Construeer het volledige pad naar het bestand
        full_path = os.path.join(self.csv_directory, self.filename)

        # Controleer of het bestand bestaat
        if not os.path.isfile(full_path):
            raise FileNotFoundError(f"Het bestand '{full_path}' bestaat niet.")
        
        print(f"Bestand gevonden: {full_path}")
        return full_path
    
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


    






if __name__ == "__main__":
    # Voeg de extensie toe aan de bestandsnaam
    filename = "exp1.csv"  # Zorg ervoor dat dit een .csv-bestand is
    data = DataStoring(filename=filename)
    
    try:
        # Roep de execute-methode aan
        file_path = data.execute()
        print(f"Het geselecteerde bestand is: {file_path}")
    except (ValueError, FileNotFoundError) as e:
        print(f"Fout: {e}")
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
    
    def ensure_csv_headers(self):
        """
        Controleer of de CSV-bestand een header bevat en voeg deze toe indien niet aanwezig.
        """
        full_path = self.get_path()

        # Controleer of het bestand leeg is of headers mist
        if not os.path.isfile(full_path) or os.stat(full_path).st_size == 0:
            with open(full_path, mode='w', newline='') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(['Run', 'Execution Time (s)', 'Stability', 'Protein Folding Sequence'])
                print(f"Headers toegevoegd aan bestand: {full_path}")

    def simulatedannealing(self, data):
        """
        Schrijft de resultaten van Simulated Annealing naar de CSV-bestand.
        """
        full_path = self.get_path()

        # Voeg een lege regel toe voordat we de resultaten toevoegen
        with open(full_path, mode='a', newline='') as csv_file:
            print('Run', 'Execution Time (s)', 'Stability', 'Protein Folding Sequence')
            csv_file.write("\n")  # Voeg een lege regel toe om data te scheiden
            
            # Voeg de resultaten toe aan het bestand
            for entry in data:
                csv_file.write(entry + "\n")

    def greedy_algorithm(self, run, execution_time, stability, folding_sequence):
        """
        Schrijft de resultaten van het Greedy Algorithm naar de CSV-bestand.
        
        :param run: De nummer van de huidige run.
        :param execution_time: De tijd die de run heeft geduurd.
        :param stability: De stabiliteitsscore van de run.
        :param folding_sequence: De vouwingssequentie van het eiwit.
        """
        full_path = self.get_path()

        # Controleer of de CSV een header nodig heeft
        self.ensure_csv_headers()

        # Voeg de gegevens toe aan het bestand
        with open(full_path, mode='a', newline='') as csv_file:
            print('Run', 'Execution Time (s)', 'Stability', 'Protein Folding Sequence')
            writer = csv.writer(csv_file)
            writer.writerow([run, execution_time, stability, folding_sequence])

        print(f"Run {run}: Time={execution_time:.2f}s, Stability={stability}, Sequence={folding_sequence}")
    

    def random_folding(self, iteration, stability):
        """
        Schrijft de resultaten van Random Folding naar de CSV-bestand.

        :param iteration: Het nummer van de huidige iteratie.
        :param stability: De stabiliteitsscore van de huidige iteratie.
        """
        full_path = self.get_path()

        # Controleer of de CSV een header nodig heeft en voeg deze toe als dat nodig is
        if not os.path.isfile(full_path) or os.stat(full_path).st_size == 0:
            with open(full_path, mode='w', newline='') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(['Iteration', 'Stability'])  # Header toevoegen
                print(f"Headers toegevoegd aan bestand: {full_path}")

        # Voeg de gegevens van de huidige iteratie toe aan het CSV-bestand
        with open(full_path, mode='a', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow([iteration, stability])

        print(f"Iteration {iteration}: Stability={stability} toegevoegd aan {full_path}")


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
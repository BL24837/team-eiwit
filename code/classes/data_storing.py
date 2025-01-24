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
        self.best_protein = best_protein

    def execute(self):
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

    def 


    



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
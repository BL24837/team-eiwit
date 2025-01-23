import csv, os, re

class DataStoring:
    def __init__(self, 
                 sequence:str=None,
                 dimension:str=None, 
                 algorithm:str=None, 
                 parameters:dict=None, 
                 best_protein:object=None, 
                 stabillities:list=None, 
                 filename:str=None):
        self.csv_directory = os.path.join(os.path.dirname(__file__), '../..', 'results', dimension, algorithm, sequence)
        self.dimension = dimension
        self.algorithm = algorithm
        self.filename = filename
        self.parameters = parameters
        self.best_protein = best_protein
        self.stabillities = stabillities
        self.execute()

    def execute(self):
        print(self.filename)
        if not self.filename:
            print("No filename provided. Creating a new CSV file.")
            self.make_csv_name()
        
    def make_csv_name(self):
        """
        Generates a unique filename and creates the CSV file if it doesn't exist.
        """
        csv_files = [f for f in os.listdir(self.csv_directory) if f.endswith('.csv')]

        max_num = 0
        for file in csv_files:
            match = re.search(r'exp(\d+)', file)
            if match:
                num = int(match.group(1))
                max_num = max(max_num, num)

        self.filename = f"exp{max_num + 1}.csv"

        filepath = os.path.join(self.csv_directory, self.filename)
        filepath = os.path.join(self.csv_directory, self.filename)
        if not os.path.exists(filepath):
            with open(filepath, 'w', newline='') as csvfile:
                pass 
    
    def create_csv(self):

        return 
    def save_to_csv(self):
        with open(self.filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([self.parameters, self.best_protein, self.stabillities])



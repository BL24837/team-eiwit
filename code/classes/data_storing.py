import csv
import os
import re

class DataStoring:
    """
    Handles the storage of protein folding results in CSV format and provides
    utility methods for generating output, handling files, and recording data
    from various algorithms.
    """

    def __init__(self, 
                 algorithm: str = None, 
                 parameters: dict = None, 
                 best_protein: object = None, 
                 filename: str = None):
        """
        Initializes the DataStoring object.

        Args:
            algorithm (str): Name of the algorithm used.
            parameters (dict): Parameters used for the algorithm.
            best_protein (Protein): The best protein structure found.
            filename (str): The CSV filename where data will be stored.
        """
        self.csv_directory = os.path.join(os.path.dirname(__file__), '../..', 'results')
        self.algorithm = algorithm
        self.filename = filename
        self.parameters = parameters
        self.protein = best_protein
    
    def ensure_csv_headers(self) -> None:
        """
        Ensures the CSV file contains the appropriate headers.
        Adds headers if the file does not exist or is empty.
        """
        full_path = self.get_path()

        if not os.path.isfile(full_path) or os.stat(full_path).st_size == 0:
            with open(full_path, mode='w', newline='') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(['Run', 'Execution Time (s)', 'Stability', 'Protein Folding Sequence'])
                print(f"Headers added to file: {full_path}")

    def log_beam_search(self, beam_data: list[tuple[int, float, float]]) -> None:
        """
        Logs data from multiple Beam Search runs into a CSV file.

        Args:
            beam_data (list): A list of tuples (beam_width, elapsed_time, stability).
        """
        filepath = self.get_path()
        self.ensure_csv_headers()

        with open(filepath, mode='a', newline='') as csv_file:
            writer = csv.writer(csv_file)
            for beam_width, elapsed_time, stability in beam_data:
                writer.writerow([beam_width, stability, elapsed_time])

    def simulatedannealing(self, data: list[str]) -> None:
        """
        Writes Simulated Annealing results to the CSV file.

        Args:
            data (list): List of results to be written to the file.
        """
        full_path = self.get_path()

        with open(full_path, mode='a', newline='') as csv_file:
            csv_file.write("\n")  # Add a blank line for separation
            for entry in data:
                csv_file.write(entry + "\n")

    def greedy_algorithm(self, run: int, execution_time: float, stability: float, folding_sequence: str) -> None:
        """
        Writes the results of the Greedy Algorithm to the CSV file.

        Args:
            run (int): The current run number.
            execution_time (float): The time taken for the run.
            stability (float): The stability score of the run.
            folding_sequence (str): The protein folding sequence.
        """
        full_path = self.get_path()
        self.ensure_csv_headers()

        with open(full_path, mode='a', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow([run, execution_time, stability, folding_sequence])
        print(f"Run {run}: Time={execution_time:.2f}s, Stability={stability}, Sequence={folding_sequence}")
    
    def random_folding(self, iteration: int, stability: float) -> None:
        """
        Writes Random Folding results to the CSV file.

        Args:
            iteration (int): The current iteration number.
            stability (float): The stability score for the iteration.
        """
        full_path = self.get_path()
        self.ensure_csv_headers()

        with open(full_path, mode='a', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow([iteration, stability])
        print(f"Iteration {iteration}: Stability={stability} added to {full_path}")

    def beam_search_data(self, protein: object, score: float, elapsed_time: float) -> None:
        """
        Writes Beam Search results and elapsed time to the CSV file.

        Args:
            protein (Protein): The protein configuration.
            score (float): Stability score of the configuration.
            elapsed_time (float): Time taken to execute the algorithm.
        """
        self.protein = protein
        full_path = self.get_path()
        output = self.generate_output(score)
        output += f"\nTIME elapsed: {elapsed_time:.2f} seconds"

        with open(full_path, mode='a', newline='') as csv_file:
            csv_file.write("\n")
            csv_file.write(output)
            csv_file.write("\n")
  
    def get_path(self) -> str:
        """
        Constructs the full path for the CSV file.

        Returns:
            str: Full path to the CSV file.

        Raises:
            ValueError: If the filename is invalid.
            FileNotFoundError: If the file does not exist.
        """
        if not self.filename or not self.filename.endswith('.csv'):
            raise ValueError("Filename must have a '.csv' extension.")
        
        full_path = os.path.join(self.csv_directory, self.filename)

        if not os.path.isfile(full_path):
            raise FileNotFoundError(f"File '{full_path}' does not exist.")
        
        print(f"File found: {full_path}")
        return full_path
    
    def get_movement_directions(self) -> list[int]:
        """
        Calculates movement directions based on positions of consecutive amino acids.

        Returns:
            list[int]: List of movement directions for the protein.
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

    def generate_output(self, score: float) -> str:
        """
        Generates formatted output for the protein configuration.

        Args:
            score (float): Stability score of the protein.

        Returns:
            str: Formatted string with protein data.
        """
        directions = self.get_movement_directions()
        output = [f"HEADER score: {score}"]

        for i, amino_acid in enumerate(self.protein.amino_acids):
            if i == 0:
                movement = directions[0] if directions else 0
            elif i == len(self.protein.amino_acids) - 1:
                movement = 0
            else:
                movement = directions[i - 1]
            output.append(f"{amino_acid['type']}, {movement}")
        output.append(f"FOOTER score: {score}")
        return "\n".join(output)

if __name__ == "__main__":
    filename = "exp1.csv"
    data = DataStoring(filename=filename)
    
    try:
        file_path = data.get_path()
        print(f"Selected file: {file_path}")
    except (ValueError, FileNotFoundError) as e:
        print(f"Error: {e}")

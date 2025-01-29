import os
import csv
from typing import Optional

class CsvFunctions:
    """
    A class that provides utility functions for handling CSV files related to protein folding simulations.
    """
    
    def __init__(self):
        pass
    
    def csv_header(self, raw_filepath: str, choice: int) -> None:
        """
        Ensures the correct header is present in the specified CSV file.
        If the file does not exist, it is created with the appropriate header.
        
        Args:
            raw_filepath (str): The path to the CSV file.
            choice (int): The algorithm type indicator (1-5).
        """
        if os.path.isfile(raw_filepath):
            # Check if the file already has a header
            with open(raw_filepath, mode='r') as f:
                existing_data = f.readlines()
                if len(existing_data) == 0 or not existing_data[0].strip().startswith("Iteration"):
                    # Add the appropriate header
                    temp_data = existing_data[:]
                    with open(raw_filepath, mode='w', newline='') as fw:
                        writer = csv.writer(fw)
                        if choice == 5:  # Simulated Annealing
                            writer.writerow(['Iteration', 'Stability', 'Temperature'])
                        elif choice == 3:  # Greedy Algorithm
                            writer.writerow(['Iteration', 'Stability'])
                        elif choice == 1:  # Random Folding
                            writer.writerow(['Iteration', 'Stability'])
                        elif choice == 4:  # Beam Search Folding
                            writer.writerow(['Beam Width', 'Stability', 'Elapsed Time'])
                        elif choice == 2:  # Beam Search Folding
                            writer.writerow(['Iteration', 'Stability'])
                        fw.writelines(temp_data)  # Rewriting the existing data
        else:
            # Create the file and write the header
            with open(raw_filepath, mode='w', newline='') as f:
                writer = csv.writer(f)
                if choice == 5:  # Simulated Annealing
                    writer.writerow(['Iteration', 'Stability', 'Temperature'])
                elif choice == 3:  # Greedy Algorithm
                    writer.writerow(['Iteration', 'Stability'])
                elif choice == 1:  # Random Algorithm
                    writer.writerow(['Iteration', 'Stability'])
                elif choice == 4:  # Beam Search Folding
                    writer.writerow(['Beam Width', 'Stability', 'Elapsed Time'])
                elif choice == 2:  # Hill Climber Algorithm
                    writer.writerow(['Iteration', 'Stability'])
    
    def csv_header_summary(self, summary_filepath: str, choice: int) -> None:
        """
        Creates a CSV summary file with an appropriate header if it does not exist.
        
        Args:
            summary_filepath (str): The path to the summary CSV file.
            choice (int): The algorithm type indicator.
        """
        if not os.path.isfile(summary_filepath):
            with open(summary_filepath, mode='w', newline='') as f:
                writer = csv.writer(f)
                if choice == 4:
                    writer.writerow(['Beam Width', 'Elapsed Time (s)', 'Stability', 'Protein Folding Sequence'])
                else:
                    writer.writerow(['Run', 'Execution Time (s)', 'Stability', 'Protein Folding Sequence'])
    
    def csv_summary(
        self, 
        summary_filepath: str, 
        current_stability: float, 
        sequence_protein: str, 
        run_count: int, 
        execution_time: float
    ) -> None:
        """
        Appends summary data to the summary CSV file.
        
        Args:
            summary_filepath (str): The path to the summary CSV file.
            current_stability (float): The stability value of the protein fold.
            sequence_protein (str): The protein sequence used in the simulation.
            run_count (int): The run iteration number.
            execution_time (float): The time taken for execution in seconds.
        """
        with open(summary_filepath, mode='a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([run_count + 1, execution_time, current_stability, sequence_protein])

import numpy as np
import matplotlib.pyplot as plt
import os
import csv

class Distribution:
    """
    Class for visualizing the distribution of stability over different iterations.
    """
    
    def __init__(self, stabilities: list[float] = None):
        """
        Initializes the Distribution class.
        
        Args:
            stabilities (list[float], optional): List of stability values. Defaults to None.
        """
        self.stabilities = stabilities

    def visualize_stability_distribution_from_results(self, filename: str) -> None:
        """
        Creates a distribution plot of stability based on data from the second column of a CSV file
        and saves it as a PNG file in the 'results/distribution' directory.

        Args:
            filename (str): Name of the CSV file located in the 'results' directory.
        """
        # Ensure the 'results/distribution' directory exists
        distribution_dir = os.path.join("results", "distribution")
        if not os.path.exists(distribution_dir):
            os.makedirs(distribution_dir)

        # Path to the file
        filepath = os.path.join("results", filename)
        print(f"Processing file: {filepath}")
        
        try:
            # Read the CSV file
            stabilities = []
            with open(filepath, mode='r') as csvfile:
                reader = csv.reader(csvfile)
                next(reader)  # Skip header if present
                for row in reader:
                    if len(row) > 1:  # Ensure there is a second column
                        try:
                            stability = float(row[1])  # Extract stability value
                            stabilities.append(stability)
                        except ValueError:
                            continue  # Skip rows with invalid values
            
            # Check if stability data is available
            if not stabilities:
                print(f"No stability data found in {filename}.")
                return
            
            # Set stability data for plotting
            self.stabilities = stabilities
            
            # Plot stability distribution
            self.plot_stability_distribution()
            
            # Save the plot with a filename based on the input file
            plot_filename = os.path.splitext(filename)[0] + "_distribution.png"
            plot_path = os.path.join(distribution_dir, plot_filename)
            
            plt.savefig(plot_path)
            plt.close()
            
            print(f"Distribution plot saved at {plot_path}")
        except FileNotFoundError:
            print(f"The file '{filename}' does not exist.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def plot_stability_distribution(self) -> None:
        """
        Plots the distribution of stability over different iterations.
        Sets the x-axis to integer values.
        """
        plt.hist(self.stabilities, bins=30, edgecolor='black')
        plt.title('Distribution of Stability in Random Folding')
        plt.xlabel('Stability (integer values)')
        plt.ylabel('Frequency')
        plt.xticks(ticks=np.arange(min(self.stabilities), max(self.stabilities) + 1, 1))
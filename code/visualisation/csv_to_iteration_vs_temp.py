import csv
import matplotlib.pyplot as plt
import os

class CSVToPlot:
    """
    A utility class to generate plots from a CSV file.
    """

    def __init__(self, file_path: str):
        """
        Initializes the CSVToPlot class and loads the CSV file.

        Args:
            file_path (str): Path to the CSV file.
        """
        self.file_path = file_path
        self.headers = []
        self.data = []
        self._load_csv()

    def _load_csv(self) -> None:
        """
        Loads the CSV file and extracts headers and data.
        """
        try:
            with open(self.file_path, mode="r", newline="") as csv_file:
                reader = csv.reader(csv_file)
                self.headers = next(reader)  # Read the headers (Iteration, Stability, Temperature)
                self.data = [row for row in reader]  # Read the remaining data
            print(f"CSV file '{self.file_path}' loaded successfully.")
        except FileNotFoundError:
            print(f"Error: File '{self.file_path}' not found.")
        except Exception as e:
            print(f"Error loading CSV file: {e}")

    def plot_iterations_vs_temperature_stability(self, title: str = "Iterations vs. Temperature & Stability") -> None:
        """
        Plots a line graph of Iterations against Temperature and Stability.

        Args:
            title (str): Title of the plot.
        """
        if "Iteration" not in self.headers or "Temperature" not in self.headers or "Stability" not in self.headers:
            print(f"Error: Required columns ('Iteration', 'Stability', 'Temperature') not found in the CSV file.")
            print("Available columns:", self.headers)
            return

        try:
            # Get indices of required columns
            iteration_index = self.headers.index("Iteration")
            stability_index = self.headers.index("Stability")
            temp_index = self.headers.index("Temperature")

            # Extract and clean data
            iterations = []
            temperatures = []
            stabilities = []

            for row in self.data:
                try:
                    iterations.append(int(row[iteration_index]))  # Convert to int
                    stabilities.append(float(row[stability_index]))  # Convert to float
                    temperatures.append(float(row[temp_index]))  # Convert to float
                except ValueError:
                    continue  # Skip invalid rows

            # Plot the line graphs
            fig, ax1 = plt.subplots(figsize=(10, 6))

            # First y-axis: Temperature
            ax1.set_xlabel("Iteration")
            ax1.set_ylabel("Temperature", color="tab:blue")
            ax1.plot(iterations, temperatures, marker="o", linestyle="-", color="tab:blue", label="Temperature")
            ax1.tick_params(axis="y", labelcolor="tab:blue")

            # Second y-axis: Stability
            ax2 = ax1.twinx()
            ax2.set_ylabel("Stability", color="tab:red")
            ax2.plot(iterations, stabilities, marker="s", linestyle="--", color="tab:red", label="Stability")
            ax2.tick_params(axis="y", labelcolor="tab:red")

            # Title and legend
            plt.title(title)
            fig.tight_layout()
            plt.show()

        except Exception as e:
            print(f"Error during plotting: {e}")

    def list_headers(self) -> list:
        """
        Lists the available column headers from the CSV file.

        Returns:
            list: A list of column headers.
        """
        return self.headers


if __name__ == "__main__":
    # Example CSV file from your 'results' folder
    results_dir = "../team-eiwit/results"
    csv_file = "o_p9_simulated_120min.csv"  # Replace with your actual file
    csv_path = os.path.join(results_dir, csv_file)

    # Initialize the CSVToPlot class
    csv_plotter = CSVToPlot(csv_path)

    # Print available columns
    print("Available columns:", csv_plotter.list_headers())

    # Plot the Iteration vs. Temperature & Stability graph
    csv_plotter.plot_iterations_vs_temperature_stability(title="Simulated Annealing: Temperature & Stability over Iterations")

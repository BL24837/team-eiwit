import csv
import matplotlib.pyplot as plt

class CSVToDistribution:
    """
    A utility class to generate distribution histograms from a CSV file
    by selecting a specific column.
    """

    def __init__(self, file_path: str):
        """
        Initializes the CSVToDistribution class and loads the CSV file.

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
            with open(self.file_path, mode="r") as csv_file:
                reader = csv.reader(csv_file)
                self.headers = next(reader)  # Read the headers
                self.data = [row for row in reader]  # Read the remaining data
            print(f"CSV file '{self.file_path}' loaded successfully.")
        except FileNotFoundError:
            print(f"Error: File '{self.file_path}' not found.")
        except Exception as e:
            print(f"Error loading CSV file: {e}")

    def plot_distribution(self, column: str, bins: int = 30, title: str = "Distribution Plot") -> None:
        """
        Plots a histogram of the values in the specified column.

        Args:
            column (str): The column to plot the distribution for.
            bins (int): Number of bins in the histogram or a sequence of bin edges.
            title (str): Title of the histogram.
        """
        if column not in self.headers:
            print(f"Error: Column '{column}' not found in the CSV file.")
            return

        try:
            # Get the index of the selected column
            column_index = self.headers.index(column)

            # Extract and clean the data
            values = []
            for row in self.data:
                try:
                    value = float(row[column_index])
                    values.append(value)
                except ValueError:
                    continue  # Skip rows with non-numeric values

            # Define custom bins based on the range of the data
            min_value = min(values)
            max_value = max(values)
            bin_edges = list(range(int(min_value), int(max_value) + 2))  # Define integer bins

            # Plot the histogram
            plt.figure(figsize=(10, 6))
            plt.hist(values, bins=bin_edges, edgecolor="black", align="left")
            plt.title(title)
            plt.xlabel(column)
            plt.ylabel("Frequency")
            plt.grid(True)
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


# Main function for testing
if __name__ == "__main__":
    # Example CSV file from your 'results' folder
    results_dir = "../team-eiwit/results"
    csv_file = "d_p9_random_120min.csv"  # Replace with your file
    csv_path = f"{results_dir}/{csv_file}"

    # Initialize the CSVToDistribution class
    csv_distribution = CSVToDistribution(csv_path)

    # Print available columns
    print("Available columns:", csv_distribution.list_headers())

    # Plot the distribution for a chosen column
    csv_distribution.plot_distribution(column="Stability", bins=30, title="Stabiliteit bij Random Folding")

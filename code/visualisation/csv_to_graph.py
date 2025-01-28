import csv
import matplotlib.pyplot as plt
import os

class CSVToGraph:
    """
    A utility class to generate graphs from CSV files by allowing the user
    to select columns for the x and y axes.
    """

    def __init__(self, file_path: str):
        """
        Initializes the CSVToGraph class and loads the CSV file.

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

    def plot(self, x_col: str, y_col: str, title: str = "CSV Data Plot") -> None:
        """
        Plots the data using the selected columns for the x and y axes.

        Args:
            x_col (str): The column to use for the x-axis.
            y_col (str): The column to use for the y-axis.
            title (str): The title of the graph.
        """
        if x_col not in self.headers or y_col not in self.headers:
            print("Error: Specified columns not found in the CSV file.")
            return

        try:
            # Get the indices of the selected columns
            x_index = self.headers.index(x_col)
            y_index = self.headers.index(y_col)

            # Extract and clean the data
            x_data = []
            y_data = []

            for row in self.data:
                try:
                    x_value = float(row[x_index])
                    y_value = float(row[y_index])
                    x_data.append(x_value)
                    y_data.append(y_value)
                except ValueError:
                    # Skip rows where conversion to float fails
                    continue

            # Ensure x_data and y_data have the same length
            if len(x_data) != len(y_data):
                print(f"Error: Data mismatch. x_data: {len(x_data)}, y_data: {len(y_data)}")
                return

            # Plot the data
            plt.figure(figsize=(10, 6))
            plt.plot(x_data, y_data, marker="o", linestyle="-", color="b")
            plt.title(title)
            plt.xlabel(x_col)
            plt.ylabel(y_col)
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


# Main function for testing the CSVToGraph class
if __name__ == "__main__":
    # Path to the CSV file (use one of your files, e.g., 'b_p3_simulated_120min.csv')
    results_dir = "../team-eiwit/results"  # Adjust the path as needed
    csv_file = "o_p7_beam_120min.csv"  # Example CSV file
    csv_path = os.path.join(results_dir, csv_file)

    # Initialize the CSVToGraph class
    csv_graph = CSVToGraph(csv_path)

    # List available columns
    print("Available columns:", csv_graph.list_headers())

    # Test plotting (adjust column names based on your CSV headers)
    csv_graph.plot(x_col="Beam Width", y_col="Stability", title="Beam Width vs Stability")

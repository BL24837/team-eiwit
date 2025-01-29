import csv
import matplotlib.pyplot as plt
import os

class CSVPlotter:
    """
    A utility class to generate various plots (distribution, graph, or histogram) from a CSV file.
    """

    def __init__(self, file_path: str):
        """
        Initializes the CSVPlotter class and loads the CSV file.

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

    def list_headers(self) -> list:
        """
        Lists the available column headers from the CSV file.

        Returns:
            list: A list of column headers.
        """
        return self.headers

    def plot_distribution(self, column: str, bins: int = 30, title: str = "Distribution Plot") -> None:
        """
        Plots a histogram of the values in the specified column.

        Args:
            column (str): The column to plot the distribution for.
            bins (int): Number of bins in the histogram.
            title (str): Title of the histogram.
        """
        if column not in self.headers:
            print(f"Error: Column '{column}' not found in the CSV file.")
            return

        try:
            # Find the column index
            column_index = self.headers.index(column)
            
            # Read and process values
            values = []
            for row in self.data:
                try:
                    value = float(row[column_index])
                    values.append(value)
                except ValueError:
                    print(f"Skipping invalid row: {row}")  # Log invalid rows

            # Debugging: Print all read values
            print(f"Values read from column '{column}':", values)

            # Check for unique values
            unique_values = set(values)
            print(f"Unique values in column '{column}':", unique_values)
            if len(unique_values) == 1:
                print(f"Warning: All values in column '{column}' are identical. Histogram may not be meaningful.")
            else:
                print(f"Values contain variation. Proceeding with plot.")

            # Dynamically adjust bins if data has low variation
            if len(unique_values) == 1:
                bins = 1  # Single bin if all values are identical
            else:
                bins = range(int(min(values)), int(max(values)) + 2)  # Integer bins for better visualization

            # Plot the histogram
            plt.figure(figsize=(10, 6))
            plt.hist(values, bins=bins, edgecolor="black", alpha=0.7, align="left")
            plt.title(title)
            plt.xlabel(column)
            plt.ylabel("Frequency")
            plt.grid(True)
            plt.show()
        except Exception as e:
            print(f"Error during plotting: {e}")

    def plot_graph(self, x_col: str, y_col: str, title: str = "CSV Data Plot") -> None:
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
            x_index = self.headers.index(x_col)
            y_index = self.headers.index(y_col)
            x_data = []
            y_data = []

            # Process rows only if both columns have valid numeric values
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

    def plot_histogram(self, x_col: str, y_col: str, title: str = "Bar Chart") -> None:
        """
        Plots a bar chart using the specified columns for the x and y axes.

        Args:
            x_col (str): The column to use for the x-axis.
            y_col (str): The column to use for the y-axis.
            title (str): The title of the bar chart.
        """
        if x_col not in self.headers or y_col not in self.headers:
            print("Error: Specified columns not found in the CSV file.")
            return

        try:
            # Find the indices of the specified columns
            x_index = self.headers.index(x_col)
            y_index = self.headers.index(y_col)

            # Extract and clean data
            x_data = []
            y_data = []
            for row in self.data:
                try:
                    x_value = float(row[x_index])
                    y_value = float(row[y_index])
                    x_data.append(x_value)
                    y_data.append(y_value)
                except ValueError:
                    print(f"Skipping invalid row: {row}")  # Log invalid rows

            # Debugging: Check for mismatched lengths
            print(f"x_data: {x_data}")
            print(f"y_data: {y_data}")

            if len(x_data) != len(y_data):
                print(f"Error: Mismatch in data lengths. x_data: {len(x_data)}, y_data: {len(y_data)}")
                return

            # Plot the bar chart
            plt.figure(figsize=(10, 6))
            plt.bar(x_data, y_data, color="blue", alpha=0.7, edgecolor="black")
            plt.title(title)
            plt.xlabel(x_col)
            plt.ylabel(y_col)
            plt.grid(axis="y", linestyle="--", alpha=0.7)
            plt.show()

        except Exception as e:
            print(f"Error during plotting: {e}")



# Main function for user interaction
if __name__ == "__main__":
    # Predefined directory for CSV files
    results_dir = "results/"  # Ensure this directory exists

    # Ask the user for the CSV file name
    csv_file = input("Enter the name of the CSV file (e.g., 'o_p5_beam_120min.csv'): ").strip()
    csv_path = os.path.join(results_dir, csv_file)

    # Initialize the CSVPlotter class
    plotter = CSVPlotter(csv_path)

    # List available columns
    print("Available columns:", plotter.list_headers())

    # Menu for plot selection
    print("\nSelect the type of plot you want to generate:")
    print("1. Distribution Plot")
    print("2. Graph (Line Plot)")
    print("3. Histogram (Bar Chart)")
    choice = input("Enter your choice (1, 2, or 3): ").strip()

    if choice == "1":
        # Automatically use the Stability column
        if "Stability" in plotter.list_headers():
            plotter.plot_distribution(column="Stability")
        else:
            print("Error: 'Stability' column not found in the CSV file.")
    elif choice == "2":
        x_col = input("Enter the column name for the x-axis: ").strip()
        y_col = input("Enter the column name for the y-axis: ").strip()
        plotter.plot_graph(x_col=x_col, y_col=y_col)
    elif choice == "3":
        x_col = input("Enter the column name for the x-axis: ").strip()
        y_col = input("Enter the column name for the y-axis: ").strip()
        plotter.plot_histogram(x_col=x_col, y_col=y_col)
    else:
        print("Invalid choice. Please select 1, 2, or 3.")

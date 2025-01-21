from matplotlib import pyplot as plt
import csv
import os

class SiGraph():
    def __init__(self, sigraph, filename="si_data.csv"):
        # Construct the path to the CSV file in the /data/si_data directory
        csv_directory = os.path.join(os.path.dirname(__file__), '../..', 'data')
        self.filename = os.path.join(csv_directory, filename)
        self.sigraph = sigraph
        self.plot_sigraph()

    def plot_sigraph(self):
        # Parse the stability and iteration data
        stability_data = []
        iteration_data = []

        previous_stability = None
        previous_iteration = None

        for entry in self.sigraph:
            stability, iteration = entry.split(',')
            stability = float(stability)
            iteration = int(iteration)

            # If the stability is different from the previous one, add a new point
            if previous_stability is None or stability != previous_stability:
                stability_data.append(stability)
                iteration_data.append(iteration)
                previous_stability = stability
                previous_iteration = iteration
            elif iteration != previous_iteration:
                # Keep the same stability for consecutive iterations with the same stability
                stability_data.append(previous_stability)
                iteration_data.append(iteration)

        # Reverse the stability to make the lower stability values appear at the top
        stability_data = list(reversed(stability_data))
        iteration_data = list(reversed(iteration_data))

        # Create the plot
        plt.step(iteration_data, stability_data, where='post', label="Stability over Iterations", color="b")

        # Set plot labels
        plt.xlabel("Iteration")
        plt.ylabel("Stability (Lower stability at top)")
        plt.title("Stability vs. Iterations during Simulated Annealing")
        plt.grid(True)
        plt.show()

        # Save the data to CSV
        self.save_to_csv(iteration_data, stability_data)

    def save_to_csv(self, iteration_data, stability_data):
        # Find the next available run number
        run_number = self.get_next_run_number()

        # Open the CSV file and append the new run data
        with open(self.filename, mode='a', newline='') as file:
            writer = csv.writer(file)

            # Write the run header (e.g., Run 1)
            writer.writerow([f"Run {run_number}"])

            # Write the column headers (Iteration, Stability)
            writer.writerow(["Iteration", "Stability"])

            # Write the run data
            for iteration, stability in zip(iteration_data, stability_data):
                writer.writerow([iteration, stability])  # Write each row

            # Add a blank line after each run to separate them
            writer.writerow([])

        print(f"Run {run_number} data saved to {self.filename}")

    def get_next_run_number(self):
    # Check if the CSV file exists and find the highest run number
        if os.path.exists(self.filename):
            with open(self.filename, mode='r', newline='') as file:
                reader = csv.reader(file)
                runs = []

                for row in reader:
                    # Check if the row is not empty and starts with "Run"
                    if row and row[0].startswith("Run"):
                        try:
                            run_number = int(row[0].split()[1])  # Extract the run number
                            runs.append(run_number)
                        except (IndexError, ValueError):
                            # Skip rows that don't have a valid run number format
                            continue

                if runs:
                    return max(runs) + 1  # Return the next available run number
                else:
                    return 1  # Start with Run 1 if no runs exist
        else:
            return 1  # If the file doesn't exist, start with Run 1
import os, csv

class CsvFunctions():
    def __init__(self):
          pass
     
    def csv_header(self, raw_filepath, choice):
        if os.path.isfile(raw_filepath):
            # Controleer of de header al aanwezig is
            with open(raw_filepath, mode='r') as f:
                existing_data = f.readlines()
                if len(existing_data) == 0 or not existing_data[0].strip().startswith("Iteration"):
                    # Voeg de header toe bovenaan
                    temp_data = existing_data[:]
                    with open(raw_filepath, mode='w', newline='') as fw:
                        writer = csv.writer(fw)
                        if choice == 5:  # Simulated Annealing
                            writer.writerow(['Iteration', 'Stability', 'Temperature'])
                        elif choice == 3:  # Greedy Algorithm
                            writer.writerow(['Iteration', 'Stability'])
                        elif choice == 1:  # Random Folding
                            writer.writerow(['Iteration', 'Stability'])
                        elif choice == 4:  # beam search Folding
                            writer.writerow(['Beam Width', 'Stability',' elapsed_time'])
                        elif choice == 2:  # beam search Folding
                            writer.writerow(['Iteration', 'Stability'])
                        # Schrijf de bestaande gegevens opnieuw
                        fw.writelines(temp_data)
            return
        else:
            # Als het bestand niet bestaat, maak het aan met de header
            with open(raw_filepath, mode='w', newline='') as f:
                writer = csv.writer(f)
                if choice == 5:  # Simulated Annealing
                    writer.writerow(['Iteration', 'Stability', 'Temperature'])
                elif choice == 3:  # Greedy Algorithm
                    writer.writerow(['Iteration', 'Stability'])
                elif choice == 1:  # Random Algorithm
                    writer.writerow(['Iteration', 'Stability'])
                elif choice == 4:  # beam search Folding
                    writer.writerow(['Beam Width', 'Stability',' elapsed_time'])
                elif choice == 1:  # hillclimber Algorithm
                    writer.writerow(['Iteration', 'Stability'])

            return

    def csv_header_summary(self, summary_filepath, choice):
        if not os.path.isfile(summary_filepath):
            with open(summary_filepath, mode='w', newline='') as f:
                writer = csv.writer(f)
                if choice == 4:
                    writer.writerow(['Beam Width', 'Elapsed Time (s)', 'Stability', 'Protein Folding Sequence'])
                else:
                    writer.writerow(['Run', 'Execution Time (s)', 'Stability', 'Protein Folding Sequence'])

    def csv_summary(
            summary_filepath = None,
            choice = None,
            beam_width = None,
            elapsed_time = None,
            current_stability = None,
            folded_protein = None,
            run_count = None,
            execution_time = None
                    ):
        # Voeg samenvattingsgegevens toe aan het summary-bestand
        with open(summary_filepath, mode='a', newline='') as f:
            writer = csv.writer(f)
            if choice == 4:  # Beam Search
                writer.writerow([beam_width, elapsed_time, current_stability, folded_protein.sequence])
            else:  # Andere algoritmen
                writer.writerow([run_count + 1, execution_time, current_stability, folded_protein.sequence])
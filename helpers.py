from code.algorithms.greedy_algorithm import GreedyFolding
from code.algorithms.random_algorithm import RandomFolding
from code.algorithms.hillclimber import HillClimber
from code.algorithms.beam_search import BeamSearchProteinFolding
from code.algorithms.Simulatedannealing import SimulatedAnnealing
from code.classes.data_storing import DataStoring
from code.classes.csv_functions import CsvFunctions
from code.visualisation.visualize import ProteinVisualizer
from code.visualisation.distribution import Distribution
from datetime import datetime, timedelta

import matplotlib.pyplot as plt
import os, time, csv
import helpers

# Functions to retrieve users data via the terminal
def get_sequence():
    """
    Get a sequence from the user. The user can choose from a list of predefined sequences or enter their own sequence. 
    The user can also choose to enter a sequence.
    """
    sequence = None

    sequences = {
        1: "HHPHHHPH",
        2: "HHPHHHPHPHHHPH",
        3: "HPHPPHHPHPPHPHHPPHPH",
        4: "PPPHHPPHHPPPPPHHHHHHHPPHHPPPPHHPPHPP",
        5: "HHPHPHPHPHHHHPHPPPHPPPHPPPPHPPPHPPPHPHHHHPHPHPHPHH",
        6: "PPCHHPPCHPPPPCHHHHCHHPPHHPPPPHHPPHPP",
        7: "CPPCHPPCHPPCPPHHHHHHCCPCHPPCPCHPPHPC",
        8: "HCPHPCPHPCHCHPHPPPHPPPHPPPPHPCPHPPPHPHHHCCHCHCHCHH",
        9: "HCPHPHPHCHHHHPCCPPHPPPHPPPPCPPPHPPPHPHHHHCHPHPHPHH"
    }

    print("Choose a sequence:")
    for key, value in sequences.items():
        print(f"{key}: {value}")
    print("10: Enter your own sequence")

    choice = int(input("Enter a number between 1 and 9 to select the sequence: "))

    if 1 <= choice <= 9:
        sequence = sequences[choice]
        print(f"You selected sequence {choice}: {sequence}")
    elif choice == 10:
        sequence = input("Enter the sequence: ").strip()
    else:
        print("Invalid choice, please enter a number between 1 and 9.")

    return sequence

def get_algorithm():
    algorithm = {
        1: "Random Folding",
        2: "Hillclimber",
        3: "Greedy Folding",
        4: "Beam search folding",
        5: "Simulatedannealing folding",
    }
    print("Choose a algorithm:")
    for key, value in algorithm.items():
        print(f"{key}: {value}")
    print("6: Other menu")

    choice = input("Enter your choice (1, 2 ,3 ,4, 5 or 6): ").strip()
    try:
        choice = int(choice)
        if choice in algorithm:
            algorithm = algorithm[choice]
            return choice, algorithm
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")
            return None
    except ValueError:
        print("Invalid input. Please enter a number.")
        return None
    
def get_filename():
    while True:
        print("Check your file where you want to save the data. Check the parameters. For example exp1.csv")
        filename = input("Enter the filename: ").strip()

        # Control if file is empty
        if not filename:  
            print("No filename provided. Please enter a valid filename.")
            continue  

        # Control if file ends on csv
        if not filename.endswith('.csv'):
            print("Invalid file extension. Please use a .csv file extension.")
            continue  

        # Control if file exists
        file_path = os.path.join(os.path.dirname(__file__), 'results', filename)

        if os.path.isfile(file_path): 
            print(f"File '{filename}' found. Data will be appended.")
            break  
        else:  
            print(f"File '{filename}' does not exist. Please enter an existing file.")
            continue 

    return filename

def get_sort_run():
    print("1: Single run")
    print("2: loop algorithme")
    execution_mode = input("Enter your choice (1 or 2): ").strip()
    return execution_mode

def get_choise_menu():
    print("1: Length of protein")
    print("2: Visualize protein")
    print("3: Fold protein")

    choice_menu = input("Enter your choice (1, 2 or 3: ").strip()
    
    return choice_menu

def get_minutes():
    print("How many minutes you want to loop")
    x_times = input(" ").strip()
    x_times = int(x_times)
    return x_times

def get_sub_menu():
    print("1: Stability")
    print("2: Visualizer")
    print("3: Both")
    choice = input("Enter your choice (1, 2 or 3): ").strip()

    return choice

# Functions to run algorithms
def run_algorithm(choice: int, protein, algorithm, filename):
    data = DataStoring(algorithm=algorithm, filename=filename)
    folded_protein = None
    results_directory = os.path.join("results")
    raw_filepath = os.path.join(results_directory, filename)
    csv_object = CsvFunctions()
    csv_object.csv_header(raw_filepath, choice)

    if choice == 1:
        # Perform random folding
        iterations = int(input("Enter the number of iterations for random folding: ").strip())
        random_folding = RandomFolding(protein,data)
        folded_protein = random_folding.execute(iterations=iterations)
    
    elif choice == 2:
        # Perform hillclimber folding
        max_iterations = int(input("Enter the number of iterations for random folding: ").strip())
        hillclimber_folding = HillClimber( protein,max_iterations=max_iterations,data = data)
        folded_protein = hillclimber_folding.execute()
    
    elif choice == 3:
        # Perform greedy folding
        greedy_folding = GreedyFolding(data, protein)
        folded_protein = greedy_folding.execute()

    elif choice == 4:
        # Perform beam search
        beam_width = int(input("Enter the beam width for beam search folding: ").strip())
        beam_search = BeamSearchProteinFolding(data, protein, beam_width)
        folded_protein = beam_search.execute()

    elif choice == 5:
        # Perform simulated annealing
        sa = SimulatedAnnealing(data, protein)
        folded_protein = sa.execute()

    return folded_protein

def run_choise_menu(choice, protein):
    if choice == "1":
            print(f"Length of protein: {len(protein.amino_acids)}")
            return
    elif choice == "2":
        ProteinVisualizer(protein).display()
    elif choice == "3":

        directions = ['x_positive', 'x_negative', 'y_positive', 'y_negative', 'z_positive', 'z_negative']

        try:
            pivot = int(input("Enter your pivot point (index): ").strip())
            direction = input("Enter your direction (x_positive, x_negative, y_positive, y_negative, z_positive, z_negative): ").strip()

            if direction not in directions:
                print("Invalid direction. Please choose from:", directions)
                return False

            if pivot < 0 or pivot >= len(protein.amino_acids):
                print("Invalid pivot point. Please choose a valid index within the protein.")
                return False

            rotation_matrices = protein.get_rotation_matrices()
            rotation_matrix = rotation_matrices[direction]

            if protein.is_rotation_valid(pivot, rotation_matrix):
                protein.rotate_protein(pivot, rotation_matrix)
                print("Rotation performed successfully!")
                ProteinVisualizer(protein).display()
                return True
            else:
                print("Rotation is not valid.")
                return False
            
        except ValueError:
            print("Invalid input. Please enter a numerical pivot point.")
            return False
    else:
        print("Invalid choice. Please select 1, 2, 3, 4, or 5.")
        return

def run_algorithm_for_x_minutes(choice, protein, algorithm, filename, x_times):
    
    """
    Run an algorithm for a specified number of minutes and save the results in the folder under the given CSV file names.
    Both raw data and a summary will be saved.

    Parameters:

    choice: The selected algorithm.
    protein: The Protein object.
    algorithm: The name of the algorithm.
    filename: The filename of the CSV file where the results will be saved.
    x_times: The number of minutes the algorithm should run.
    """
    best_stability = None  
    best_protein = None  

    # Directories
    results_directory = os.path.join("results")
    summary_directory = os.path.join("results", "summary_loops")
    plots_directory = os.path.join("results", "plots")

    for directory in [results_directory, summary_directory, plots_directory]:
        if not os.path.exists(directory):
            os.makedirs(directory)

    raw_filepath = os.path.join(results_directory, filename)
    summary_filepath = os.path.join(summary_directory, filename)

    csv_object = CsvFunctions()

    csv_object.csv_header(raw_filepath, choice)
    csv_object.csv_header_summary(summary_filepath, choice)

    # Set looptime
    end_time = datetime.now() + timedelta(minutes=x_times)
    run_count = 0

    print(f"Starting {x_times}-minute execution...")

    while datetime.now() < end_time:
        start_time = time.time()  # Starting time
        data = DataStoring(algorithm=algorithm ,filename=filename, run_count=run_count)

        if choice == 1:  # Random Folding
            rf = RandomFolding(protein,data)
            folded_protein = rf.execute(iterations=1000)
        
        elif choice == 2:  # hillclimber
            max_iterations = int(10000)
            hillclimber_folding = HillClimber( protein,max_iterations=max_iterations,data = data)
            folded_protein = hillclimber_folding.execute()
        
        elif choice == 3:  # Greedy Algorithm
            gf = GreedyFolding(data, protein)
            folded_protein = gf.execute()
            
        elif choice == 4:  # Beam Search
            bs = BeamSearchProteinFolding(data, protein, beam_width=1)
            folded_protein = bs.execute_with_dynamic_beam_width(end_time)

        elif choice == 5:  # Simulated Annealing
            sa = SimulatedAnnealing(data, protein)
            folded_protein = sa.execute()

        # Calculates stabbility and time of the best protein from this run
        current_stability = folded_protein.calculate_stability()
        execution_time = time.time() - start_time

        if best_stability is None or current_stability < best_stability:
            best_stability = current_stability
            best_protein = folded_protein
        
        sequence_protein=folded_protein.sequence

        print(f"Run {run_count + 1} completed: Time={execution_time:.2f}s, Stability={current_stability}")
        
        csv_object.csv_summary(
            summary_filepath,
            current_stability,
            sequence_protein,
            run_count,
            execution_time)

        run_count += 1

    # Shows the best folding
    if best_protein:
        print(f"Best folding found:")
        print(f"Stability: {best_stability}")
        print(f"Protein folding sequence: {best_protein.sequence}")

        # Visualize the protein
        visualizer = ProteinVisualizer(best_protein)
        fig, ax = visualizer.display(return_figure=True)  
        plot_path = os.path.join(plots_directory, filename.replace('.csv', '_best_folding.png'))
        fig.savefig(plot_path)
        plt.close(fig)

        # Saves the amino acids placing of the best protein
        amino_acids_filename = filename.replace('.csv', '_best_folding.csv')
        amino_acids_path = os.path.join(plots_directory, amino_acids_filename)
        with open(amino_acids_path, mode='w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Index', 'Type', 'Position'])
            for index, amino_acid in enumerate(best_protein.amino_acids):
                writer.writerow([index, amino_acid['type'], amino_acid['position']])
    else:
        print("No valid folding found.")

    distribution = Distribution()
    distribution.visualize_stability_distribution_from_results(filename)


from code.algorithms.greedy_algorithm import *
from code.algorithms.random_algorithm import *
from code.algorithms.hillclimber import *
from code.algorithms.beam_search import *
from code.algorithms.Simulatedannealing import *
from code.classes.data_storing import DataStoring
from code.classes.csv_functions import CsvFunctions
from code.visualisation.timer import Timer
import os
from code.visualisation.visualize import ProteinVisualizer
from code.classes.protein import Protein
import helpers
from datetime import datetime, timedelta
import time
import csv
import pandas as pd


# Get information of the user via the terminal functions
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
    while True:  # Blijf vragen totdat een geldig bestaand bestand wordt ingevoerd
        print("Check your file where you want to save the data. Check the parameters. For example exp1.csv")
        filename = input("Enter the filename: ").strip()

        # Controleer of de bestandsnaam leeg is
        if not filename:  
            print("No filename provided. Please enter a valid filename.")
            continue  # Vraag opnieuw om de bestandsnaam

        # Controleer of de bestandsnaam eindigt op .csv
        if not filename.endswith('.csv'):
            print("Invalid file extension. Please use a .csv file extension.")
            continue  # Vraag opnieuw om de bestandsnaam

        # Controleer of het bestand al bestaat
        file_path = os.path.join(os.path.dirname(__file__), 'results', filename)

        if os.path.isfile(file_path):  # Bestand bestaat al
            print(f"File '{filename}' found. Data will be appended.")
            break  # Als het bestand bestaat, stop met vragen
        else:  # Bestand bestaat niet
            print(f"File '{filename}' does not exist. Please enter an existing file.")
            continue  # Vraag opnieuw om de bestandsnaam

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

# Run the chosen things functions
def run_algorithm(choice: int, protein, algorithm, filename):
    data = DataStoring(algorithm=algorithm, filename=filename)
    folded_protein = None

    if choice == 1:
        # Perform random folding
        iterations = int(input("Enter the number of iterations for random folding: ").strip())
        random_folding = RandomFolding(data, protein)
        folded_protein = random_folding.execute(iterations=iterations)
    
    elif choice == 2:
        # Perform hillclimber folding
        iterations = int(input("Enter the number of iterations for random folding: ").strip())
        hillclimber_folding = HillClimber(data, protein)
        folded_protein = hillclimber_folding.execute(iterations=iterations)
    
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
        folded_protein ,interation_data = sa.execute()

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
    Laat een algoritme een aantal minuten draaien en sla de resultaten op in de map onder de opgegeven CSV-bestandsnamen.
    Zowel raw data als een samenvatting worden opgeslagen.

    :param choice: De keuze van het algoritme.
    :param protein: Het Protein-object.
    :param algorithm: De naam van het algoritme.
    :param filename: Bestandsnaam van het CSV-bestand waarin resultaten worden opgeslagen.
    :param x_times: Aantal minuten dat het algoritme moet draaien.
    """
    best_stability = None  # Best stabiele score (initieel onbekend)
    best_protein = None  # Best folded protein (initieel onbekend)

    # Zorg ervoor dat de benodigde directories bestaan
    results_directory = os.path.join("results")
    summary_directory = os.path.join("results", "summary_loops")
    plots_directory = os.path.join("results", "plots")

    for directory in [results_directory, summary_directory, plots_directory]:
        if not os.path.exists(directory):
            os.makedirs(directory)

    # Bestandslocaties voor ruwe data en samenvatting
    raw_filepath = os.path.join(results_directory, filename)
    summary_filepath = os.path.join(summary_directory, filename)

    csv_object = CsvFunctions()

    csv_object.csv_header(raw_filepath, choice)
    csv_object.csv_header_summary(summary_filepath, choice)

    # Looptijden instellen
    end_time = datetime.now() + timedelta(minutes=x_times)
    run_count = 0

    print(f"Starting {x_times}-minute execution...")

    while datetime.now() < end_time:
        start_time = time.time()  # Starttijd van deze run
        data = DataStoring(algorithm=algorithm ,filename=filename)

        if choice == 4:  # Beam Search
            beam_search = BeamSearchProteinFolding(data, protein, beam_width=1)
            folded_protein, beam_data = beam_search.execute_with_dynamic_beam_width(end_time)

            # Log de Beam Search gegevens naar raw data CSV
            with open(raw_filepath, mode='a', newline='') as f:
                writer = csv.writer(f)
                for beam_width,elapsed_time, stability in beam_data:
                    writer.writerow([beam_width,stability,elapsed_time])

        elif choice == 5:  # Simulated Annealing
            # Simulated Annealing uitvoeren
            sa = SimulatedAnnealing(data, protein)
            folded_protein, iteration_data = sa.execute()

            # Log de iteration data naar raw data CSV
            with open(raw_filepath, mode='a', newline='') as f:
                writer = csv.writer(f)
                for iteration, temp, stability in iteration_data:
                    writer.writerow([iteration, stability, temp])

        elif choice == 3:  # Greedy Algorithm
            # Greedy Algorithm uitvoeren
            greedy_folding = GreedyFolding(data, protein)
            folded_protein = greedy_folding.execute()

            # Stabiliteit van de huidige vouwing berekenen
            current_stability = folded_protein.calculate_stability()

            # Log gegevens naar raw data CSV
            with open(raw_filepath, mode='a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([run_count + 1, current_stability])

        elif choice == 1:  # Random Folding
            random_folding = RandomFolding(data, protein)
            folded_protein = random_folding.execute(iterations=10000)

            # Log de random folding data
            current_stability = folded_protein.calculate_stability()
            with open(raw_filepath, mode='a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([run_count + 1, current_stability])

        # Bereken de stabiliteit en tijd van de huidige run
        current_stability = folded_protein.calculate_stability()
        execution_time = time.time() - start_time  # Looptijd van deze run

        if best_stability is None or current_stability < best_stability:
            best_stability = current_stability
            best_protein = folded_protein

        # Voeg samenvattingsgegevens toe aan het summary-bestand
        with open(summary_filepath, mode='a', newline='') as f:
            writer = csv.writer(f)
            if choice == 4:  # Beam Search
                writer.writerow([beam_width, elapsed_time, current_stability, folded_protein.sequence])
            else:  # Andere algoritmen
                writer.writerow([run_count + 1, execution_time, current_stability, folded_protein.sequence])

        print(f"Run {run_count + 1} completed: Time={execution_time:.2f}s, Stability={current_stability}")
        run_count += 1



    # Toon de beste vouwing na afloop van de loop
    if best_protein:
        print(f"Best folding found:")
        print(f"Stability: {best_stability}")
        print(f"Protein folding sequence: {best_protein.sequence}")

        # Visualiseer het beste eiwit
        visualizer = ProteinVisualizer(best_protein)
        fig, ax = visualizer.display(return_figure=True)  # Haal de figuur op om op te slaan
        plot_path = os.path.join(plots_directory, filename.replace('.csv', '_best_folding.png'))
        fig.savefig(plot_path)
        plt.close(fig)

        # Sla de aminozuurgegevens van de beste vouwing op
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


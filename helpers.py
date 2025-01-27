from code.algorithms.greedy_algorithm import *
from code.algorithms.random_algorithm import *
from code.algorithms.hillclimber import *
from code.algorithms.beam_search import *
from code.algorithms.Simulatedannealing import *
from code.classes.data_storing import DataStoring
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
    print("10: Enter your own sequence")

    choice = input("Enter your choice (1, 2 ,3 ,4, 5, 6 or 7): ").strip()
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

def get_choise_menu():
    print("1: Length of protein")
    print("2: Visualize protein")
    print("3: Fold protein")

    choice_menu = input("Enter your choice (1, 2 or 3: ").strip()
    
    return choice_menu

# Run the chosen things functions
def run_algorithm(choice: int, protein, algorithm, filename):
    data = DataStoring(algorithm=algorithm, filename=filename)
    folded_protein = None

    if choice == 1:
        # Perform random folding
        iterations = int(input("Enter the number of iterations for random folding: ").strip())
        random_folding = RandomFolding(data, protein)
        if random_folding:
            print("Random folding is  possible")
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
        sequence = protein.sequence
        beam_width = int(input("Enter the beam width for beam search folding: ").strip())
        timer = Timer()
        timer.start()
        beam_search = BeamSearchProteinFolding(data, sequence, beam_width)
        folded_protein = beam_search.execute() # extra optie plot_distribution = False
        timer.stop()
        elapsed = timer.elapsed_time()
        score = folded_protein.calculate_stability()
        print(elapsed)
        beam_search.export_results(folded_protein, score, elapsed)


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
    Laat een algoritme een aantal minuten draaien en sla de resultaten op in een map onder de opgegeven CSV-bestandsnaam.

    :param choice: De keuze van het algoritme.
    :param protein: Het Protein-object.
    :param algorithm: De naam van het algoritme.
    :param filename: Bestandsnaam van het CSV-bestand waarin resultaten worden opgeslagen.
    :param x_times: Aantal minuten dat het algoritme moet draaien.
    """

    best_stability = None  # Best stabiele score (initieel onbekend)
    best_protein = None  # Best folded protein (initieel onbekend)
    
    # Zorg ervoor dat de map "results/summary_loops" bestaat en dat plots bestaat
    directory = os.path.join("results", "summary_loops")
    plots_directory = os.path.join("results", "plots")
    if not os.path.exists(directory):
        os.makedirs(directory)
    if not os.path.exists(plots_directory):
        os.makedirs(plots_directory)


    # Volledig pad naar het CSV-bestand
    filepath = os.path.join(directory, filename)

    # Zorg ervoor dat het CSV-bestand een header heeft als het nog niet bestaat
    if not os.path.isfile(filepath):
        with open(filepath, mode='w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Run', 'Execution Time (s)', 'Stability', 'Protein Folding Sequence'])

    end_time = datetime.now() + timedelta(minutes=x_times)
    run_count = 0

    print(f"Starting {x_times}-minute execution...")

    while datetime.now() < end_time:
        start_time = time.time()  # Starttijd van deze run

        # Voer het algoritme uit
        folded_protein = helpers.run_algorithm(choice=choice, protein=protein, algorithm=algorithm, filename=filename)

        # Bereken de stabiliteit van de huidige vouwing
        current_stability = folded_protein.calculate_stability()

        # Als het de eerste run is, stel de eerste protein als de "beste"
        if best_stability is None or current_stability < best_stability:
            best_stability = current_stability
            best_protein = folded_protein

        execution_time = time.time() - start_time  # Looptijd van deze run

        # Resultaten toevoegen aan CSV-bestand
        with open(filepath, mode='a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([run_count + 1, execution_time, current_stability, folded_protein.sequence])

        print(f"Run {run_count + 1} completed: Time={execution_time:.2f}s, Stability={current_stability}")
        run_count += 1

    print(f"Finished {x_times} minutes of execution. Total runs: {run_count}")

    # Toon de beste vouwing na afloop van de loop
    if best_protein:
        print(f"Best folding found:")
        print(f"Stability: {best_stability}")
        print(f"Protein folding sequence: {best_protein.sequence}")

        # Visualiseer het beste eiwit
        visualizer = ProteinVisualizer(best_protein)
        fig, ax = visualizer.display(return_figure =True)  # Haal de figuur op om op te slaan

        # Sla de figuur op als PNG
        plot_path = os.path.join(plots_directory, filename.replace('.csv', '_best_folding.png'))
        fig.savefig(plot_path)
        plt.close(fig)

        amino_acids_filename = filename.replace('.csv', '_best_folding.csv')
        amino_acids_path = os.path.join(plots_directory, amino_acids_filename)
        with open(amino_acids_path, mode='w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Index', 'Type', 'Position'])
            for index, amino_acid in enumerate(best_protein.amino_acids):
                writer.writerow([index, amino_acid['type'], amino_acid['position']])
    else:
        print("No valid folding found.")

    visualize_stability_distribution_from_results(filename)

def visualize_stability_distribution_from_results(filename):
    """
    Maakt een distributiegrafiek van stabiliteit op basis van de gegevens in de tweede kolom van een CSV-bestand
    en slaat deze op als een PNG-bestand in de map 'results/distribution'.

    :param filename: Naam van het CSV-bestand in de map 'results'.
    """
    # Zorg ervoor dat de map 'results/distribution' bestaat
    distribution_dir = os.path.join("results", "distribution")
    if not os.path.exists(distribution_dir):
        os.makedirs(distribution_dir)

    # Pad naar het bestand
    filepath = os.path.join("results", filename)
    
    try:
        # Lees het CSV-bestand
        stabilities = []
        with open(filepath, mode='r') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Sla de header over als die aanwezig is
            for row in reader:
                if len(row) > 1:  # Controleer of er een tweede kolom is
                    try:
                        stability = float(row[1])  # Haal het tweede element (Stability) op
                        stabilities.append(stability)
                    except ValueError:
                        continue  # Sla rijen over met ongeldige waarden
        
        # Controleer of we stabiliteitsgegevens hebben
        if not stabilities:
            print(f"Geen stabiliteitsgegevens gevonden in {filename}.")
            return
        
        # Maak de distributiegrafiek met de Distribution-klasse
        distribution = Distribution(stabilities)
        
        # Sla de grafiek op met de naam aangepast aan het bestand
        plot_filename = os.path.splitext(filename)[0] + "_distribution.png"
        plot_path = os.path.join(distribution_dir, plot_filename)
        
        # Sla de distributiegrafiek op
        plt.savefig(plot_path)
        plt.close()
        
        print(f"Distributiegrafiek opgeslagen in {plot_path}")
    except FileNotFoundError:
        print(f"Het bestand '{filename}' bestaat niet.")
    except Exception as e:
        print(f"Er ging iets fout: {e}")


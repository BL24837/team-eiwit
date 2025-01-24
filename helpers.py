from code.algorithms.greedy_algorithm import *
from code.algorithms.random_algorithm import *
from code.algorithms.hillclimber import *
from code.algorithms.beam_search import *
from code.algorithms.Simulatedannealing import *
from code.classes.data_storing import DataStoring
from code.visualisation.data import Data

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

def get_dimension():
    """
    Get the dimension from the user. The user can choose between 2D and 3D.
    """
    print("Select the dimension:")
    print("1: 2D")
    print("2: 3D")
    dimension = input("Enter your choice (1 or 2): ").strip()

    return dimension

def get_algorithm():
    algorithm = {
        1: "Random Folding",
        2: "Hillclimber",
        3: "Greedy Folding",
        4: "Beam search folding",
        5: "Simulatedannealing folding",
        6: "lightBGM"
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
    print("Enter the filename for the results. Look into the folder results. Than your chosen dimension, algorithm and sequence. If already existing files check for the same parameters, else type in exp + 1. If none is put in, the code creates self a csv file with name exp + 1.")
    filename = input("Enter the filename: ").strip()
    if not filename:  # Check if filename is empty
        return None
    return filename

def get_choise_menu():
    print("1: Length of protein")
    print("2: Visualize protein")
    print("3: Fold protein")

    choice_menu = input("Enter your choice (1, 2 or 3: ").strip()
    
    return choice_menu

# Run the chosen things functions
def run_algorithm(choice: int, protein, dimension, algorithm, filename):
    data = DataStoring(sequence=protein.sequence, dimension=dimension, algorithm=algorithm, filename=filename)
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
        beam_search = BeamSearchProteinFolding(data, sequence, beam_width)
        folded_protein = beam_search.execute() # extra optie plot_distribution = False

    elif choice == 5:
        # Perform simulated annealing
        sa = SimulatedAnnealing(data, protein)
        folded_protein = sa.execute()

    elif choice == 6:
        lgbm_folding = LightGBMFolding(data, protein)
        lgbm_folding.train_model()
        folded_protein = lgbm_folding.predict_best_folding()

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
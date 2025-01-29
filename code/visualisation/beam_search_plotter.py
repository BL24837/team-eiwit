import csv
import matplotlib.pyplot as plt
from code.visualisation.timer import Timer
from code.algorithms.beam_search import BeamSearchProteinFolding
from code.classes.protein import Protein

def run_and_export_beam_search(sequence: str, max_beam_width: int, output_file: str) -> None:
    """
    Executes beam search for beam widths ranging from 1 to max_beam_width, exports results to CSV, and generates a plot.
    
    The X-axis represents beam width, and the Y-axis represents stability score.

    Args:
        sequence (str): The protein sequence.
        max_beam_width (int): The maximum beam width to be tested.
        output_file (str): The name of the CSV file to store the results.
    """
    beam_widths = []  # List to store beam width values
    scores = []  # List to store corresponding stability scores
    results = []  # List to store results in dictionary format

    for beam_width in range(1, max_beam_width + 1):
        print(f"Running beam search for beam width: {beam_width}")
        
        # Execute beam search algorithm
        beam_search = BeamSearchProteinFolding(None, sequence, beam_width)
        folded_protein = beam_search.execute(plot_distribution=False)

        # Calculate stability score
        score = folded_protein.calculate_stability()
        
        # Store results
        beam_widths.append(beam_width)
        scores.append(score)
        results.append({"beam_width": beam_width, "score": score})
    
    # Export results to CSV file
    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Beam Width", "Score"])
        for result in results:
            writer.writerow([result["beam_width"], result["score"]])
    
    # Plot results
    plt.figure(figsize=(10, 6))
    plt.plot(beam_widths, scores, marker="o", linestyle="-", color="b")
    plt.title("Beam Width versus Score")
    plt.xlabel("Beam Width")
    plt.ylabel("Score")
    plt.grid(True)
    plt.show()

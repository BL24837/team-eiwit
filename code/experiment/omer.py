import csv
import matplotlib.pyplot as plt
from code.visualisation.timer import Timer
from code.algorithms.beam_search import BeamSearchProteinFolding
from code.classes.protein import Protein

def run_beam_search_experiments(sequence, max_beam_width, output_file):
    """
    Voert beam search uit voor verschillende beam widths en slaat de resultaten op.
    
    X-as : Beam_width
    Y-as : Score en Tijd

    Args:
        sequence (str): De eiwitsequentie.
        max_beam_width (int): Maximale beam width om te proberen.
        output_file (str): Naam van het CSV-bestand voor de resultaten.
    """
    results = []
    
    for beam_width in range(1, max_beam_width + 1):
        # Initialiseer de timer
        timer = Timer()
        timer.start()
        
        # Voer beam search uit
        beam_search = BeamSearchProteinFolding(None, sequence, beam_width)
        folded_protein = beam_search.execute(plot_distribution=False)
        
        # Stop de timer
        timer.stop()
        elapsed_time = timer.elapsed_time()
        
        # Bereken stabiliteit
        score = folded_protein.calculate_stability()
        
        # Sla resultaten op
        results.append({"beam_width": beam_width, "score": score, "time": elapsed_time})
        print(f"Beam width: {beam_width}, Score: {score}, Time: {elapsed_time:.2f} seconds")
    
    # Schrijf resultaten naar CSV
    with open(output_file, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["beam_width", "score", "time"])
        writer.writeheader()
        writer.writerows(results)
    print(f"Resultaten opgeslagen in {output_file}.")
    
    # Plot de resultaten
    beam_widths = [result["beam_width"] for result in results]
    times = [result["time"] for result in results]

    plt.figure(figsize=(10, 6))
    plt.plot(beam_widths, times, marker='o', linestyle='-', label="Time (seconds)")
    plt.title("Beam Width vs Time")
    plt.xlabel("Beam Width")
    plt.ylabel("Time (seconds)")
    plt.grid(True)
    plt.legend()
    plt.show()

# Voorbeeldgebruik
if __name__ == "__main__":
    sequence = "HCPHPHP"  # Vervang dit door de gewenste eiwitsequentie
    max_beam_width = 10
    output_file = "beam_search_experiments3.csv"
    
    run_beam_search_experiments(sequence, max_beam_width, output_file)

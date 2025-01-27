import csv
import matplotlib.pyplot as plt
from code.visualisation.timer import Timer
from code.algorithms.beam_search import BeamSearchProteinFolding
from code.classes.protein import Protein

def run_and_export_beam_search(sequence, max_beam_width, output_file):
    """
    Voert beam search uit voor beam widths van 1 tot max_beam_width, exporteert resultaten naar CSV en maakt een grafiek.
    
    X-as beam width
    Y-as score

    Args:
        sequence (str): De eiwitsequentie.
        max_beam_width (int): Maximale beam width om te proberen.
        output_file (str): Naam van het CSV-bestand voor de resultaten.
    """
    beam_widths = []
    scores = []
    results = []

    for beam_width in range(1, max_beam_width + 1):
        print(f"Running beam search for beam width: {beam_width}")
        
        # Timer starten
        timer = Timer()
        timer.start()
        
        # Beam search uitvoeren
        beam_search = BeamSearchProteinFolding(None, sequence, beam_width)
        folded_protein = beam_search.execute(plot_distribution=False)
        
        # Timer stoppen
        timer.stop()
        
        # Stabiliteit berekenen
        score = folded_protein.calculate_stability()
        elapsed_time = timer.elapsed_time()
        
        # Resultaten opslaan
        beam_widths.append(beam_width)
        scores.append(score)
        results.append({"beam_width": beam_width, "score": score})
        
        print(f"Beam width: {beam_width}, Score: {score}, Time: {elapsed_time:.2f} seconds")
    
    # Schrijf resultaten naar CSV
    with open(output_file, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["beam_width", "score"])
        writer.writeheader()
        writer.writerows(results)
    print(f"Resultaten succesvol geëxporteerd naar {output_file}.")
    
    # Resultaten plotten
    plt.figure(figsize=(10, 6))
    plt.plot(beam_widths, scores, marker="o", linestyle="-", color="b")
    plt.title("Beam Width versus Score")
    plt.xlabel("Beam Width")
    plt.ylabel("Score")
    plt.grid(True)
    plt.show()

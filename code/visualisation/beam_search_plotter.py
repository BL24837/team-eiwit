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
        
        # Beam search uitvoeren
        beam_search = BeamSearchProteinFolding(None, sequence, beam_width)
        folded_protein = beam_search.execute(plot_distribution=False)

        
        # Stabiliteit berekenen
        score = folded_protein.calculate_stability()
        
        # Resultaten opslaan
        beam_widths.append(beam_width)
        scores.append(score)
        results.append({"beam_width": beam_width, "score": score})
    
    # Resultaten plotten
    plt.figure(figsize=(10, 6))
    plt.plot(beam_widths, scores, marker="o", linestyle="-", color="b")
    plt.title("Beam Width versus Score")
    plt.xlabel("Beam Width")
    plt.ylabel("Score")
    plt.grid(True)
    plt.show()

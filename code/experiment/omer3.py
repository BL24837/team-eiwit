import csv
import matplotlib.pyplot as plt
from code.visualisation.timer import Timer
from code.algorithms.beam_search import BeamSearchProteinFolding

def grid_search_beam_width(sequence, beam_width_values, num_runs_per_value, output_file):
    """
    Voert grid search uit voor de parameter beam_width, exporteert resultaten naar CSV en maakt een grafiek.
    
    Args:
        sequence (str): De eiwitsequentie.
        beam_width_values (list): Lijst van waarden voor beam_width.
        num_runs_per_value (int): Aantal runs per waarde.
        output_file (str): Naam van het CSV-bestand voor de resultaten.
    """
    beam_widths = []
    avg_scores = []
    results = []

    for beam_width in beam_width_values:
        print(f"Running beam search for beam width: {beam_width}")
        
        total_score = 0
        total_time = 0
        
        for _ in range(num_runs_per_value):
            timer = Timer()
            timer.start()
            
            # Beam search uitvoeren
            beam_search = BeamSearchProteinFolding(None, sequence, beam_width)
            folded_protein = beam_search.execute(plot_distribution=False)
            
            timer.stop()
            elapsed_time = timer.elapsed_time()
            score = folded_protein.calculate_stability()

            # Accumuleer resultaten
            total_score += score
            total_time += elapsed_time
        
        # Gemiddelde resultaten berekenen
        avg_score = total_score / num_runs_per_value
        avg_scores.append(avg_score)
        beam_widths.append(beam_width)
        results.append({"beam_width": beam_width, "avg_score": avg_score})
        
        print(f"Beam width: {beam_width}, Average Score: {avg_score}, Time: {total_time / num_runs_per_value:.2f} seconds")

    # Schrijf resultaten naar CSV
    with open(output_file, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["beam_width", "avg_score"])
        writer.writeheader()
        writer.writerows(results)
    print(f"Resultaten succesvol geëxporteerd naar {output_file}.")

    # Resultaten plotten
    plt.figure(figsize=(10, 6))
    plt.plot(beam_widths, avg_scores, marker="o", linestyle="-", color="b")
    plt.title("Beam Width versus Average Score")
    plt.xlabel("Beam Width")
    plt.ylabel("Average Score")
    plt.grid(True)
    plt.show()

# Voorbeeldgebruik
if __name__ == "__main__":
    sequence = "HCHHCHC"  # De eiwitsequentie
    beam_width_values = [1, 5, 10, 20, 50, 100]  # Waarden voor beam_width
    num_runs_per_value = 15  # Aantal runs per waarde
    output_file = "grid_search_results.csv"  # Naam van het uitvoerbestand

    grid_search_beam_width(sequence, beam_width_values, num_runs_per_value, output_file)

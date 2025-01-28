import numpy as np
import matplotlib.pyplot as plt
import os, csv

class Distribution:
    """
    Class voor het visualiseren van de distributie van stabiliteit over de verschillende iteraties.
    """
    
    def __init__(self, stabillities=None):
        self.stabillities = stabillities

    def visualize_stability_distribution_from_results(self, filename):
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
        print(f"{filepath}")
        
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
                            print(stability)
                        except ValueError:
                            continue  # Sla rijen over met ongeldige waarden
            
            # Controleer of we stabiliteitsgegevens hebben
            if not stabilities:
                print(f"Geen stabiliteitsgegevens gevonden in {filename}.")
                return
            
            # Maak de distributiegrafiek met de Distribution-klasse
            self.stabillities = stabilities

            distribution = self.plot_stability_distribution()
            
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

    def plot_stability_distribution(self):
        """
        Plot de distributie van stabiliteit over de verschillende iteraties.
        Stelt de x-as in op gehele getallen.
        
        Args:
            stabilities (list): Lijst van stabiliteitswaarden per iteratie.
        """
        plt.hist(self.stabillities, bins=30, edgecolor='black')
        plt.title('Distributie van stabiliteit bij random folding')
        plt.xlabel('Stabiliteit (gehele getallen)')
        plt.ylabel('Frequentie')
        plt.xticks(ticks=np.arange(min(self.stabillities), max(self.stabillities) + 1, 1))
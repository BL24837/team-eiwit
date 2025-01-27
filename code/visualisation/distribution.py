import numpy as np
import matplotlib.pyplot as plt

class Distribution:
    """
    Class voor het visualiseren van de distributie van stabiliteit over de verschillende iteraties.
    """
    
    def __init__(self, stabilities):
        self.stabilities = stabilities
        self.plot_stability_distribution()

    def plot_stability_distribution(self):
            """
            Plot de distributie van stabiliteit over de verschillende iteraties.
            Stelt de x-as in op gehele getallen.
            
            Args:
                stabilities (list): Lijst van stabiliteitswaarden per iteratie.
            """
            plt.hist(self.stabilities, bins=30, edgecolor='black')
            plt.title('Distributie van stabiliteit bij random folding')
            plt.xlabel('Stabiliteit (gehele getallen)')
            plt.ylabel('Frequentie')
            plt.xticks(ticks=np.arange(min(self.stabilities), max(self.stabilities) + 1, 1))
            

# Example usage:
# stabilities = [0, -1, -1.5, -2, -3, -2.5, -1]
# distribution = Distribution(stabilities)

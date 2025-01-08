import numpy as np
import random
import matplotlib.pyplot as plt

# Eiwitsequentie
sequentie = "HHPHHHPHPHHPHHPHPPH"

# Dimensies van de ruimte voor vouwen (2D grid)
grid_size = 10

# Functie om de energie van een specifieke configuratie te berekenen
def bereken_energie(coordinates, sequentie):
    energie = 0
    for i in range(len(sequentie)):
        for j in range(i+1, len(sequentie)):
            # Afstand tussen twee punten
            x1, y1 = coordinates[i]
            x2, y2 = coordinates[j]
            afstand = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
            
            # Als beide H zijn, telt dat als een positieve interactie
            if sequentie[i] == 'H' and sequentie[j] == 'H':
                energie += 1 / afstand  # Positieve interactie, de energie wordt lager als ze dichterbij zijn
            # Coils (P) interactie wordt als een negatieve energie beschouwd
            if sequentie[i] == 'P' and sequentie[j] == 'P':
                energie -= 1 / afstand  # Negatieve interactie voor coils
    return energie

# Functie om de eiwitstructuur te vouwen in 2D
def vouw_eiwit(sequentie):
    # Begin met een willekeurige plaatsing van de eiwitsequentie in het 2D-vlak
    coordinates = [(grid_size//2, grid_size//2)]  # Begin met het plaatsen van het eerste aminozuur in het midden
    richting = [(1, 0), (0, 1), (-1, 0), (0, -1)]  # Vier mogelijke richtingen om te bewegen
    
    # Plaats de aminozuren (H of P) op het grid
    for i in range(1, len(sequentie)):
        last_x, last_y = coordinates[-1]
        random.shuffle(richting)  # Willekeurige richting kiezen
        for dx, dy in richting:
            new_x, new_y = last_x + dx, last_y + dy
            if 0 <= new_x < grid_size and 0 <= new_y < grid_size and (new_x, new_y) not in coordinates:
                coordinates.append((new_x, new_y))
                break

    # Bereken de energie van deze vouw
    energie = bereken_energie(coordinates, sequentie)
    
    return coordinates, energie

# Voer het vouw-algoritme uit en toon de resultaten
coordinates, energie = vouw_eiwit(sequentie)

# Visualiseer de vouw van het eiwit
x_coords, y_coords = zip(*coordinates)
plt.figure(figsize=(6, 6))
plt.plot(x_coords, y_coords, marker='o', linestyle='-', color='b')
plt.title(f"Eiwitvouwing met energie: {energie:.2f}")
plt.xlim(0, grid_size)
plt.ylim(0, grid_size)
plt.gca().set_aspect('equal', adjustable='box')
plt.grid(True)
plt.show()

print(f"Energie van de vouw: {energie}")
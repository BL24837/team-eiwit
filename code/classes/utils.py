import csv

class utils:
    def read_sequences(file_path):
        proteins = []
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file, delimiter=';')  
            for row in reader:
                proteins.append({
                    'id': row['id'],           
                    'sequence': row['sequence'] 
                })
        return proteins


    def export_results_to_csv(protein, file_path):
        """
        Exporteert de eiwitstructuur naar een CSV-bestand in het gewenste formaat.

        Args:
            protein (Protein): Het gevouwen eiwitobject.
            file_path (str): Pad naar het output CSV-bestand.
        """
        rows = []
        grid_positions = list(protein.grid.keys())
        sequence = [amino_acid.type for amino_acid in protein.sequence]

        for i in range(len(grid_positions) - 1):
            current = grid_positions[i]
            next_ = grid_positions[i + 1]
            delta_x = next_[0] - current[0]
            delta_y = next_[1] - current[1]

            if delta_x > 0:
                fold = 1  
            elif delta_x < 0:
                fold = -1  
            elif delta_y > 0:
                fold = 2 
            elif delta_y < 0:
                fold = -2  
            else:
                fold = 0  

            rows.append({'amino': sequence[i], 'fold': fold})

        rows.append({'amino': sequence[-1], 'fold': 0})

        rows.append({'amino': 'score', 'fold': protein.score})

        with open(file_path, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=['amino', 'fold'])
            writer.writeheader()
            writer.writerows(rows)

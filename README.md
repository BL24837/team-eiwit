# Protein Folding Optimization

This project focuses on optimizing protein folding using a different algorithm. Proteins in this project consist of three types of amino acids: hydrophobic amino acids (H), polar amino acids (P), and cysteine (C). These amino acids can be folded around each other to form a compact structure.

The strength of the protein structure is determined by the stability score, which is calculated based on bonds between specific amino acids:
- **H-H or C-H bonds**: Contribute a stability of `-1`.
- **C-C bonds**: Contribute a stronger stability of `-5`.

The goal of this project is to find a configuration with the lowest possible stability score, as a lower score indicates a more stable and tightly folded protein.


# Installing

### Clone the repository
Before cloning make sure you make a empty directory to clone into.
```
git clone <https://github.com/BL24837/team-eiwit.git>
```

#### Navigate to the project directory
```
cd <repository-directory>
```

### Install dependencies
After opening the right repository instal all requirements.
```
pip install -r requirements.txt
```

## Operation of the different algorithms

1. Random Algorithm:
The Random Folding Algorithm explores the solution space of protein folding by performing random rotations of the protein structure. It aims to discover configurations with the best stability. The algorithm is particularly suited for generating diverse solutions without bias towards specific patterns.

2. Greedy Algorithm:
The Hybrid Folding Algorithm combines random exploration and greedy refinement to optimize the folding of protein sequences. It leverages a two-phase process:
Exploratory Random Folding: Identifies an initial configuration with a stability score of -1 or better.
Iterative Refinement: Incrementally improves the protein's stability using a mix of greedy and random folding approaches.

3. Beam Search:
The Beam Search Protein Folding Algorithm is a heuristic method designed to find an optimal folding configuration for a protein sequence. It systematically explores possible configurations while maintaining a fixed number of top candidates (beam width) at each step, effectively balancing exploration and computational efficiency.

4. Hill Climber:
The Hill Climber Algorithm is a local search optimization technique used to find a better folding configuration for a protein. It works iteratively, exploring small, random changes in the current configuration to improve the stability score. This approach is simple yet effective for incrementally improving protein folding solutions.

5. Simmulated Annealing:
The Simulated Annealing Algorithm is a probabilistic optimization technique inspired by the annealing process in metallurgy. It seeks to optimize protein folding by balancing exploration of the solution space with exploitation of promising configurations. By gradually lowering the "temperature," the algorithm transitions from broad exploration to focused refinement, effectively escaping local minima.
This program is run on ```Python 3.10.12```

# Running

## main program
Run this code:
```
python3 main.py
```
OR
```
python main.py
```

# How to Reproduce Results (scripts)

All results can be found in the `results` folder, which contains CSV files. 

### Explanation of the CSV Files
- `p1` stands for protein sequence 1, `p2` for protein sequence 2, and so on.
- The file names also include the name of the algorithm used.
- Finally, the duration for which the algorithm was looped (in minutes) is indicated in the file name.

For example, a file named `p1_simulated_120min.csv` represents the results for:
- Protein sequence 1 (`p1`),
- Using the simulated annealing algorithm,
- Looped for 120 minutes.


To reproduce the results, follow these steps:

1. **Prepare a CSV File**  
   First, create a CSV file in the `results` directory to store the output data.

2. **Run the Main Program**  
   Execute the program by running `python3 main.py`. The main program will present you with five different algorithms to choose from:

   ```
   1. Random Folding
   2. Hillclimber
   3. Greedy Folding
   4. Beam Search Folding
   5. Simulated Annealing Folding
   ```

3. **Choose an Algorithm**  
   Select the algorithm for which you want to reproduce results.
   ```
   Enter your choice (1, 2 ,3 ,4 or 5):
   ```


4. **Choose a Protein Sequence**  
   After selecting an algorithm, you will be prompted to choose a protein sequence. The available sequences are:
   
   ```
   1  HHPHHHPH
   2  HHPHHHPHPHHHPH
   3  HPHPPHHPHPPHPHHPPHPH
   4  PPPHHPPHHPPPPPHHHHHHHPPHHPPPPHHPPHPP
   5  HHPHPHPHPHHHHPHPPPHPPPHPPPPHPPPHPPPHPHHHHPHPHPHPHH
   6  PPCHHPPCHPPPPCHHHHCHHPPHHPPPPHHPPHPP
   7  CPPCHPPCHPPCPPHHHHHHCCPCHPPCPCHPPHPC
   8  HCPHPCPHPCHCHPHPPPHPPPHPPPPHPCPHPPPHPHHHCCHCHCHCHH
   9  HCPHPHPHCHHHHPCCPPHPPPHPPPPCPPPHPPPHPHHHHCHPHPHPHH
   10 Enter your own sequence.
   ```

   Select the protein sequence for which you want to reproduce results.
   
   ```
   Enter a number between 1 and 9 to select the sequence:
   ```

5. **Specify the Output File**  
   Enter the name of the file where the data should be saved. This file must be the same one you created in step 1.

6. **Choose an Execution Mode**  
   After specifying the output file, the program will present you with two options:
   
   ```
   1 Single Run
   2 Loop Algorithm
   ```

    1 : For this option, depending on the algorithm chosen, the program will ask you to input specific parameters.
    
    2 : For this option, the program will ask how many minutes you want the algorithm to run in a loop.
    
7. **Choose Stability, Visualizer, or Both**  
   After the program is done running, it will present you with three options:
   
   ```
   1 Stability
   2 Visualizer
   3 Both 
   ```

    1 : For this option, the program will print the stability score in the terminal.

    2 : For this option, the program will plot the protein sequence.

    3 : The program will perform both actions.

8. **Create distribution, graph or histogram plot**   

   Once the results have been saved in the chosen CSV file, you can visualize them using the `csv_to_distribution`, `csv_to_graph`, or `csv_to_histogram` functions.

   Each of these functions operates similarly in generating plots, so we will explain one as an example. To create a graph, navigate to the `csv_to_graph` function inside the `visualisation` folder. 

   1. Open the script and locate the **main section**.
   2. Assign the CSV filename to the `csv_file` variable.
   3. In the `csv_graph.plot()` method, specify the columns for the x-axis and y-axis. The names of the columns are saved at the top of the csv files.
   4. In the terminal run `python3 -m code.visualisation.csv_to_graph`

   This same approach applies to the distribution and histogram functions, allowing you to easily visualize your results in different ways.

Follow these steps to reproduce the results accurately.
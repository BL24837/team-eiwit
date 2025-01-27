# Protein Folding Optimization

This project focuses on optimizing protein folding using a different algorithm. Proteins in this project consist of three types of amino acids: hydrophobic amino acids (H), polar amino acids (P), and cysteine (C). These amino acids can be folded around each other to form a compact structure.

The strength of the protein structure is determined by the stability score, which is calculated based on bonds between specific amino acids:
- **H-H bonds**: Contribute a stability of `-1`.
- **C-H or C-C bonds**: Contribute a stronger stability of `-5`.

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
After running this code you have to choose which algorithm you want to run.

### Select algorithm
Select folding algorithm:
1: Random Folding
2: Hillclimber
3: Greedy Folding
4: Beam Search
5: Simmulated Annealing
```Enter your choice (1, 2, 3, 4 or 5): into your terminal```

After choosing your algorithm, the program presents you 10 different options. Nine options are the standard protein sequences and the tenth option is a sequence you can choose by yourself.
### Select protein sequence
Choose a sequence:
1: HHPHHHPH
2: HHPHHHPHPHHHPH
3: HPHPPHHPHPPHPHHPPHPH
4: PPPHHPPHHPPPPPHHHHHHHPPHHPPPPHHPPHPP
5: HHPHPHPHPHHHHPHPPPHPPPHPPPPHPPPHPPPHPHHHHPHPHPHPHH
6: PPCHHPPCHPPPPCHHHHCHHPPHHPPPPHHPPHPP
7: CPPCHPPCHPPCPPHHHHHHCCPCHPPCPCHPPHPC
8: HCPHPCPHPCHCHPHPPPHPPPHPPPPHPCPHPPPHPHHHCCHCHCHCHH
9: HCPHPHPHCHHHHPCCPPHPPPHPPPPCPPPHPPPHPHHHHCHPHPHPHH
10: Enter your own sequence

### Enter filename

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

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
Before running the program insert the right protein sequence inside the main.py file. Then run this code:
```
python3 main.py
```
OR
```
python main.py
```
After running this code you have to discide which algorithm you want to run.

### Select algorithm
Select folding algorithm:
1: Random Folding
2: Hillclimber
3: Greedy Folding
```Enter your choice (1, 2 or 3): into your terminal```




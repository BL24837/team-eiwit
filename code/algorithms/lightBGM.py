import lightgbm as lgb
import numpy as np
import pandas as pd
import random
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from code.classes.protein import Protein
from code.algorithms.random_algorithm import RandomFolding
import matplotlib.pyplot as plt

class LightGBMFolding:
    def _init_(self, data:DataStoring ,protein: Protein , random_folding_iterations=1000, test_size=0.2, num_leaves=31, learning_rate=0.1, n_estimators=100):
        """
        Initialize the LightGBMFolding class with parameters.
        """
        self.data = data
        self.protein = protein
        self.random_folding_iterations = random_folding_iterations
        self.test_size = test_size
        self.num_leaves = num_leaves
        self.learning_rate = learning_rate
        self.n_estimators = n_estimators
        self.model = None
        self.stabilities = []

    def generate_training_data(self):
        """
        Generate training data using random folding iterations.
        Returns feature matrix X and target vector y.
        """
        features = []
        stabilities = []

        random_folding = RandomFolding(self.protein)

        for _ in range(self.random_folding_iterations):
            # Geef hier het iterations-argument door aan execute()
            folded_protein = random_folding.execute(iterations=self.random_folding_iterations)
            stability = folded_protein.calculate_stability()
            feature_vector = self.extract_features(folded_protein)
            
            features.append(feature_vector)
            stabilities.append(stability)

        self.stabilities = stabilities
        return np.array(features), np.array(stabilities)

    def extract_features(self, protein: Protein):
        """
        Extract features from a protein configuration.
        Features can include distances, angles, and other structural information.
        """
        # Example features: length, count of hydrophobic/hydrophilic amino acids, etc.
        length = len(protein.sequence)
        hydrophobic_count = sum(1 for aa in protein.sequence if aa in 'AILMFWYV')
        hydrophilic_count = length - hydrophobic_count

        # Add more complex features as needed
        return [length, hydrophobic_count, hydrophilic_count]

    def train_model(self):
        """
        Train a LightGBM model on the generated dataset.
        """
        print("Generating training data...")
        X, y = self.generate_training_data()
        
        print("Splitting data into train and test sets...")
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=self.test_size, random_state=42)
        
        print("Training LightGBM model...")
        self.model = lgb.LGBMRegressor(
            num_leaves=self.num_leaves,
            learning_rate=self.learning_rate,
            n_estimators=self.n_estimators
        )
        self.model.fit(X_train, y_train, eval_set=[(X_test, y_test)], eval_metric='l2', verbose=True)

        print("Evaluating model...")
        predictions = self.model.predict(X_test)
        mse = mean_squared_error(y_test, predictions)
        print(f"Mean Squared Error: {mse}")

    def predict_best_folding(self):
        """
        Predict the best folding configuration based on the trained model.
        """
        print("Generating potential configurations...")
        potential_configurations = [
            RandomFolding(self.protein).execute(iterations=self.random_folding_iterations) for _ in range(self.random_folding_iterations)
        ]

        print("Extracting features and predicting stability...")
        features = np.array([self.extract_features(protein) for protein in potential_configurations])
        predictions = self.model.predict(features)

        best_index = np.argmin(predictions)
        best_protein = potential_configurations[best_index]

        print(f"Best predicted stability: {predictions[best_index]}")

        # Show the stability distribution only when returning the result

        return best_protein

    def plot_stability_distribution(self):
        """
        Plot the distribution of stabilities observed during the training process.
        """
        plt.figure(figsize=(10, 6))
        plt.hist(self.stabilities, bins=30, alpha=0.7, color='blue', edgecolor='black')
        plt.title("Distribution of Protein Stabilities")
        plt.xlabel("Stability")
        plt.ylabel("Frequency")
        plt.grid(True)
        plt.show()
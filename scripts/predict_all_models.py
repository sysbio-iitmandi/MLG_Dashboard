import pandas as pd
import xgboost as xgb
import pickle
import sys

# Get command line arguments
model_file = sys.argv[1]
data_file = sys.argv[2]
output_file = sys.argv[3]


# Load the model, scaler, and feature names from the pickle file
with open(model_file, 'rb') as f:
    model, scaler, feature_names = pickle.load(f)

# Load the test dataset
test_dataset = pd.read_csv(data_file, index_col='Assembly Accession')

# Ensure the test data has the same feature names
X_test = test_dataset[feature_names]

# Scale the features
X_test_scaled = scaler.transform(X_test)

# Predict the dataset using the classifier
predictions = model.predict(X_test_scaled)

# Get prediction probabilities
probabilities = model.predict_proba(X_test_scaled)
non_prob = probabilities[:, 0]
prob = probabilities[:, 1]

# Round the probabilities
rounded_prob = [round(p, 2) for p in prob]
rounded_non_prob = [round(p, 2) for p in non_prob]


# Create a DataFrame with Assembly Accession and Predicted Category
categories = ["Non-Probiotic", "Probiotic"]
results = pd.DataFrame({
    'Assembly Accession': X_test.index,
    'Predicted Category': [categories[round(pred)] for pred in predictions],
    'Probiotic Probability': rounded_prob,
    'Non-Probiotic Probability': rounded_non_prob   
})

# Save the predictions to a CSV file
results.to_csv(output_file, index=False)
import sys
import os
import pandas as pd
import xgboost as xgb
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, confusion_matrix
import pickle


#Initializing the variables
kmer_matrix = sys.argv[1]
split_int = float(sys.argv[2])
output_predictions = 'Training_predictions.csv'
output_model = 'XGB_trained_model.pkl'

#Removing the output files, if they exist
if os.path.exists(output_predictions):
    os.remove(output_predictions)

if os.path.exists(output_model):
    os.remove(output_model)

print("Training with XGBoost")
print(f"Test data size: {split_int}")

# Load the data
dataset = pd.read_csv(kmer_matrix, index_col='Assembly Accession')

# Separate features and target
X = dataset.drop(columns=['Category'])
y = dataset['Category']

# Encode the target variable
label_encoder = preprocessing.LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=split_int, random_state=0)

# Scale the features
scaler = preprocessing.StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train the XGBoost model
model = xgb.XGBClassifier(use_label_encoder=False, eval_metric='logloss')
model.fit(X_train_scaled, y_train)

# Make predictions
y_pred = model.predict(X_test_scaled)

# Evaluate the model
cm = confusion_matrix(y_test, y_pred)
tn, fp, fn, tp = cm.ravel()

print("TP = ", tp)
print("FP = ", fp)
print("TN = ", tn)
print("FN = ", fn)

accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy:.2f}')

fscore = f1_score(y_test, y_pred)
print(f'F1 Score: {fscore:.2f}')

precision = precision_score(y_test, y_pred)
print(f'Precision: {precision:.2f}')

recall = recall_score(y_test, y_pred)
print(f'Recall: {recall:.2f}')

# Create a DataFrame with index, actual, and predicted labels
results = pd.DataFrame({
    'Index': X_test.index,
    'Actual': label_encoder.inverse_transform(y_test),
    'Predicted': label_encoder.inverse_transform(y_pred)
})

# Save the results to a CSV file
results.to_csv(output_predictions, index=False)

if os.path.exists(output_predictions):
    print(f"Training predictions: {output_predictions}")
else:
    print("Could not write predictions to file")

# Save model, scaler, and feature names to a file using pickle
with open(output_model, 'wb') as f:
    pickle.dump((model, scaler, X.columns.tolist()), f)

if os.path.exists(output_model):
    print(f'Trained model: {output_model}')
else:
    print("Could not dump the model")

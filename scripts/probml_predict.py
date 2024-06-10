import pandas as pd
from scipy.special import expit
import xgboost as xgb
import sys

#sys.argv list:

#$1 model json
#$2 csv matrix
#$3 top features file
#$4 output filename



# Load the classifier model from the json file

#change
classifier = xgb.Booster(model_file=sys.argv[1])

test_dataset = pd.read_csv(sys.argv[2], index_col = 'Assembly Accession')

assembly_accessions = test_dataset.index

#change
# Open the file in read mode
with open(sys.argv[3], 'r') as file:
    # Read the content of the file
    imp_features = file.read().split()

test_dataset = test_dataset[imp_features]
predictions = classifier.predict(xgb.DMatrix(test_dataset))

# Predict raw margin values to calculate probabilities
raw_predictions = classifier.predict(xgb.DMatrix(test_dataset), output_margin=True)

# Convert to probabilities (This tells probability of being probiotic)
probabilities = expit(raw_predictions)


text_to_write = "Assembly Accession,Predicted Category,Probability of probiotic, Probability of non-probiotic\n"

categories = ["Non-probiotic", "Probiotic"]

for i in range(len(test_dataset)):
    text_to_write += str(assembly_accessions[i]) + "," + categories[round(predictions[i])] + "," + str(round(probabilities[0], 2)) + "," + str(round(1-probabilities[0], 2)) + "\n"


#change
# Specify the file path and mode ('w' for write)
file_path = sys.argv[4]

# Open the file for writing
with open(file_path, 'w') as file:
    # Write the string to the file
    file.write(text_to_write)

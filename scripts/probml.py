import os
import sys
import subprocess
import random
import glob


# Initializing variables
model = sys.argv[1]
file_path = 'tmp/file_path.txt'
output_file = 'ProbML_results.csv'
kmers = 'tmp/kmers.csv'

# Remove the output and kmers file
if os.path.isfile(output_file):
    os.remove(output_file)

if os.path.isfile(kmers):
    os.remove(kmers)



# Read file paths from file
with open(file_path, 'r') as f:
    files = f.read().splitlines()

min_kmer_value = 2
max_kmer_value = 8
min_kmer_value_str = str(min_kmer_value)
max_kmer_value_str = str(max_kmer_value)


# Print model information
print(f"Model: XGB-SB-IITM {model}\nNo. of genomes: {len(files)}")


# Invoke kmer generation script
subprocess.run(["python", "scripts/f2m.py", min_kmer_value_str, max_kmer_value_str, "probml", kmers, file_path])

model = model.replace(" ", "")

# Choose the model
if model == "Random":
    # Randomly choose a number between 1 and 12
    randnum = random.randint(1, 12)
    xgboost = f"models/Model{randnum}.json"
    top_features = f"models/TF_Model{randnum}.txt"
    print(f"Classifying with {xgboost}")
else:
    # Use specified model
    xgboost = f"models/{model}.json"
    top_features = f"models/TF_{model}.txt"
    print(f"Classifying with {xgboost}")

# Invoke prediction script
subprocess.run(['python', 'scripts/probml_predict.py', xgboost, kmers, top_features, output_file])

# Check if results file exists and process the results
if os.path.isfile(output_file):
    with open(output_file, 'r') as results_file:
        lines = results_file.readlines()
        for line in lines:
            if 'Assembly Accession' not in line:
                print(line.strip())
else:
    print("Results not generated")


if os.path.isfile(file_path):
    os.remove(file_path)

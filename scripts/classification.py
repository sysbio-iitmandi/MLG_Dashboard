import os
import sys
import subprocess

# Get command line arguments
model_path = sys.argv[1]
minK = int(sys.argv[2])
maxK = int(sys.argv[3])
input_file = "tmp/file_path.txt"
output_file = "Classifier_predictions.csv"
kmers = "tmp/kmers.csv"

#remove the output file and kmer file
if os.path.isfile(output_file):
    os.remove(output_file)

if os.path.isfile(kmers):
    os.remove(kmers)

# Determine model type
model_basename = os.path.basename(model_path)
if model_basename.startswith("XGB"):
    model = "XGB"
elif model_basename.startswith("RF"):
    model = "RF"
else:
    model = None


# Invoke kmer generation script
subprocess.run(["python", "scripts/f2m.py", str(minK), str(maxK), "probml", kmers, input_file])


# Invoke prediction
print(f"Classifying with {os.path.basename(model_path)}")
subprocess.run(["python", "scripts/predict_all_models.py", model_path, kmers, output_file])


# Display results if generated
if os.path.isfile(output_file):
    print(f"Results: {output_file}")
    with open(output_file, "r") as results_file:
        for line in results_file:
            if "Assembly Accession" not in line:
                print(line.rstrip())
else:
    print("Results not generated")


#remove the kmer matrix
if os.path.isfile(output_file):
    os.remove(input_file)



import sys
import os
import pandas as pd
import subprocess

# Getting arguments from the command line
model = sys.argv[1]
positive = sys.argv[2]
negative = sys.argv[3]
split = sys.argv[4]

model_path = f"scripts/{model}.py"

output_file =  "tmp/dataset.csv"

# Reading the positive and negative datasets
positive_df = pd.read_csv(positive)
negative_df = pd.read_csv(negative)

# Concatenating the positive and negative datasets
combined_df = pd.concat([positive_df, negative_df], ignore_index=True)

# Saving the combined dataset to the output file
combined_df.to_csv(output_file, index=False)

# Adjusting the dataset split values
split_int = 0.5  # Default value in case of an invalid split string

if split == "50:50":
    split_int = 0.5
elif split == "60:40":
    split_int = 0.6
elif split == "70:30":
    split_int = 0.7
elif split == "80:20":
    split_int = 0.8
elif split == "90:10":
    split_int = 0.9
else:
    sys.stderr.write(f"Invalid split value: {split}\n")
    sys.exit(1)


# Running the model script with the dataset and split_int
subprocess.run(["python", model_path, output_file, str(split_int)])

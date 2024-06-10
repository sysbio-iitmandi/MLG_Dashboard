#!/usr/bin/env python
import sys
import math
import os

#############################################################################


def make_kmer_list(k, alphabet):
    if k == 1:
        return alphabet
    if k == 0:
        return []
    if k < 1:
        sys.stderr.write("Invalid k=%d" % k)
        sys.exit(1)

    alphabet_length = len(alphabet)
    return_value = []
    for kmer in make_kmer_list(k - 1, alphabet):
        for i_letter in range(0, alphabet_length):
            return_value.append(kmer + alphabet[i_letter])

    return return_value

##############################################################################
def make_upto_kmer_list(min_k, max_k, alphabet):
    return_value = []
    for k in range(min_k, max_k + 1):
        return_value.extend(make_kmer_list(k, alphabet))
    return return_value

##############################################################################
def normalize_vector(normalize_method, k_values, vector, kmer_list):
    if normalize_method == "none":
        return vector

    vector_lengths = {}
    for k in k_values:
        vector_lengths[k] = 0

    num_kmers = len(kmer_list)
    for i_kmer in range(0, num_kmers):
        kmer_length = len(kmer_list[i_kmer])
        count = vector[i_kmer]
        if normalize_method == "frequency":
            vector_lengths[kmer_length] += count
        elif normalize_method == "unitsphere":
            vector_lengths[kmer_length] += count * count

    if normalize_method == "unitsphere":
        for k in k_values:
            vector_lengths[k] = math.sqrt(vector_lengths[k])

    return_value = []
    for i_kmer in range(0, num_kmers):
        kmer_length = len(kmer_list[i_kmer])
        count = vector[i_kmer]
        vector_length = vector_lengths[kmer_length]
        if vector_length == 0:
            return_value.append(0)
        else:
            return_value.append(float(count) / float(vector_length))

    return return_value

##############################################################################
def make_sequence_vector(sequence, normalize_method, k_values, alphabet, kmer_list):
    kmer_counts = {}

    for k in k_values:
        seq_length = len(sequence) - k + 1
        for i_seq in range(0, seq_length):
            kmer = sequence[i_seq: i_seq + k]
            if kmer in kmer_counts:
                kmer_counts[kmer] += 1
            else:
                kmer_counts[kmer] = 1

    sequence_vector = []
    for kmer in kmer_list:
        if kmer in kmer_counts:
            sequence_vector.append(kmer_counts[kmer])
        else:
            sequence_vector.append(0)

    return normalize_vector(normalize_method, k_values, sequence_vector, kmer_list)

##############################################################################
def read_fasta_sequence(fasta_file):
    first_char = fasta_file.read(1)
    if first_char == "":
        return ["", ""]
    elif first_char == ">":
        line = ""
    else:
        line = first_char

    line = line + fasta_file.readline()
    words = line.split()
    if len(words) == 0:
        sys.stderr.write("No words in header line (%s)\n" % line)
        sys.exit(1)
    id = '_'.join(words).replace(',', '_')

    first_char = fasta_file.read(1)
    sequence = ""
    while first_char != ">" and first_char != "":
        if first_char != "\n":
            line = fasta_file.readline()
            sequence = sequence + first_char + line
        first_char = fasta_file.read(1)

    clean_sequence = ""
    for letter in sequence:
        if letter != "\n":
            clean_sequence = clean_sequence + letter
    sequence = clean_sequence

    clean_sequence = ""
    for letter in sequence:
        if letter != " ":
            clean_sequence = clean_sequence + letter
    sequence = clean_sequence.upper()

    return [id, sequence]

##############################################################################
def combine_lists(*lists):
    combined_list = []
    min_length = min(len(lst) for lst in lists)
    for i in range(min_length):
        combined_element = sum(lst[i] for lst in lists)
        combined_list.append(combined_element)
    return combined_list

##############################################################################
# MAIN
##############################################################################

usage = """Usage: fasta2matrix [options] <min_k> <max_k> <category_label>

  Options:
    -normalize [frequency|unitsphere] Normalize counts to be 
                frequencies or project onto unit sphere.
"""

normalize_method = "none"
alphabet = "ACGT"

sys.argv = sys.argv[1:]
while len(sys.argv) > 5:
    next_arg = sys.argv[0]
    sys.argv = sys.argv[1:]
    if next_arg == "-normalize":
        normalize_method = sys.argv[0]
        sys.argv = sys.argv[1:]
        if normalize_method not in ["unitsphere", "frequency"]:
            sys.stderr.write("Invalid normalization method (%s).\n" % normalize_method)
            sys.exit(1)
    else:
        sys.stderr.write("Invalid option (%s)\n" % next_arg)
        sys.exit(1)
if len(sys.argv) != 5:
    sys.stderr.write(usage)
    sys.exit(1)

min_k = int(sys.argv[0])
max_k = int(sys.argv[1])

category_label = sys.argv[2]
output_file_path = sys.argv[3] 
file_path_txt = sys.argv[4]

k_values = range(min_k, max_k + 1)
kmer_list = make_upto_kmer_list(min_k, max_k, alphabet)



# Print the title row.
# sys.stdout.write("Assembly Accession,Category")
# num_bins = 1  # Default to 1 if not specified
# for i_bin in range(1, num_bins + 1):
#     for kmer in kmer_list:
#         if num_bins > 1:
#             sys.stdout.write("\t%s-%d" % (kmer, i_bin))
#         else:
#             sys.stdout.write(",%s" % kmer)
# sys.stdout.write("\n")



with open(output_file_path, 'w') as output_file:
    # Print the title row.
    output_file.write("Assembly Accession,Category")
    num_bins = 1  # Default to 1 if not specified
    for i_bin in range(1, num_bins + 1):
        for kmer in kmer_list:
            if num_bins > 1:
                output_file.write("\t%s-%d" % (kmer, i_bin))
            else:
                output_file.write(",%s" % kmer)
    output_file.write("\n")

    try:
        with open(file_path_txt, 'r') as file_path_file:
            file_paths = file_path_file.read().splitlines()
            for file_path in file_paths:
                if file_path == "":
                    continue
                fasta_file = open(file_path, "r")
                [id, sequence] = read_fasta_sequence(fasta_file)
                i_sequence = 1

                vectors = []
                vectors.append(kmer_list)

                while id != "":
                    vector = make_sequence_vector(sequence, normalize_method, k_values, alphabet, kmer_list)
                    vectors.append(vector)
                    [id, sequence] = read_fasta_sequence(fasta_file)
                    i_sequence += 1

                fasta_file.close()
                combined = combine_lists(*vectors[1:])
                output_file.write("_".join(file_path.split('/')[-1].split('_')[:2]) + "," + category_label + "," + ",".join(map(str, combined)) + "\n")
    except IOError:
        sys.stderr.write("Error: File not found or cannot be opened: %s\n" % file_path_txt)
        sys.exit(1)

if os.path.isfile(output_file_path):
    print(f'Kmer matrix generated: {output_file_path}')

if os.path.isfile('kmer/file_path.txt'):
    os.remove('kmer/file_path.txt')

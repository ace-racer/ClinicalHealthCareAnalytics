import numpy as np
import pandas as pd
import random


input_file_location = "ModelOutputs/bala/p2 - Bala.csv"

# read the details from the CSV input
input_df = pd.read_csv(input_file_location, header=0)

# Get model names (other than the first column)
model_names = list(input_df.columns.values)[1:]

num_models = len(model_names)

output_content = "Models," + ",".join(model_names) + "\n"


def compute_jaccard_distance(m1, m2):
    if m1 is not None and m2 is not None:
        same_and_one = 0
        differents = 0
        for itr in range(len(m1)):
            if (m1[itr] == m2[itr]) and m1[itr] == 1:
                same_and_one += 1
            elif m1[itr] != m2[itr]:
                differents += 1
        
        return differents/(differents + same_and_one)
    raise ValueError("Both models to be present")


for itr in range(0, num_models):
    output_content += model_names[itr] + ","
    for jtr in range(0, num_models):
        print("Calculating distance between {0} and {1}".format(model_names[itr], model_names[jtr]))

        # The columns in the data frame start from 1
        distance = compute_jaccard_distance(input_df.iloc[:, itr + 1], input_df.iloc[:, jtr + 1])
        output_content += str(distance) + ","
        print("Distance = {0}".format(str(distance)))
    output_content += "\n"

with open("output/jaccard_distances_" + input_file_location.replace("/", "_"), "w") as fw:
    fw.writelines(output_content)


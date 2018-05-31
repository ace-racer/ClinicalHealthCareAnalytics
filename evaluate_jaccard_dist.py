import numpy as np
import pandas as pd
import random
from sklearn.metrics import jaccard_similarity_score


# read the details from the CSV input
input_df = pd.read_csv("data/combined.csv", header=0)

# Get model names (other than the first column)
model_names = list(input_df.columns.values)[1:]

num_models = len(model_names)

output_content = "Models," + ",".join(model_names) + "\n"

for itr in range(0, num_models):
    output_content += model_names[itr] + ","
    for jtr in range(0, num_models):
        print("Calculating distance between {0} and {1}".format(model_names[itr], model_names[jtr]))

        # The columns in the data frame start from 1
        score = jaccard_similarity_score(input_df.iloc[:, itr + 1], input_df.iloc[:, jtr + 1])
        output_content += str(1-score) + ","
        print("Distance = {0}".format(str(1-score)))
    output_content += "\n"

with open("output/jaccard_distances_" + str(random.randint(1, 10000000)) + ".csv", "w") as fw:
    fw.writelines(output_content)


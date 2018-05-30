import numpy as np
import pandas as pd
import random
from sklearn.metrics import jaccard_similarity_score


# read the details from the CSV input
input_df = pd.read_csv("data/model_performance.csv", header=0)

# Get model names (other than the first column)
model_names = list(input_df.columns.values)[1:]

num_models = len(model_names)

output_content = ",".join(model_names) + "\n"

for itr in range(0, num_models):
    for jtr in range(0, num_models):
        score = jaccard_similarity_score(input_df.iloc[:, itr], input_df.iloc[:, jtr])
        output_content += str(1-score) + ","
    output_content += "\n"

with open("output/jaccard_distances_" + str(random.randint(1, 10000000)) + ".csv", "w") as fw:
    fw.writelines(output_content)


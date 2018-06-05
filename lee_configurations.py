columns_to_remove = ["encounter_id", "readmitted2"]
identity_output_columns = ["encounter_id", "readmitted2"]
target_column_name = "readmitted2"
input_file_location = "ModelOutputs/lee/model_output_p2(Lee).csv"
ensemble_count = 5
models_always_include = ["RandomTrees",  "BayesNet"]
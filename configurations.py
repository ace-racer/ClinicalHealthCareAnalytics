columns_to_remove = ["encounter_id", "readmitted2", "LR2 #16", "DT-Chaid_2 #17"]
identity_output_columns = ["encounter_id", "readmitted2"]
target_column_name = "readmitted2"
input_file_location = "data/p2_results.csv"
best_model = "DT-C5.0"
model_with_greatest_J_dist = "NB-TAN"

import pandas as pd

df = pd.read_csv("data/model_outputs.csv", header=0)
target = "readmitted2"
count = 3

def majority_voting(*args):
    if args and len(args) >= 3:
        print("Getting predictions from: " + str(args[-1]))
        args = args[:-1]
        predictions = []
        for itr in range(len(args[0])):
            predicted_vals_sum = 0
            for arg in args:
                predicted_vals_sum += arg[itr]

            if predicted_vals_sum >= (count // 2) + 1:
                predictions.append(1)
            else:
                predictions.append(0)


    return predictions

def compare_predictions(ensemble_predictions, actual_values, selected_models):
    total_predictions = len(actual_values)
    corrects = 0
    correct_1 = 0
    correct_0 = 0
    total_actual_1 = 0
    total_actual_0 = 0
    for itr in range(len(actual_values)):
        if ensemble_predictions[itr] == actual_values[itr]:
            corrects += 1
            if ensemble_predictions[itr] == 0:
                correct_0 += 1
                total_actual_0 += 1
            else:
                correct_1 += 1
                total_actual_1 += 1
        else:
            if actual_values[itr] == 0:
                total_actual_0 += 1
            else:
                total_actual_1 += 1
    
    print("{0}, {1}, {2} for {4}".format(corrects / total_predictions, correct_0 / total_actual_0, correct_1 / total_actual_1, selected_models))
    return (corrects / total_predictions, correct_0 / total_actual_0, correct_1 / total_actual_1, selected_models)



readmitted_df = df[["encounter_id", "readmitted2"]]
print(readmitted_df)
df = df.drop(["encounter_id", "readmitted2", "LR2", "DT-CHAID-2"], axis=1)

models = df.columns.values
print("Num models: " + str(len(models)))

all_predictions_results = []
for itr in range(len(models)):
    for jtr in range(itr + 1, len(models)):
        for ktr in range(jtr + 1, len(models)):
            print("Evaluating models {0}, {1} and {2}".format(models[itr], models[jtr], models[ktr]))
            predictions_A = df[models[itr]]
            predictions_B = df[models[jtr]]
            predictions_C = df[models[ktr]]
            selected_models = "{0}, {1} and {2}".format(models[itr], models[jtr], models[ktr])
            predictions = majority_voting(predictions_A, predictions_B, predictions_C, selected_models)
            all_predictions_results.append(compare_predictions(readmitted_df[target], predictions, selected_models))
        break
    break

all_predictions_results = sorted(all_predictions_results, key=lambda x: x[0], reverse = True)
print(all_predictions_results)

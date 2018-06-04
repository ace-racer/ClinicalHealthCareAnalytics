import pandas as pd
import itertools
import lee_configurations as configurations

df = pd.read_csv(configurations.input_file_location, header=0)
target = configurations.target_column_name
count = configurations.ensemble_count


def one_vs_rest(model_names, *args):
    if args and len(args) >= 3:
        print("One vs rest: " + model_names)
        main_model_predictions = args[0]

        args = args[1:]
        predictions = []
        for itr in range(len(main_model_predictions)):
            rest_predictions = 0
            prediction = 0
            for arg in args:
                rest_predictions += arg[itr]
                prediction = arg[itr]
            
            # if the rest agree
            if rest_predictions == 0 or rest_predictions == (count - 1):
                predictions.append(prediction)
            else:
                predictions.append(main_model_predictions[itr])

    return predictions



def majority_voting(models_selected, current_model_combination_predictions):
    if models_selected and current_model_combination_predictions is not None:
        num_models = len(current_model_combination_predictions)
        print("Getting ensemble predictions for: " + models_selected)
        print("Num models: " + str(len(current_model_combination_predictions)))
        
        predictions = []
        for itr in range(len(current_model_combination_predictions[0])):
            predicted_vals_sum = 0
            for current_model_combination_prediction in current_model_combination_predictions:
                predicted_vals_sum += current_model_combination_prediction[itr]

            if predicted_vals_sum >= (num_models // 2) + 1:
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
    
    print("{0}, {1}, {2} for {3}".format(corrects / total_predictions, correct_0 / total_actual_0, correct_1 / total_actual_1, selected_models))
    return (corrects / total_predictions, correct_0 / total_actual_0, correct_1 / total_actual_1, selected_models)



readmitted_df = df[configurations.identity_output_columns]
print(readmitted_df)
df = df.drop(configurations.columns_to_remove, axis=1)

models = list(df.columns.values)

# remove the models to always include from the model pool
for model in configurations.models_always_include:
    models.remove(model)

combinations_count = count - len(configurations.models_always_include)
print("Combinations: " + str(combinations_count))
print("Num models: " + str(len(models)))
all_predictions_results = []
print(models)
all_combinations = itertools.combinations(models, combinations_count)

for combination in all_combinations:
    models_selected = ""
    current_model_combination_predictions = []
    models_to_evaluate = list(combination) + configurations.models_always_include
    for model in models_to_evaluate:
        models_selected += model + ", "
        model_predictions = df[model]
        current_model_combination_predictions.append(model_predictions)
    
    print(models_selected)
    ensemble_predictions = majority_voting(models_selected, current_model_combination_predictions)
    # ensemble_predictions = one_vs_rest(selected_models, predictions_A, predictions_B, predictions_C)
    all_predictions_results.append(compare_predictions(readmitted_df[target], ensemble_predictions, models_selected))

all_predictions_results = sorted(all_predictions_results, key=lambda x: x[0], reverse = True)
print(all_predictions_results)
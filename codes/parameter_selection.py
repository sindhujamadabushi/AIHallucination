import pandas as pd

# Define a function to analyze the impact of each parameter on the Count value
def analyze_parameter_impact(file_path):
    # Load the CSV file into a pandas DataFrame
    df = pd.read_csv(file_path)

    # Define the parameter names
    parameters = ['Temperature', 'Frequency Penalty', 'Presence Penalty', 'Top P']

    # Initialize a dictionary to store the results
    results = {}

    # Loop through each parameter and calculate the total Count per unique value of that parameter
    for parameter in parameters:
        # Group by the current parameter and sum the Count values
        group_sum = df.groupby(parameter)['Count'].sum().reset_index()

        # Add the group sum DataFrame to the results dictionary
        results[parameter] = group_sum

    # Return the results
    return results

# Files to analyze
file_paths = [
    './hallucination_analysis_results/count_LLM_Evaluation_hallucination_distribution.csv',
    './hallucination_analysis_results/yesno_LLM_Evaluation_hallucination_distribution.csv'
]

# Analyze each file and store results
file_results = {}
for file_path in file_paths:
    file_results[file_path] = analyze_parameter_impact(file_path)

# Output the results for further inspection or analysis
for file_path, results in file_results.items():
    print(f"Results for {file_path}:")
    for parameter, result_df in results.items():
        print(f"\nParameter: {parameter}")
        print(result_df)
    print("\n" + "-"*50 + "\n")

# The script should be adjusted to match the actual file paths.
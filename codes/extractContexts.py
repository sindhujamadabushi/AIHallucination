# Retry the operation due to the previous exception
import json

# Load the provided JSON file
file_path = '/Users/sindhuja/Desktop/AIHallucination/results/questions/generated2/context_0.json'

try:
    with open(file_path, 'r') as file:
        data = json.load(file)

    # Extract the first 128 dictionaries from the 'count_variations' key
    first_128_dictionaries = data['count_variations'][0]
    

    # Save the extracted data to a new JSON file
    output_file_path = 'first_128_dictionaries.json'
    with open(output_file_path, 'w') as output_file:
        json.dump(first_128_dictionaries, output_file, indent=4)

    output_file_path
except Exception as e:
    error_message = str(e)
    error_message



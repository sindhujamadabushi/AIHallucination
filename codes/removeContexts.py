import os
import json

def modify_context(input_path, output_path, file_num):
    # Construct file names based on the file number
    input_file = os.path.join(input_path, f"context_{file_num}.json")
    output_file = os.path.join(output_path, f"nocontext_{file_num}.json")

    with open(input_file, 'r') as file:
        data = json.load(file)
    # Replace context with an empty string
    data['context'] = ""

    # Create a directory for questions
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    with open(output_file, 'w') as file:
        json.dump(data, file, indent=4)

input_file_path = '../results/questions/context/'  
output_file_path = '../results/questions/nocontext/'  
num_contexts = 5

# Process files from context_0.json to context_100.json
for i in range(num_contexts):
    modify_context(input_file_path, output_file_path, i)


# import json

# #Function to get contexts from the SQuAD dataset. 
# #Outputs gert stored in contexts.txt in the input folder
# def get_context_from_dataset(dataset_path):
#     # Initialize an empty list to store contexts
#     contexts = []

#     # Load JSON data from input file
#     with open(dataset_path, 'r') as f:
#         data = json.load(f)

#     # Iterate through the data to extract contexts
#     for topic in data['data']:
#         for paragraph in topic['paragraphs']:
#             contexts.append(paragraph['context'])

#     with open("../inputs/contexts.txt", "w") as f:
#         for item in contexts:
#             f.write(f"{item}\n")
    
#     return 

# # Function to extract every 100th context and save to a new file
# def extract_contexts(input_file_path, output_file_path, step=100):
#     with open(input_file_path, 'r') as input_file:
#         contexts = input_file.readlines()
    
#     # Extract every 100th context
#     extracted_contexts = contexts[::step]

#     # Write the extracted contexts to the output file
#     with open(output_file_path, 'w') as output_file:
#         for context in extracted_contexts:
#             output_file.write(context)


# input_file_path = '../inputs/contexts.txt'
# output_file_path = '../inputs/contexts_100.txt'
# dataset_path = '../inputs/train-v2.0.json'

# #Get contexts from dataset
# get_context_from_dataset(dataset_path)

# # Extract 100 contexts and save contexts
# extract_contexts(input_file_path, output_file_path)



from itertools import product
num_questions = 2
paraphrased_questions = []
T = [1.2, 1.4, 1.6, 1.8]
FP = [1.2, 1.4, 1.6, 1.8]
PP = [1.2, 1.4, 1.6, 1.8]
top_p = [0.92, 0.95]

for parameters in product(T, FP, PP, top_p):
    print(parameters)
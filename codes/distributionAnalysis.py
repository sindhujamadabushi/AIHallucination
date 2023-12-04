import os
import json
import csv
from collections import defaultdict
from loadDataset import LoadDataset

def load_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

# def prune_questions():
#     file_base_path = '/Users/sindhuja/Desktop/AIHallucination/results/questions/generated2/context_'
#     file_count = 22  
#     total_nan_count = 0
#     total_unknown_count = 0
#     for i in range(file_count):
#         file_path = f'{file_base_path}{i}.json'
#         nan_count = 0
#         unknown_count = 0
#         with open(file_path, 'r') as file:
#             data = json.load(file)

#         if 'NaN' in data["count_gt"] or 'NaN' in data["yesno_gt"]:
#             nan_count += 1
#         if 'unknown' in data["count_gt"] or 'unknown' in data["yesno_gt"]:
#             unknown_count += 1 
#         total_nan_count += nan_count
#         total_unknown_count += unknown_count
        
#     return total_nan_count, total_unknown_count

def analyze_hallucination_parameters(dataset):
    # Initialize counters for parameter combinations
    count_llm_params = defaultdict(int)
    count_bert_params = defaultdict(int)
    yesno_llm_params = defaultdict(int)
    yesno_bert_params = defaultdict(int)

    # Analyze count question variations
    for idx, variations in enumerate(dataset['count_variations']):
        if dataset['count_gt'][idx] == 'unknown':
            continue

        for variation in variations:
            params = tuple(variation['parameters'])
            if variation['llm_selfevaluation'] == 'yes':
                count_llm_params[params] += 1
            if variation['exact_match'] == 'yes':
                count_bert_params[params] += 1

    # Analyze yesno question variations
    for idx, variations in enumerate(dataset['yesno_variations']):

        if dataset['yesno_gt'][idx] == 'unknown':
            continue

        for variation in variations:
            params = tuple(variation['parameters'])
            if variation['llm_selfevaluation'] == 'yes':
                yesno_llm_params[params] += 1
            if variation['exact_match'] == 'yes':
                yesno_bert_params[params] += 1

    return count_llm_params, count_bert_params, yesno_llm_params, yesno_bert_params

def save_to_csv(hallucination_params, question_type, metric, output_directory):
    sorted_params = sorted(hallucination_params.items(), key=lambda x: x[1], reverse=True)
    csv_filename = f"{question_type}_{metric}_hallucination_distribution.csv"
    csv_path = os.path.join(output_directory, csv_filename)

    with open(csv_path, 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['Temperature', 'Frequency Penalty', 'Presence Penalty', 'Top P', 'Count'])
        for params, count in sorted_params:
            csv_writer.writerow([params[0], params[1], params[2], params[3], count])

    print(f"Saved {metric} hallucination parameter distribution for {question_type} questions to {csv_path}")

def main():
    dataset_directory = '../results/questions/generated4/'
    output_directory = './hallucination_analysis_results/final_dataset_results/'
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    total_count_llm_params = defaultdict(int)
    total_count_bert_params = defaultdict(int)
    total_yesno_llm_params = defaultdict(int)
    total_yesno_bert_params = defaultdict(int)

    for filename in os.listdir(dataset_directory):
        if filename.endswith('.json'):
            file_path = os.path.join(dataset_directory, filename)
            dataset = load_json_file(file_path)

            # Analyze hallucination parameters for the dataset
            count_llm, count_bert, yesno_llm, yesno_bert = analyze_hallucination_parameters(dataset)

            # Aggregate the results
            for params, count in count_llm.items():
                total_count_llm_params[params] += count
            for params, count in count_bert.items():
                total_count_bert_params[params] += count
            for params, count in yesno_llm.items():
                total_yesno_llm_params[params] += count
            for params, count in yesno_bert.items():
                total_yesno_bert_params[params] += count

    # Save the sorted tables to CSV files
    save_to_csv(total_count_llm_params, "no_unknown_count", "LLM_Evaluation", output_directory)
    save_to_csv(total_count_bert_params, "no_unknown_count", "Exact_Match", output_directory)
    save_to_csv(total_yesno_llm_params, "no_unknown_yesno", "LLM_Evaluation", output_directory)
    save_to_csv(total_yesno_bert_params, "no_unknown_yesno", "Exact_Match", output_directory)

if __name__ == '__main__':
    main()
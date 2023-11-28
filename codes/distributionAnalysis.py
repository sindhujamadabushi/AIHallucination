import os
import json
import csv
from collections import defaultdict

def load_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def analyze_hallucination_parameters(dataset):
    # Initialize counters for parameter combinations
    count_llm_params = defaultdict(int)
    count_bert_params = defaultdict(int)
    yesno_llm_params = defaultdict(int)
    yesno_bert_params = defaultdict(int)

    # Analyze count question variations
    for variations in dataset['count_variations']:
        for variation in variations:
            params = tuple(variation['parameters'])
            if variation['llmevaluation'] == 'yes':
                count_llm_params[params] += 1
            if variation['bertscore'] == 'yes':
                count_bert_params[params] += 1

    # Analyze yesno question variations
    for variations in dataset['yesno_variations']:
        for variation in variations:
            params = tuple(variation['parameters'])
            if variation['llmevaluation'] == 'yes':
                yesno_llm_params[params] += 1
            if variation['bertscore'] == 'yes':
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
    dataset_directory = '../results/questions/generated2/'
    output_directory = './hallucination_analysis_results/'
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
    save_to_csv(total_count_llm_params, "count", "LLM_Evaluation", output_directory)
    save_to_csv(total_count_bert_params, "count", "BERT_Score", output_directory)
    save_to_csv(total_yesno_llm_params, "yesno", "LLM_Evaluation", output_directory)
    save_to_csv(total_yesno_bert_params, "yesno", "BERT_Score", output_directory)

if __name__ == '__main__':
    main()
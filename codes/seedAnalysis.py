import os
import json

def load_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def perform_statistical_analysis(dataset):
    # Initialize counters for count questions
    count_gt_known = sum(1 for answer in dataset['count_gt'] if answer.lower() not in ['unknown', 'nan', ''])
    count_gt_nan = sum(1 for answer in dataset['count_gt'] if answer.lower() == 'nan')
    count_gt_unknown = sum(1 for answer in dataset['count_gt'] if answer.lower() == 'unknown')

    # Initialize counters for yesno questions
    yesno_gt_known = sum(1 for answer in dataset['yesno_gt'] if answer.lower() not in ['unknown', 'nan', ''])
    yesno_gt_nan = sum(1 for answer in dataset['yesno_gt'] if answer.lower() == 'nan')
    yesno_gt_unknown = sum(1 for answer in dataset['yesno_gt'] if answer.lower() == 'unknown')

    # Compile analysis results
    analysis_results = {
        'count_questions_total': len(dataset['count']),
        'yesno_questions_total': len(dataset['yesno']),
        'count_gt_known': count_gt_known,
        'count_gt_nan': count_gt_nan,
        'count_gt_unknown': count_gt_unknown,
        'yesno_gt_known': yesno_gt_known,
        'yesno_gt_nan': yesno_gt_nan,
        'yesno_gt_unknown': yesno_gt_unknown,
    }
    return analysis_results

def main():
    dataset_directory = '../results/questions/context/'
    total_analysis = {
        'count_questions_total': 0,
        'yesno_questions_total': 0,
        'count_gt_known': 0,
        'count_gt_nan': 0,
        'count_gt_unknown': 0,
        'yesno_gt_known': 0,
        'yesno_gt_nan': 0,
        'yesno_gt_unknown': 0,
    }

    for filename in os.listdir(dataset_directory):
        if filename.endswith('.json'):
            file_path = os.path.join(dataset_directory, filename)
            dataset = load_json_file(file_path)

            # Perform statistical analysis on the dataset
            results = perform_statistical_analysis(dataset)

            # Aggregate the results
            for key in total_analysis:
                total_analysis[key] += results[key]

            # Print the analysis results for the current file
            print(f"Analysis for {filename}:")
            print(json.dumps(results, indent=4))

    # Print the total analysis results for all files
    print("Total analysis results for all files:")
    print(json.dumps(total_analysis, indent=4))
    print(f"Total known answers: {total_analysis['count_gt_known'] + total_analysis['yesno_gt_known']}")
    print(f"Total NaN answers: {total_analysis['count_gt_nan'] + total_analysis['yesno_gt_nan']}")
    print(f"Total unknown answers: {total_analysis['count_gt_unknown'] + total_analysis['yesno_gt_unknown']}")
    print(f"Total answers: {total_analysis['count_questions_total'] + total_analysis['yesno_questions_total']}")

if __name__ == '__main__':
    main()
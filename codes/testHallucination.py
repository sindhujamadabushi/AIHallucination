import json, os
from answerGenerator import generate_answers
from evaluationMetrics import llm_selfevaluation, bert_score
from loadDataset import LoadDataset

def evaluate_llmevaluation(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        file_content = file.read()
        data = json.loads(file_content)
    
    for question_type in ['count_variations', 'yesno_variations']:
        for question_dicts in data[question_type]:
            for question_dict in question_dicts:
                # print(question_dict)
                answer = generate_answers(data["context"], question_dict["question"])
                question_dict['answer'] = answer
                llm_evaluation = llm_selfevaluation(data["context"], question_dict["question"], answer)
                try:
                    # print('enter try')
                    if int(llm_evaluation) < 7:
                        question_dict['llmevaluation'] = 'no'
                    else:
                        question_dict['llmevaluation'] = 'yes'
                        
                except:
                    print('cannot convert to int')
                    question_dict['llmevaluation'] = 'N'
    # if 'yes' in llm_evaluation or 'YES' in llm_evaluation or 'Yes' in llm_evaluation:
    #     return 'yes'
    # if 'no' in llm_evaluation or 'NO' in llm_evaluation or 'No' in llm_evaluation:
    #     return 'no'

    with open('out.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)
    return


def evaluate_bert_score(file_path):
    with open('out.json', 'r', encoding='utf-8') as file:
        file_content = file.read()
        data = json.loads(file_content)
    def find_subarray_index(question, variations):
        for index, subarray in enumerate(variations):
            if any(q['question'] == question for q in subarray):
                return index
        return None
    for question_type, gt_key in [('count_variations', 'count_gt'), ('yesno_variations', 'yesno_gt')]:
        for subarray in data[question_type]:
            for question_dict in subarray:
                subarray_index = find_subarray_index(question_dict['question'], data[question_type])
                gt_answer = data[gt_key][subarray_index] if subarray_index is not None else None
                # print("gt_answer: ",gt_answer)
                # print("question_dict: ",question_dict['answer'])
                if gt_answer is not None:
                    question_dict['bertscore'] = bert_score(gt_answer, question_dict['answer'])
                try:
                    # print('enter try')
                    if float(bert_score(gt_answer, question_dict['answer'])) < 0.5:
                        question_dict['bertscore'] = 'no'
                    else:
                        question_dict['bertscore'] = 'yes'
                        
                except:
                    print('cannot convert to int')
                    question_dict['bertscore'] = 'N'

    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)


all_data = LoadDataset.read_all_json_files('../results/questions/generated/')
output_directory = ('../results/questions/generated2/')

for i, dataset in enumerate(all_data):
    context = dataset['context']
    count_questions = dataset['count']
    yesno_questions = dataset['yesno']

    print("Context ", i)

    for idx, question_list in enumerate(dataset['count_variations']):
        gt_answer = dataset['count_gt'][idx]

        print("  Count ", idx)

        for dict_idx, question_dict in enumerate(question_list):
            print("    Dict idx ", dict_idx)
            question = question_dict['question']
            answer = generate_answers(context, question)
            llm_selfevaluation_out = llm_selfevaluation(context, gt_answer, answer)
            bert_score_output = bert_score(gt_answer, answer)

            try:
                # print('enter try')
                if int(llm_selfevaluation_out) < 7:
                    question_dict['llmevaluation'] = 'no'
                else:
                    question_dict['llmevaluation'] = 'yes'

            except:
                print('cannot convert to int')
                question_dict['llmevaluation'] = 'N'

            try:
                # print('enter try')
                if float(bert_score_output) < 0.5:
                    question_dict['bertscore'] = 'no'
                else:
                    question_dict['bertscore'] = 'yes'

            except:
                print('cannot convert to int')
                question_dict['bertscore'] = 'N'

    for idx, question_list in enumerate(dataset['yesno_variations']):

        print("  Yesno ", idx)
        gt_answer = dataset['yesno_gt'][idx]

        for dict_idx, question_dict in enumerate(question_list):
            print("    Dict idx ", dict_idx)

            question = question_dict['question']
            answer = generate_answers(context, question)
            llm_selfevaluation_out = llm_selfevaluation(context, gt_answer, answer)
            bert_score_output = bert_score(gt_answer, answer)

            try:
                # print('enter try')
                if int(llm_selfevaluation_out) < 7:
                    question_dict['llmevaluation'] = 'no'
                else:
                    question_dict['llmevaluation'] = 'yes'

            except:
                print('cannot convert to int')
                question_dict['llmevaluation'] = 'N'

            try:
                # print('enter try')
                if float(bert_score_output) < 0.5:
                    question_dict['bertscore'] = 'no'
                else:
                    question_dict['bertscore'] = 'yes'

            except:
                print('cannot convert to int')
                question_dict['bertscore'] = 'N'

        # print("Finish yesno")

    # Generate a filename for each dataset
    output_filename = f"context_{i}.json"
    output_path = os.path.join(output_directory, output_filename)

    # Save the dataset with generated questions to a JSON file
    with open(output_path, 'w', encoding='utf-8') as json_file:
        json.dump(dataset, json_file, ensure_ascii=False, indent=4)

    # print("Finish saving")

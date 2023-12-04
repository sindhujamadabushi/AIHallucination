def evaluate_llmevaluation(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        file_content = file.read()
        data = json.loads(file_content)
    
    for question_type in ['count_variations', 'yesno_variations']:
        for question_dicts in data[question_type]:
            for question_dict in question_dicts:
                answer = generate_answers(data["context"], question_dict["question"])
                question_dict['answer'] = answer
                print(question_dict['answer'])
                llm_evaluation = llm_selfevaluation(data["context"], question_dict["question"], answer)
                try:
                    if int(llm_evaluation) < 7:
                        question_dict['llmevaluation'] = 'no'
                    else:
                        question_dict['llmevaluation'] = 'yes'
                        
                except:
                    print('cannot convert to int')
                    question_dict['llmevaluation'] = 'N'
    # with open('out.json', 'w', encoding='utf-8') as file:
    #     json.dump(data, file, indent=4)
    return

def evaluate_exact_match(file_path):
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
                if gt_answer is not None:
                    question_dict['exact_match'] = exact_match(gt_answer, question_dict['answer'])
                try:
                    if float(exact_match(gt_answer, question_dict['answer'])) == 'yes':
                        question_dict['exact_match'] = 'yes'
                    else:
                        question_dict['exact_match'] = 'no'      
                except:
                    print('cannot convert to int')
                    question_dict['exact_match'] = 'N'

    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)

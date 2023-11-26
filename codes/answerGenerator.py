import json
import os
from openai import OpenAI

client = OpenAI(api_key="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")

def generate_answers(context, questions):
    answers = []
    for question in questions: 
        context_part = f"Context: {context}\n" if context else "Context: \n"
        prompt = f"{context_part}Question: {question}\nAnswer:\nAnswer should not be more than five words."
        
        response = client.completions.create(model="text-davinci-002",
        prompt=prompt,
        max_tokens=150)
        answer = response.choices[0].text.strip()
        answers.append({"question": question, "answer": answer})
    return answers

def process_file(input_file_path, output_file_path, iscontext, counter):
    if iscontext:
        with open(input_file_path + 'context_' + str(counter) + '.json', 'r') as file:
            data = json.load(file)
    else: 
        with open(input_file_path + 'nocontext_' + str(counter) + '.json', 'r') as file:
            data = json.load(file)
    
    context = data['context']
    count_questions = data.get('count', [])
    yesno_questions = data.get('yesno', [])

    count_answers = generate_answers(context, count_questions)
    yesno_answers = generate_answers(context, yesno_questions)

    output_data = {
        "context": context,
        "count": count_answers,
        "yesno": yesno_answers
    }

    if not os.path.exists(output_file_path):
        os.makedirs(output_file_path)

    with open(output_file_path + 'seedQA_' + str(counter) + '.json', 'w') as file:
        json.dump(output_data, file, indent=4)

input_file_path_context = '../results/questions/context/' 
input_file_path_nocontext = '../results/questions/nocontext/'  
output_file_path_context = '../results/seedQA/context/'
output_file_path_nocontext = '../results/seedQA/nocontext/'  
num_contexts = 5 #arg
iscontext = False #arg

if iscontext:
    for i in range(num_contexts):
        process_file(input_file_path_context, output_file_path_context, iscontext, i)
else:
    for i in range(num_contexts):
        process_file(input_file_path_nocontext, output_file_path_nocontext, iscontext, i)
    

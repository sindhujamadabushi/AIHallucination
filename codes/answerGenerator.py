import json
import os
from openai import OpenAI
import argparse


def generate_answers(context, question, openai_key):
    client = OpenAI(api_key = openai_key)
    context_part = f"Context: {context}\n" if context else "Context: \n"
    prompt = f"Based on the following context, answer the given question: {context_part}Question: {question}"   
    response = client.completions.create(model="text-davinci-002",
    prompt=prompt,
    max_tokens=150)
    answer = response.choices[0].text.strip()
    return answer

# def process_file(input_file_path, output_file_path, counter, openai_key):
#     with open(input_file_path +"context_" +str(counter) + '.json', 'r') as file:
#         data = json.load(file)

#     context = data['context']
#     count_questions = data.get('count', [])
#     yesno_questions = data.get('yesno', [])

#     count_answers = []  
#     for i in range(len(count_questions)):
#         answer = {"question": count_questions[i], "answer": generate_answers(context, count_questions[i], openai_key)}
#         count_answers.append(answer)  
#     yesno_answers = []
#     for i in range(len(yesno_questions)):
#         answer = {"question": yesno_questions[i], "answer": generate_answers(context, yesno_questions[i], openai_key)}
#         yesno_answers.append(answer) 

#     output_data = {
#         "context": context,
#         "count": count_answers,
#         "yesno": yesno_answers
#     }

#     if not os.path.exists(output_file_path):
#         os.makedirs(output_file_path)

#     with open(output_file_path + 'context_' + str(counter) + '.json', 'w') as file:
#         json.dump(output_data, file, indent=4)

# # input_file_path = '../results/questions/generated/' 
# # output_file_path = '../results/seedQA/'
# # num_contexts = 1

# # parser = argparse.ArgumentParser()
# # parser.add_argument('--api_key', type=str, required=True)
# # args = parser.parse_args()
# # openai_key = str(args.api_key)

# # for i in range(num_contexts):
# #     process_file(input_file_path, output_file_path, i, openai_key)

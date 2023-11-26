from openai import OpenAI
import json
import os
import random

client = OpenAI(api_key="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")

# extract all the questions from the files ~ 1000 Qs
def extract_questions(input_path, output_path, num_contexts):
    questions = []
    
    for i in range(num_contexts):  
        file_path = os.path.join(input_path, f"context_{i}.json")
        with open(file_path, 'r') as file:
            data = json.load(file)
            count_questions = data.get('count', [])
            yesno_questions = data.get('yesno', [])
            questions.extend(count_questions + yesno_questions)

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    with open(output_path + 'tmp_questions.txt', 'w') as file:
        for question in questions:
            file.write(question + '\n')


def paraphrase_question(question, temperature, freq_penalty, presence_penalty, top_p):
    try:
        response = client.completions.create(
            model="text-davinci-002",
            prompt=f"Rephrase the question without changing its meaning and answer.\nQuestion: '{question}'",
            temperature=temperature,
            frequency_penalty=freq_penalty,
            presence_penalty=presence_penalty,
            top_p=top_p,
            max_tokens=60
        )
        return response.choices[0].text.strip()
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def process_questions(input_file, num_questions=6):
    with open(input_file, 'r') as file:
        questions = file.readlines()

    question_counts = {}
    for question in questions:
        question = question.strip()
        if question not in question_counts:
            question_counts[question] = 0

        if question_counts[question] < num_questions:
            T = random.choice([1.2, 1.4, 1.6, 1.8])
            FP = random.choice([1.2, 1.4, 1.6, 1.8])
            PP = random.choice([1.2, 1.4, 1.6, 1.8])
            top_p = random.choice([0.92, 0.95])

            paraphrased = paraphrase_question(question, T, FP, PP, top_p)
            if paraphrased:
                out_path = 'results/diverseQuestions/'
                file_name = f"questions_t{T}_fp{FP}_pp{PP}_tp{top_p}.txt"
                with open(out_path + file_name, 'a') as out_file:
                    out_file.write(paraphrased + '\n')

            question_counts[question] += 1

input_path = '../results/questions/context'  
output_path = '../results/diverseQuestions/'  
num_contexts = 5
num_questions = 6 # number of diversified questions for each seed question

extract_questions(input_path, output_path, num_contexts)

# Process the questions from tmp_questions.txt
input_file = '../results/diverseQuestions/tmp_questions.txt'  

process_questions(input_file, num_questions)


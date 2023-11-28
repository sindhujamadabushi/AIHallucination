from openai import OpenAI
import json
import os
import random

from loadDataset import LoadDataset  # Import the QADataset class from qa_dataset.py

class DiverseQuestionGenerator:
    def __init__(self, dataset_directory):
        self.dataset_directory = dataset_directory
        self.datasets = self.load_all_datasets()
        self.client = OpenAI(api_key="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")

    def load_all_datasets(self):
        return LoadDataset.read_all_json_files(self.dataset_directory)

    def generate_diverse_questions(self, num_questions):

        output_directory = '../results/questions/generated/'

        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        for i, dataset in enumerate(self.datasets):
            context = dataset['context']
            count_questions = dataset['count']
            yesno_questions = dataset['yesno']

            dataset['count_variations'] = [[] for _ in count_questions]
            dataset['yesno_variations'] = [[] for _ in yesno_questions]

            for idx, question in enumerate(count_questions):
                diversified_count_questions = self.call_gpt_api(context, question, num_questions)
                dataset['count_variations'][idx].extend(diversified_count_questions)

            print("Finish count")

            # print(len(diversified_count_questions))
            # print(len(dataset['count_variations']))
            # print(len(dataset['count_variations'][0]))

            # Generate diverse questions for yes/no questions
            for idx, question in enumerate(yesno_questions):
                diversified_yesno_questions = self.call_gpt_api(context, question, num_questions)
                dataset['yesno_variations'][idx].extend(diversified_yesno_questions)

            print("Finish yesno")

            # Generate a filename for each dataset
            output_filename = f"context_{i}.json"
            output_path = os.path.join(output_directory, output_filename)

            # Save the dataset with generated questions to a JSON file
            with open(output_path, 'w', encoding='utf-8') as json_file:
                json.dump(dataset, json_file, ensure_ascii=False, indent=4)

            print("Finish saving")

    def paraphrase_question(self, question, temperature, freq_penalty, presence_penalty, top_p):
        try:
            response = self.client.completions.create(
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

    def call_gpt_api(self, context, question, num_questions=2):

        paraphrased_questions = []

        while len(paraphrased_questions) < num_questions:
            T = random.choice([1.2, 1.4, 1.6, 1.8])
            FP = random.choice([1.2, 1.4, 1.6, 1.8])
            PP = random.choice([1.2, 1.4, 1.6, 1.8])
            top_p = random.choice([0.92, 0.95])
            paraphrased_questions.append({'parameters': (T, FP, PP, top_p), 'question': self.paraphrase_question(question, T, FP, PP, top_p)})


        # print(paraphrased_questions)
        # print(len(paraphrased_questions))

        return paraphrased_questions


if __name__ == '__main__':
    # Assuming the JSON files are located in '../results/questions/context/'
    dataset_directory = '../results/questions/context/'
    output_directory = '../results/questions/generated/'
    generator = DiverseQuestionGenerator(dataset_directory)
    generator.generate_diverse_questions(num_questions=10)  # Assuming you want to generate 5 variations
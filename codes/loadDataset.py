import json
import os

class LoadDataset:
    def __init__(self, data):
        self.data = data
        self.context = data.get('context', '')
        self.count_questions = data.get('count', [])
        self.yesno_questions = data.get('yesno', [])
        self.count_gt = data.get('count_gt', [])
        self.yesno_gt = data.get('yesno_gt', [])

    def get_context(self):
        return self.context

    def get_count_questions(self):
        return self.count_questions

    def get_yesno_questions(self):
        return self.yesno_questions

    def get_count_gt(self):
        return self.count_gt

    def get_yesno_gt(self):
        return self.yesno_gt

    @classmethod
    def load_from_json(cls, json_path):
        with open(json_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return cls(data)

    @staticmethod
    def read_all_json_files(directory):
        all_data = []
        for filename in os.listdir(directory):
            if filename.endswith('.json'):
                file_path = os.path.join(directory, filename)
                try:
                    with open(file_path, 'r', encoding='utf-8') as file:
                        file_content = file.read()
                        file_content = LoadDataset.remove_control_characters(file_content)
                        data = json.loads(file_content)
                        all_data.append(data)
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON from file: {file_path}")
                    print(f"Error message: {e}")
        return all_data

    @staticmethod
    def remove_control_characters(s):
        return ''.join(ch for ch in s if ch.isprintable() or ch.isspace())

if __name__ == '__main__':
    qa_dataset = LoadDataset.load_from_json('../results/questions/context/context_0.json')

    # Access the dataset information
    context = qa_dataset.get_context()
    count_questions = qa_dataset.get_count_questions()
    yesno_questions = qa_dataset.get_yesno_questions()
    count_gt = qa_dataset.get_count_gt()
    yesno_gt = qa_dataset.get_yesno_gt()

    # Print the context
    print("Context:", context)
    # Print the count questions
    print("Count Questions:", count_questions)
    # Print the yes/no questions
    print("Yes/No Questions:", yesno_questions)
    # Print the count ground truth answers
    print("Count Ground Truth:", count_gt)
    # Print the yes/no ground truth answers
    print("Yes/No Ground Truth:", yesno_gt)
# from transformers import BertTokenizer, BertModel
# import torch
# import numpy as np
# from factsumm import FactSumm
# from selfcheckgpt.modeling_selfcheck import SelfCheckNLI
# from openai import OpenAI

# client = OpenAI(api_key="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")

# def bert_score(ground_truth,answer):
#     tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
#     model = BertModel.from_pretrained("bert-base-uncased")
#     inputs1 = tokenizer(ground_truth, return_tensors="pt", padding=True, truncation=True)
#     inputs2 = tokenizer(answer, return_tensors="pt", padding=True, truncation=True)
#     outputs1 = model(**inputs1)
#     outputs2 = model(**inputs2)
#     embeddings1 = outputs1.last_hidden_state.mean(dim=1).detach().numpy()
#     embeddings2 = outputs2.last_hidden_state.mean(dim=1).detach().numpy()
#     similarity = np.dot(embeddings1, embeddings2.T) / (np.linalg.norm(embeddings1) * np.linalg.norm(embeddings2))
#     return str(similarity[0][0])

# def rogue_score(ground_truth,answer):
#     factsumm = FactSumm()
#     return factsumm.calculate_rouge(ground_truth, answer)

# def selfcheckGPT(ground_truth, answer): 
#     device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
#     selfcheck_nli = SelfCheckNLI(device=device) # set device to 'cuda' if GPU is available
#     sent_scores_nli = selfcheck_nli.predict(
#         sentences = ground_truth,                          
#         sampled_passages = [answer], 
#     )
#     return sent_scores_nli

def exact_match(ground_truth, answer):
    if ground_truth in answer:
        return 'model is not hallucinating'                 # case model not hallucinating
    else:
        return 'models is hallucinating'                # case model is hallucinating

# def llm_selfevaluation(context, ground_truth, answer):
#     response = []
#     response = client.completions.create(
#         model="text-davinci-002",
#         prompt=f"Score the following summary given the corresponding context with respect to consistency from 1 to 10. Note that consistency measures how much information in the ground truth is present in the answer. 10 points indicate the answer contains the ground truth.\nContext: {context} Ground Truth: {ground_truth}\nAnswer: {answer}\nScore:",
#         max_tokens = 10
#     )
#     score = response.choices[0].text.strip().split("\\n")
#     return score[0]


print(exact_match('five', 'beyonce won seven awards awards but taylor swift won five'))

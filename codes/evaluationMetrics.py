from transformers import BertTokenizer, BertModel
import torch
import numpy as np
from factsumm import FactSumm
from selfcheckgpt.modeling_selfcheck import SelfCheckNLI

def bert_score(ground_truth,answer):
    # Load the pre-trained BERT model and tokenizer
    tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
    model = BertModel.from_pretrained("bert-base-uncased")

    # Prepare the input texts for BERT
    inputs1 = tokenizer(ground_truth, return_tensors="pt", padding=True, truncation=True)
    inputs2 = tokenizer(answer, return_tensors="pt", padding=True, truncation=True)

    outputs1 = model(**inputs1)
    outputs2 = model(**inputs2)

    # Obtain the representation vectors
    embeddings1 = outputs1.last_hidden_state.mean(dim=1).detach().numpy()
    embeddings2 = outputs2.last_hidden_state.mean(dim=1).detach().numpy()

    # Calculate cosine similarity
    similarity = np.dot(embeddings1, embeddings2.T) / (np.linalg.norm(embeddings1) * np.linalg.norm(embeddings2))

    # Step 8: Print the result
    print("Similarity between the texts: {:.4f}".format(similarity[0][0]))
    return similarity[0][0]

def rogue_score(ground_truth,answer):
    factsumm = FactSumm()
    factsumm.calculate_rouge(ground_truth, answer)

def selfcheckGPT(ground_truth, answer): 
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    selfcheck_nli = SelfCheckNLI(device=device) # set device to 'cuda' if GPU is available

    sent_scores_nli = selfcheck_nli.predict(
        sentences = ground_truth,                          
        sampled_passages = [answer], 
    )
    print(sent_scores_nli)
    return sent_scores_nli

text1 = "Beyonce has won five awards"
text2 = "five"

print(selfcheckGPT(text1, text2))
print(bert_score(text1, text2))



import json

file = '/Users/sindhuja/Desktop/AIHallucination/results/questions/generated2/context_0.json'
with open(file) as f:
    data = json.load(f)

data1 = data['count_variations'][:128]

with open('out2.json') as f:
    json.dump(data1)
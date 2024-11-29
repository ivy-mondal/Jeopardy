import json

with open('../../datasets/topics.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

data = [item.replace("\u201c", '"') for item in data]
data = [item.replace("\u201d", '"') for item in data]
data = [item.replace("\u00d1", "Ñ") for item in data]
data = [item.replace('\"', '') for item in data]
with open('../../datasets/topics.json', 'w', encoding='utf-8') as file:
    json.dump(data, file)
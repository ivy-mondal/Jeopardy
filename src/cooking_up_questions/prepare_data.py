# Gotta prepare Questions and answers
import json

with open('../../datasets/JEOPARDY_QUESTIONS1.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

extract_data = [
    {"topic": item["category"],
     "question": item["question"],
     "answer": item["answer"],
     "value": int(item["value"].strip("$").replace(",", "")) if item["value"] is not None else 0}
    for item in data
    if not ('<a href' in item["question"] or '.mp3' in item["question"] or '<br' in item["question"])
]

with open('../../datasets/dataset.json', 'w') as f:
    json.dump(extract_data, f, indent=4)

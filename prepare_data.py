# Gotta prepare Questions and answers
import json

with open('JEOPARDY_QUESTIONS1.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

extract_data = [{"question": item["question"], "answer": item["answer"]} for item in data]

with open('dataset.json', 'w') as f:
    json.dump(extract_data, f, indent=4)


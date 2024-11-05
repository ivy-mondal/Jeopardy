# Gotta prepare Questions and answers
import json
import re

with open('JEOPARDY_QUESTIONS1.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

extract_data = [{"topic": item["category"],"question": item["question"], "answer": item["answer"], "points": item["value"]} for item in data
                if not ('<a href' in item["question"] or '.mp3' in item["question"])]

with open('dataset.json', 'w') as f:
    json.dump(extract_data, f, indent=4)


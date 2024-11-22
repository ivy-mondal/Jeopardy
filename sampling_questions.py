# making questions for rounds
import json
from collections import Counter

with open('datasets/dataset.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

total_items = len(data)
print(f"There are {total_items} questions in this trivia treasure trove!")
unique_points = {item["value"] for item in data}
print(sorted(unique_points))
point_counts = Counter(item["value"] for item in data if item["value"] is not None)

for value, count in point_counts.most_common():
    print(f"{value:<5} shows up {count:,} times")  # The :<5 aligns the values nicely


def create_question_level(data, min_value, max_value, file_name):
    questions_and_answers = [
        {"topic": item["topic"], "question": item["question"], "answer": item["answer"]} for item in data if min_value < item["value"] <= max_value and item["value"] % 100 == 0
    ]
    with open(file_name, 'w') as f:
        json.dump(questions_and_answers, f, indent=4)


create_question_level(data, 0, 300, "datasets/level_1_questions.json")
create_question_level(data, 300, 600, "datasets/level_2_questions.json")
create_question_level(data, 600, 1000, "datasets/level_3_questions.json")
create_question_level(data, 1000, 2000, "datasets/level_4_questions.json")
create_question_level(data, 2000, 18000, "datasets/level_5_questions.json")

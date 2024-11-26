import json


def create_topic_list(data):
    topic_list = []
    for item in data:
        if item["topic"] not in topic_list:
            topic_list.append(item["topic"])
    with open('../../datasets/topics.json', 'w') as f:
        json.dump(topic_list, f, indent=4)


with open('../../datasets/dataset.json', 'r', encoding='utf-8') as file:
    data = json.load(file)
create_topic_list(data)


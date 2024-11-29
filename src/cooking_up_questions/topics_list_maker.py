import json


def create_topic(data):
    topic_list = []
    for item in data:
        if item["topic"] not in topic_list:
            topic_list.append(item["topic"])

    with open('../../datasets/topics.json', 'w') as f:
        json.dump(topic_list, f, indent=4)
    return topic_list


with open('../../datasets/dataset.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

topics = create_topic(data)
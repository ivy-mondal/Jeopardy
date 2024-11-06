# Super dum dum to supa smort ai, depends of the model ehe
from openai import OpenAI


def choose_ai_player(level):
    models = {
        "super easy": "meta-llama/llama-3.1-8b-instruct",
        "easy": "openai/gpt-4o-mini",
        "medium": "meta-llama/llama-3.1-70b-instruct",
        "hard": "openai/gpt-4o",
        "final boss": "anthropic/claude-3.5-sonnet"
    }
    return models[level]


def ai_player(level, topic, question):
    api_key = open(".env", mode='r').read()
    client = OpenAI(base_url="https://openrouter.ai/api/v1",
                    api_key=api_key, )
    completion = client.chat.completions.create(
        model=choose_ai_player(level),
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": "I will provide you a question, and topic which contains additional context. Your task is to answer the question within the given context. In your output include only the answer, nothing else."
            },
            {
                "role": "user",
                "content": f" {topic}\n Who or what it refers to in\n {question}"
            }
        ]
    )
    result = completion.choices[0].message.content
    return result

"""
question_1 = "'Revolutionary War hero: \"His spirit is in Vermont now\"'"
print(ai_player("super easy", "EPITAPHS & TRIBUTES", question_1))
print(ai_player("easy", "EPITAPHS & TRIBUTES", question_1))
print(ai_player("medium", "EPITAPHS & TRIBUTES", question_1))
print(ai_player("hard", "EPITAPHS & TRIBUTES", question_1))
print(ai_player("final boss", "EPITAPHS & TRIBUTES", question_1))
question_2 = "'A single layer of paper, or to perform one's craft diligently'"
topic_2 = "3-LETTER WORDS"
print(ai_player("super easy", topic_2, question_2))
print(ai_player("easy", topic_2, question_2))
print(ai_player("medium", topic_2, question_2))
print(ai_player("hard", topic_2, question_2))
print(ai_player("final boss", topic_2, question_2))

"""
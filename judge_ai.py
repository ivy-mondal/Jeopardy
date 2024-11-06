# To check answers
from openai import OpenAI


def the_judge(topic, question, correct_answer, answer):
    api_key = open(".env", mode='r').read()
    client = OpenAI(base_url="https://openrouter.ai/api/v1",
                    api_key=api_key, )
    completion = client.chat.completions.create(
        model="anthropic/claude-3.5-sonnet",
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": "I will provide you a question, and topic which contains additional context. Your task is to compare the answer  with provided correct answer, and determine if the answer is close enough to the correct answer to be considered  as correct answer for the question within the given context. Your output should be True if it's correct else false, only that, nothing else."
            },
            {
                "role": "user",
                "content": f" {topic}\n Who or what it refers to in\n {question} \n {correct_answer}\n {answer} is this close enough to correct answer"
            }
        ]
    )
    result = completion.choices[0].message.content
    return result


# , , "sly"
question_1 = "'Revolutionary War hero: \"His spirit is in Vermont now\"'"
print(the_judge("EPITAPHS & TRIBUTES", question_1, "Ethan Allen", "The phrase refers to Ethan Allan, a Revolutionary War Hero associated with Vermont"))
question_2 = "'A single layer of paper, or to perform one's craft diligently'"
topic_2 = "3-LETTER WORDS"
print(the_judge(topic_2, question_2, "ply", "pLy"))

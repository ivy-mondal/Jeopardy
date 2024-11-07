# To fetch questions for game
import json
import random

from ai_player import choose_ai_player, ai_player
from judge_ai import the_judge


def fetch_question_file(level: int):
    question_files = {1: "level_1_questions.json",
                      2: "level_2_questions.json",
                      3: "level_3_questions.json",
                      4: "level_4_questions.json",
                      5: "level_5_questions.json"}
    return question_files[level]


def get_question(file_name, rounds: int):
    with open(file_name, 'r', encoding='utf-8') as file:
        data = json.load(file)
    question_set = random.sample(data, rounds)
    questions = [item["question"].strip("'") for item in question_set]
    topics = [item["topic"] for item in question_set]
    answers = [item["answer"] for item in question_set]
    questions = [q.replace('\\"', '"').replace('\\\'', "'") for q in questions]

    return questions, topics, answers


def play_level(level, rounds, questions, topics, answers):
    model = choose_ai_player(level)
    ai_points = 0
    player_points = 0
    for i in range(rounds):
        print(f"Your question number {i + 1} is Topic:{topics[i]}\n Question:{questions[i]}")
        player_answer = input("Please write your answer here 🤓:")
        ai_answer = ai_player(model, topics[i], questions[i])
        if the_judge(topics[i], questions[i], answers[i], player_answer):
            player_points += 5
            print("YOU ARE CORRECTO 🥳 ")
        else:
            player_points -= 1
            print("WHOOPS 😱")
        if the_judge(topics[i], questions[i], answers[i], ai_answer):
            ai_points += 5
            print("SMORT AI 🤩")
        else:
            ai_points -= 1
            print("OOF 😫")
    print("Game  Ovah!! 👀")
    print(f"SOOOOOO THE FINAL SCORE IS: AI = {ai_points} & You = {player_points}")
    return player_points, ai_points

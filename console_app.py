# Da game
import time
from needed_functions import fetch_question_file, get_question, play_level

levels = {
    1: "Super easy",
    2: "Easy",
    3: "Medium",
    4: "Hard",
    5: "The Final Boss"
}


def play():

    print("\n" + "=" * 50)
    time.sleep(0.5)
    print("Welcome to jeopardy! Let's see if you beat A.I. 😎 or get beaten by A.I. 🤖")
    time.sleep(1)
    print("GOOF LUCK!!👻")
    time.sleep(1)

    print("\nLEVEL SELECTION")
    time.sleep(0.5)
    game_route = input("Enter level number (2-5) to start from that level, or press Enter to start from level 1: ")
    if game_route in ['2', '3', '4', '5']:
        level = int(game_route)
        print(f"Starting from level {level}! Brave choice! 💪")
    else:
        level = 1
        print("Starting from level 1! Let's take it from the top! 🎮")
    time.sleep(1)

    while level <= 5:
        print("\n" + "=" * 50)
        time.sleep(0.5)
        print(f"LEVEL {level} : {levels[level]} ✨")
        time.sleep(1)

        while True:
            try:
                rounds = int(input("How many questions do you want to face? (minimum 2): "))
                if rounds < 2:
                    print("Please enter a number greater than 1!")
                    time.sleep(0.1)
                    continue
                break
            except ValueError:
                print("Please enter a valid number! 🤔")
                time.sleep(0.5)

        questions, topics, answers = get_question(fetch_question_file(level), rounds)
        player_score, ai_score = play_level(level, rounds, questions, topics, answers)

        if player_score >= ai_score and rounds // 2 <= player_score:
            print(f"🎉 Woohoo! You've beaten level {level}!")
            time.sleep(1)
            print("You can proceed to the next level 😸")
            time.sleep(0.5)
            while True:
                command = input("Do you want to continue (yes/no)? ").lower()
                if command in ['yes', 'no']:
                    break
                print("Please answer with 'yes' or 'no'!")
                time.sleep(0.5)

            if command.lower() == "yes":
                level += 1
                if level > 5:
                    print("\n")
                    time.sleep(0.5)
                    print("🏆 CONGRATULATIONS!")
                    time.sleep(1)
                    print("You've beaten the Final Boss!")
                    time.sleep(1)
                    print("You're officially smarter than AI!🎊🎇")
                    time.sleep(1)
                    print("HERE!!! HAVE A SMART COOKIE 🍪")
            else:
                print("\nThanks for playing! See you next time! 👋")
                time.sleep(0.5)
                break
        else:
            print("\nOh nwo! Sowwy score too low 😵!")
            time.sleep(1)
            print("Better luck next time!")
            time.sleep(0.5)
            break


if __name__ == "__main__":
    play()

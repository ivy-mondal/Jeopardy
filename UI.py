import customtkinter as ctk

from ai_player import choose_ai_player, ai_player
from judge_ai import the_judge
from needed_functions import fetch_question_file, get_question

levels = {
    1: "Super easy",
    2: "Easy",
    3: "Medium",
    4: "Hard",
    5: "The Final Boss"
}


class JeopardyGame(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Jeopardy: Human vs AI!")
        self.geometry("1200x800")  # Nice big window!

        # Main game area (LEFT SIDE - 70% of window)
        self.game_frame = ctk.CTkFrame(self)
        self.game_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Create a separate frame for game content
        self.content_frame = ctk.CTkFrame(self.game_frame)
        self.content_frame.pack(expand=True, fill="both")

        # Display messages/questions area
        self.display_area = ctk.CTkTextbox(
            self.game_frame,
            width=600,
            height=400,
            font=("Arial", 14)
        )
        self.current_level = 1
        self.rounds = 0
        self.current_round = 0
        self.player_score = 0
        self.ai_score = 0
        self.questions = []
        self.topics = []
        self.answers = []
        self.model = None
        self.display_area.pack(pady=10)

        # Input area
        self.input_frame = ctk.CTkFrame(self.game_frame)
        self.input_frame.pack(pady=10)
        self.answer_entry = ctk.CTkEntry(
            self.input_frame,
            width=300,
            placeholder_text="Type your answer here..."
        )
        self.answer_entry.pack(side="left", padx=5)
        self.submit_btn = ctk.CTkButton(
            self.input_frame,
            text="Submit Answer!"
        )
        self.submit_btn.pack(side="left", padx=5)
        self.submit_btn.configure(command=self.handle_answer)

        # Animation area (bottom of game frame)
        self.animation_area = ctk.CTkFrame(
            self.game_frame,
            height=200
        )
        self.animation_area.pack(fill="x", pady=10)

        # Hide the game elements initially
        self.display_area.pack_forget()
        self.input_frame.pack_forget()
        self.animation_area.pack_forget()

        # SCOREBOARD (RIGHT SIDE - 30% of window)
        self.score_frame = ctk.CTkFrame(self)
        self.score_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        # Player Score
        self.player_score_label = ctk.CTkLabel(
            self.score_frame,
            text="Player: 0",
            font=("Arial", 20, "bold")
        )
        self.player_score_label.pack(pady=10)

        # AI Score
        self.ai_score_label = ctk.CTkLabel(
            self.score_frame,
            text="AI: 0",
            font=("Arial", 20, "bold")
        )
        self.ai_score_label.pack(pady=10)

        self.start_btn = ctk.CTkButton(
            self.score_frame,
            text="Start Game!",
            command=self.start_game
        )
        self.start_btn.pack(pady=10)

        # Configure grid weights
        self.grid_columnconfigure(0, weight=7)  # Game area takes 70%
        self.grid_columnconfigure(1, weight=3)  # Score area takes 30%

        # Show level selection first!
        self.show_level_selection()

        # ====== THEN ADD ALL THE NEW METHODS ======

    def show_level_selection(self):
        # Clear game frame
        for widget in self.game_frame.winfo_children():
            widget.destroy()

        # Welcome message
        ctk.CTkLabel(
            self.game_frame,
            text="Welcome to Jeopardy: Human vs AI! 🤖",
            font=("Arial", 24, "bold")
        ).pack(pady=20)

        # Level selection buttons
        for level in range(1, 6):
            ctk.CTkButton(
                self.game_frame,
                text=f"Level {level}: {levels[level]}",
                command=lambda l=level: self.set_level(l)
            ).pack(pady=10)

    def set_level(self, level):
        self.current_level = level
        # Show rounds selection
        self.show_rounds_selection()

    def show_rounds_selection(self):
        # Clear game frame
        for widget in self.game_frame.winfo_children():
            widget.destroy()

        ctk.CTkLabel(
            self.game_frame,
            text=f"Level {self.current_level}: {levels[self.current_level]}",
            font=("Arial", 20, "bold")
        ).pack(pady=20)

        # Rounds entry
        self.rounds_entry = ctk.CTkEntry(
            self.game_frame,
            placeholder_text="Enter number of rounds (minimum 2)"
        )
        self.rounds_entry.pack(pady=10)

        ctk.CTkButton(
            self.game_frame,
            text="Start Game!",
            command=self.validate_and_start_game
        ).pack(pady=10)

    def validate_and_start_game(self):
        try:
            rounds = int(self.rounds_entry.get())
            if rounds < 2:
                self.display_message("Please enter a number greater than 1!")
                return
            self.rounds = rounds
            self.start_game()
        except ValueError:
            self.display_message("Please enter a valid number!")

    def start_game(self):
        # Clear content frame
        for widget in self.content_frame.winfo_children():
            if widget not in [self.display_area, self.input_frame, self.animation_area]:
                widget.destroy()

        # Show game elements
        self.display_area.pack(pady=10)
        self.input_frame.pack(pady=10)
        self.animation_area.pack(fill="x", pady=10)

        # Get questions for the level
        self.questions, self.topics, self.answers = get_question(
            fetch_question_file(self.current_level),
            self.rounds
        )
        self.current_round = 0
        self.display_next_question()

    def display_next_question(self):
        if self.current_round < self.rounds:
            self.display_area.delete("1.0", "end")
            self.display_area.insert("1.0", f"""
    Round {self.current_round + 1}/{self.rounds}
    Topic: {self.topics[self.current_round]}

    {self.questions[self.current_round]}
                """)
        else:
            self.end_level()

    def handle_answer(self):
        player_answer = self.answer_entry.get()
        # Get AI's answer
        ai_answer = ai_player(self.questions[self.current_round],
                              self.topics[self.current_round],
                              choose_ai_player(self.current_level))

        # Judge the answers
        player_correct = the_judge(player_answer, self.answers[self.current_round])
        ai_correct = the_judge(ai_answer, self.answers[self.current_round])

        # Update scores
        if player_correct:
            self.player_score += 1
        if ai_correct:
            self.ai_score += 1

        # Update score display
        self.player_score_label.configure(text=f"Player: {self.player_score}")
        self.ai_score_label.configure(text=f"AI: {self.ai_score}")

        # Clear answer entry
        self.answer_entry.delete(0, 'end')

        # Move to next round
        self.current_round += 1
        self.display_next_question()

    def end_level(self):
        # Clear game frame
        for widget in self.game_frame.winfo_children():
            widget.destroy()

        if self.player_score >= self.ai_score and self.rounds // 2 <= self.player_score:
            message = f"🎉 Congratulations! You've beaten level {self.current_level}!"
            if self.current_level < 5:
                ctk.CTkButton(
                    self.game_frame,
                    text="Next Level",
                    command=lambda: self.set_level(self.current_level + 1)
                ).pack(pady=10)
        else:
            message = "Better luck next time! 😅"

        ctk.CTkLabel(
            self.game_frame,
            text=message,
            font=("Arial", 20)
        ).pack(pady=20)

        ctk.CTkButton(
            self.game_frame,
            text="Play Again",
            command=self.show_level_selection
        ).pack(pady=10)

    def display_message(self, message):
        # Helper method for showing error messages
        self.display_area.delete("1.0", "end")
        self.display_area.insert("1.0", message)


if __name__ == "__main__":
    app = JeopardyGame()
    app.mainloop()

import tkinter as tk

import pygame
from PIL import Image

from animations import animate_letter, initial_pulse, animate_loading_gif, LevelSelectionAnimations
from ui_components import create_paw_button, LevelSelectionComponents


class JeopardyGUI:
    def __init__(self):
        pygame.mixer.init()
        self.window = tk.Tk()
        self.canvas = None
        self.pulse_active = True
        self.glow_active = True
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.window.title("Cute Jeopardy game 😻🎀🌸")
        self.window.configure(bg='#FFE5E5')
        self.window.state('zoomed')
        self.level = 1
        self.glow_after_id = None
        self.pulse_count = 0
        self.paw_button = None
        self.high_five_label = None
        self.paw_image = Image.open("media_files/paw.png")
        self.ps = 100
        self.show_welcome_screen()

    def show_welcome_screen(self):
        self.clear_window()

        try:
            pygame.mixer.music.load("media_files/klee_theme.mp3")
            pygame.mixer.music.set_volume(0.8)
            pygame.mixer.music.play(-1)
        except (pygame.error, FileNotFoundError):
            print("Uh oh! Klee must have bombed the music file! 💣")

        # Create canvas first
        self.canvas = tk.Canvas(
            self.window,
            bg='#FFE5E5',
            highlightthickness=0
        )
        self.canvas.pack(expand=True, fill='both')

        # Wait a tiny bit for window to finish sizing
        self.window.update()
        # Calculate positions based on screen height
        screen_height = self.window.winfo_height()

        self.window.after(100, lambda: animate_letter(self.canvas, self.window, "Welcome to", screen_height * 0.1, 0))
        self.window.after(800, lambda: animate_letter(self.canvas, self.window, "Meow-pardy! 😺", screen_height * 0.2, 0))
        self.window.after(1500, lambda: animate_letter(self.canvas, self.window, "Can you beat the A.I.? 🤖", screen_height * 0.3, 0))
        self.window.after(2500, self.add_paw)

    def add_paw(self):
        paw_frame, self.paw_button, self.high_five_label = create_paw_button(
            self.window,
            self.paw_image,
            self.ps,
            self.start_game
        )
        initial_pulse(
            window=self.window,
            button=self.paw_button,
            paw_image=self.paw_image,
            ps=self.ps,
            pulse_count=self.pulse_count,
            pulse_active=self.pulse_active
        )  # Start the initial pulse animation

    def start_game(self):
        # Check if glow_after_id exists on window before trying to cancel
        if hasattr(self.window, 'glow_after_id'):
            self.window.after_cancel(self.window.glow_after_id)
        self.clear_window()

        def transition_to_game():
            pygame.mixer.music.stop()
            self.show_game_screen()

        animate_loading_gif(
            self.window,
            "media_files/gamingcats.gif",
            transition_to_game
        )

    def show_game_screen(self):
        self.clear_window()
        self.window.configure(bg="#FAC8E4")

        # Create and pack title
        title = LevelSelectionComponents.create_title(self.window)
        title.pack(pady=20)

        # Create main button grid frame
        button_grid = LevelSelectionComponents.create_button_grid_frame(self.window)
        button_grid.pack(pady=20)

        # First row - Levels 1, 2, 3
        top_row = tk.Frame(button_grid, bg="#FAC8E4")
        top_row.pack()

        for level in range(1, 4):
            btn = LevelSelectionComponents.create_cat_button(
                top_row,
                level,
                command=lambda l=level: self.start_level(l)
            )
            btn.pack(side=tk.LEFT, padx=10)
            LevelSelectionAnimations.add_hover_effect(btn)

        # Second row - Levels 4, 5
        bottom_row = tk.Frame(button_grid, bg="#FAC8E4")
        bottom_row.pack(pady=10)

        for level in range(4, 6):
            btn = LevelSelectionComponents.create_cat_button(
                bottom_row,
                level,
                command=lambda l=level: self.start_level(l)
            )
            btn.pack(side=tk.LEFT, padx=10)
            LevelSelectionAnimations.add_hover_effect(btn)

        # Hint label
        hint = LevelSelectionComponents.create_hint_label(self.window)
        hint.pack(pady=10)

    def start_level(self, level):
        # This will be implemented later
        print(f"Starting level {level}! Meow!")

    def on_closing(self):
        self.pulse_active = False
        self.glow_active = False
        self.window.destroy()

    def clear_window(self):
        # Clear all widgets from window
        for widget in self.window.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    game = JeopardyGUI()
    game.window.mainloop()  # This makes your window stay open!

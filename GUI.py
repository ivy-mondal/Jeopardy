import math
import tkinter as tk
from datetime import datetime

import pygame
from PIL import Image, ImageTk


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

        self.show_welcome_screen()
        self.add_paw()

    # Animate welcome text
    def animate_letter(self, text, y_pos, delay_start, letters=None):
        if letters is None:
            letters = []

        screen_width = self.window.winfo_width()
        text_width = len(text) * 30
        x_start = (screen_width - text_width) / 2

        screen_height = self.window.winfo_height()
        adjusted_y = screen_height * (y_pos / 600)  # Scale based on screen height

        for i, char in enumerate(text):
            letter = self.canvas.create_text(
                x_start + (i * 30),
                adjusted_y,  # Use adjusted y position
                text=char,
                font=('Comic Sans MS', 10),
                fill='#F266A7',
                anchor='center'
            )
            letters.append(letter)

            def animate_size(letter_obj, index, start_time):
                def grow(size=1):
                    if size <= 40:  # Made font bigger
                        y_offset = math.sin(size / 3) * 10
                        self.canvas.itemconfig(
                            letter_obj,
                            font=('Segoe Script', size)
                        )
                        self.canvas.move(
                            letter_obj,
                            0,
                            y_offset
                        )
                        self.window.after(50, lambda: grow(size + 2))

                self.window.after(start_time, grow)

            animate_size(letter, i, delay_start + (i * 10))

    def show_welcome_screen(self):
        self.clear_window()

        try:
            pygame.mixer.music.load("klee_theme.mp3")
            pygame.mixer.music.set_volume(0.8)
            pygame.mixer.music.play(-1)
        except (pygame.error, FileNotFoundError) as e:
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

        self.window.after(100, lambda: self.animate_letter("Welcome to", screen_height * 0.2, 0))
        self.window.after(800, lambda: self.animate_letter("Meow-pardy! 😺", screen_height * 0.3, 0))
        self.window.after(1500, lambda: self.animate_letter("Can you beat the A.I.? 🤖", screen_height * 0.4, 0))
        self.window.after(2500, self.add_paw)

    # Glow animation
    def glow_animation(self):
        if self.glow_active:  # Only continue if active
            colors = ['#FFE5E5', '#FFD1D1', '#FFB7B7', '#FFD1D1', '#FFE5E5']

            def cycle_colors(index=0):
                if self.glow_active and index < len(colors):  # Check if still active
                    try:
                        self.paw_button.configure(bg=colors[index])
                        self.glow_after_id = self.window.after(100, lambda: cycle_colors(index + 1))
                    except tk.TclError:
                        self.glow_active = False  # Stop if window is destroyed

            cycle_colors()

    # Make initial appearance with a pulse effect
    def initial_pulse(self, size=1.0, growing=True):
        if not hasattr(self, 'pulse_count'):
            self.pulse_count = 0

        if self.pulse_count < 6 and self.pulse_active:  # Check if still active
            try:
                if growing and size < 1.1:
                    size += 0.01
                    growing = True
                elif growing:
                    growing = False
                elif not growing and size > 1.0:
                    size -= 0.01
                    growing = False
                else:
                    growing = True
                    self.pulse_count += 1

                current_width = int(200 * size)
                current_height = int(200 * size)
                paw_image_pulse = Image.open("paw.png")
                paw_image_pulse = paw_image_pulse.resize((current_width, current_height), Image.LANCZOS)
                self.paw_photo_pulse = ImageTk.PhotoImage(paw_image_pulse)
                self.paw_button.configure(image=self.paw_photo_pulse)

                self.window.after(50, lambda: self.initial_pulse(size, growing))
            except tk.TclError:
                self.pulse_active = False  # Stop if window is destroyed

    def add_paw(self):
        # Create a frame for the paw (this will help with the glow effect)
        paw_frame = tk.Frame(self.window, bg='#FFE5E5')
        paw_frame.pack(expand=True)

        paw_image = Image.open("paw.png")
        paw_image = paw_image.resize((200, 200), Image.LANCZOS)
        self.paw_photo = ImageTk.PhotoImage(paw_image)

        # Create slightly larger image for hover effect
        paw_image_large = Image.open("paw.png")
        paw_image_large = paw_image_large.resize((220, 220), Image.LANCZOS)
        self.paw_photo_large = ImageTk.PhotoImage(paw_image_large)

        self.paw_button = tk.Button(
            paw_frame,
            image=self.paw_photo,
            borderwidth=0,
            bg='#FFE5E5',
            activebackground='#FFE5E5',
            command=self.start_game
        )

        # Add hover effects
        def on_enter(event):
            self.glow_animation()
            self.paw_button.configure(image=self.paw_photo_large)

        def on_leave(event):
            self.paw_button.configure(bg='#FFE5E5')
            if hasattr(self, 'glow_after_id'):
                self.window.after_cancel(self.glow_after_id)

        # Bind hover events
        self.paw_button.bind('<Enter>', on_enter)
        self.paw_button.bind('<Leave>', on_leave)

        # Add "High five!" text that also glows
        self.high_five_label = tk.Label(
            paw_frame,
            text="✨ High five to start! ✨",
            font=('Segoe Script', 16),
            bg='#FFE5E5',
            fg='#FF9494'
        )
        self.high_five_label.pack(pady=5)
        self.paw_button.pack()
        self.initial_pulse()  # Start the initial pulse animation

    def start_game(self):
        self.window.after_cancel(self.glow_after_id)
        self.clear_window()

        # Create loading screen frame
        loading_frame = tk.Frame(self.window, bg='#FFE5E5')
        loading_frame.pack(expand=True)

        mochi_gif = Image.open("gamingcats.gif")

        # Convert the gif into frames
        frames = []
        try:
            while True:
                frames.append(ImageTk.PhotoImage(mochi_gif.copy()))
                mochi_gif.seek(len(frames))  # next frame
        except EOFError:
            pass  # We're done reading frames!

        gif_label = tk.Label(loading_frame, bg='#FFE5E5')
        gif_label.pack()

        # Loading text with dots animation
        loading_label = tk.Label(
            loading_frame,
            text="Loading your paw-some game...",
            font=('Segoe Script', 20),
            fg='#F266A7',
            bg='#FFE5E5'
        )
        loading_label.pack(pady=20)

        # Animate the gif and dots
        def update_frame(frame_num=0, start_time=None):
            if start_time is None:
                start_time = datetime.now()

            if (datetime.now() - start_time).seconds >= 5:
                pygame.mixer.music.stop()
                self.show_game_screen()  # Move to game screen
                return

            gif_label.configure(image=frames[frame_num])
            frame_num = (frame_num + 1) % len(frames)
            self.window.after(100, lambda: update_frame(frame_num, start_time))

        update_frame()

    def show_game_screen(self):
        pass

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

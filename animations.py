import math
import random
import tkinter as tk
from datetime import datetime

from PIL import Image, ImageTk


# Animate welcome text
def animate_letter(canvas, window, text, y_pos, delay_start, letters=None):
    if letters is None:
        letters = []

    screen_width = window.winfo_width()
    text_width = len(text) * 30
    x_start = (screen_width - text_width) / 2

    screen_height = window.winfo_height()
    adjusted_y = screen_height * (y_pos / 600)

    for i, char in enumerate(text):
        letter = canvas.create_text(
            x_start + (i * 30),
            adjusted_y,
            text=char,
            font=('Comic Sans MS', 10),
            fill='#F266A7',
            anchor='center'
        )
        letters.append(letter)

        def animate_size(letter_obj, start_time):
            def grow(size=1):
                if size <= 40:
                    y_offset = math.sin(size / 3) * 10
                    canvas.itemconfig(letter_obj, font=('Segoe Script', size))
                    canvas.move(letter_obj, 0, y_offset)
                    window.after(25, lambda: grow(size + 2))

            window.after(start_time, grow)

        animate_size(letter, delay_start + (i * 10))


# Glow animation
def glow_animation(window, button, glow_active):
    if glow_active:
        colors = ['#FFE5E5', '#FFD1D1', '#FFB7B7', '#FFD1D1', '#FFE5E5']

        def cycle_colors(index=0):
            if glow_active and index < len(colors):
                try:
                    button.configure(bg=colors[index])
                    next_id = window.after(100, lambda: cycle_colors(index + 1))
                    return next_id
                except tk.TclError:
                    return None

        return cycle_colors()
    return None


# Make initial appearance with a pulse effect
def initial_pulse(window, button, paw_image, ps, pulse_count, pulse_active):
    def pulse(size=1.0, growing=True):
        nonlocal pulse_count
        if pulse_count < 6 and pulse_active:
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
                    pulse_count += 1

                current_width = int(ps * size)
                current_height = int(ps * size)
                paw_image_pulse = paw_image.resize((current_width, current_height), Image.LANCZOS)
                paw_photo_pulse = ImageTk.PhotoImage(paw_image_pulse)
                button.configure(image=paw_photo_pulse)
                button.image = paw_photo_pulse  # Keep reference!

                window.after(50, lambda: pulse(size, growing))
            except tk.TclError:
                return False

    pulse()


def create_loading_screen(window, bg_color='#FFE5E5'):
    loading_frame = tk.Frame(window, bg=bg_color)
    loading_frame.pack(expand=True)

    gif_label = tk.Label(loading_frame, bg=bg_color)
    gif_label.pack()

    loading_label = tk.Label(
        loading_frame,
        text="Loading your paw-some game...",
        font=('Segoe Script', 20),
        fg='#F266A7',
        bg=bg_color
    )
    loading_label.pack(pady=20)

    return loading_frame, gif_label, loading_label


def animate_loading_gif(window, gif_path, callback, duration=7):
    """All-in-one function to handle loading screen animation"""
    # Create UI elements
    _, gif_label, _ = create_loading_screen(window)

    # Load gif frames
    gif_image = Image.open(gif_path)
    frames = []
    try:
        while True:
            frames.append(ImageTk.PhotoImage(gif_image.copy()))
            gif_image.seek(len(frames))
    except EOFError:
        pass

    # Animate frames
    def update_frame(frame_num=0, start_time=None):
        if start_time is None:
            start_time = datetime.now()

        if (datetime.now() - start_time).seconds >= duration:
            callback()
            return

        gif_label.configure(image=frames[frame_num])
        frame_num = (frame_num + 1) % len(frames)
        window.after(100, lambda: update_frame(frame_num, start_time))

    update_frame()


# For level selection screen
class LevelSelectionAnimations:
    @staticmethod
    def add_hover_effect(button):
        def on_enter(e):
            button['background'] = '#FF69B4'

        def on_leave(e):
            button['background'] = '#FFB6C1'

        button.bind('<Enter>', on_enter)
        button.bind('<Leave>', on_leave)

    @staticmethod
    def animate_gif(label, gif_path, loop=True):
        def update_frame(frame_number):
            frame = frames[frame_number]
            label.configure(image=frame)
            next_frame = (frame_number + 1) % n_frames if loop else frame_number + 1
            if next_frame < n_frames:
                label.after(50, update_frame, next_frame)

        gif = Image.open(gif_path)
        frames = []
        try:
            while True:
                # Resize each frame to be larger
                resized = gif.copy().resize((300, 200), Image.Resampling.LANCZOS)  # Made bigger to reduce compression
                frames.append(ImageTk.PhotoImage(resized))
                gif.seek(len(frames))
        except EOFError:
            pass

        n_frames = len(frames)
        label.frames = frames
        update_frame(0)

    @staticmethod
    def create_driving_cat(parent, gif_path="media_files/level_select_screen.gif"):
        """Creates a cat that drives back and forth (backwards when needed because YOLO)"""
        bottom_frame = tk.Frame(parent, bg="#FAC8E4", height=300)
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)
        bottom_frame.pack_propagate(False)

        # Create gif label inside bottom frame
        gif_label = tk.Label(bottom_frame)
        gif_label.place(x=-100, y=50, width=300, height=200)

        # Initialize direction
        moving_right = True

        def drive_animation():
            nonlocal moving_right
            window_width = parent.winfo_width()
            current_x = gif_label.winfo_x()

            if moving_right:
                if current_x > window_width:
                    moving_right = False
                else:
                    gif_label.place(x=current_x + 5, y=50)
            else:
                if current_x < -100:
                    moving_right = True
                else:
                    gif_label.place(x=current_x - 5, y=50)

            return parent.after(50, drive_animation)

        try:
            LevelSelectionAnimations.animate_gif(gif_label, gif_path, loop=True)
            animation_id = drive_animation()
            return animation_id, bottom_frame  # Return the frame instead of canvas
        except Exception as e:
            print(f"Error starting animation: {e}")
            return None, None



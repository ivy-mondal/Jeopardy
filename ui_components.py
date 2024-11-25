import tkinter as tk
from tkinter import messagebox

from PIL import Image, ImageTk

from animations import glow_animation


def create_paw_button(window, paw_image, ps, start_game_callback):
    paw_frame = tk.Frame(window, bg='#FFE5E5')
    paw_frame.pack(expand=True)

    # Create normal-sized paw
    paw_photo = ImageTk.PhotoImage(
        paw_image.resize((ps, ps), Image.LANCZOS)
    )

    # Create larger paw for hover
    paw_photo_large = ImageTk.PhotoImage(
        paw_image.resize((int(ps * 1.1), int(ps * 1.1)), Image.LANCZOS)
    )

    paw_button = tk.Button(
        paw_frame,
        image=paw_photo,
        borderwidth=0,
        bg='#FFE5E5',
        activebackground='#FFE5E5',
        command=start_game_callback
    )

    # Keep references to prevent garbage collection
    paw_button.normal_image = paw_photo
    paw_button.large_image = paw_photo_large

    # Add hover effects
    def on_enter(event):
        window.glow_after_id = glow_animation(window, paw_button, True)
        paw_button.configure(image=paw_button.large_image)

    def on_leave(event):
        paw_button.configure(bg='#FFE5E5')
        if hasattr(window, 'glow_after_id'):
            window.after_cancel(window.glow_after_id)
            delattr(window, 'glow_after_id')  # Clean up after cancelling

    # Bind hover events
    paw_button.bind('<Enter>', on_enter)
    paw_button.bind('<Leave>', on_leave)

    # Add "High five!" text
    high_five_label = tk.Label(
        paw_frame,
        text="✨ High five to start! ✨",
        font=('Segoe Script', 16),
        bg='#FFE5E5',
        fg='#FF9494'
    )
    high_five_label.pack(pady=5)
    paw_button.pack()

    return paw_frame, paw_button, high_five_label


# For level selection screen
class LevelSelectionComponents:
    @staticmethod
    def create_title(parent):
        return tk.Label(parent,
                        text="Choose Your Purr-fect Level!",
                        font=("Kawaii", 24, "bold"),
                        fg="#FF69B4",
                        bg="#FAC8E4")

    @staticmethod
    def create_cat_button(parent, level, command):
        # Create a frame for our cat button
        cat_frame = tk.Frame(parent, bg="#FAC8E4")

        emoji_map = {
            1: "🐱",
            2: "😺",
            3: "😸",
            4: "😻",
            5: "🐱‍👤"
        }

        try:
            # Load the cat face image
            original_image = Image.open(f"media_files/cat_face_button.png")
            # Resize to desired size
            resized_image = original_image.resize((100, 100), Image.Resampling.LANCZOS)
            cat_photo = ImageTk.PhotoImage(resized_image)

            # Create label for the cat image
            cat_label = tk.Label(
                cat_frame,
                image=cat_photo,
                bg="#FAC8E4",
            )
            cat_label.image = cat_photo  # Keep a reference!

            # Level number and emoji label
            text_label = tk.Label(
                cat_frame,
                text=f"Level {level} {emoji_map[level]}",
                font=("Kawaii", 14, "bold"),
                fg="#FF1493",
                bg="#FAC8E4"
            )

            # Pack widgets
            cat_label.pack(pady=5)
            text_label.pack()

            def on_enter(e):
                text_label.configure(fg="#FF69B4")
                # Add hover effect here (could be a glow effect or subtle scale)

            def on_leave(e):
                text_label.configure(fg="#FF1493")

            def on_click(e):
                command()

            # Bind events
            for widget in (cat_label, text_label):
                widget.bind("<Enter>", on_enter)
                widget.bind("<Leave>", on_leave)
                widget.bind("<Button-1>", on_click)

        except Exception as e:
            print(f"Couldn't load cat image: {e}")
            # Fallback to a simple button if image loading fails
            return tk.Button(parent, text=f"Level {level}")

        return cat_frame

    @staticmethod
    def create_hint_label(parent):
        return tk.Label(parent,
                        text="Hint: Level 1 is purr-fect for beginners!",
                        font=("Kawaii", 12, "italic"),
                        fg="#75B8EB",
                        bg="#FAC8E4")

    @staticmethod
    def create_button_grid_frame(parent, bg="#FAC8E4"):
        frame = tk.Frame(parent, bg="#FAC8E4")
        return frame


# For round and topic selection
class RoundTopicSelectionComponents:
    @staticmethod
    def create_title(window):
        title = tk.Label(
            window,
            text=f"Neow time to set up your game! 👻",
            font=("Kawaii", 24),
            bg="#FAC8E4",
            fg="#FF69B4"
        )
        return title

    @staticmethod
    def create_round_input(window):
        round_frame = tk.Frame(window, bg="#FAC8E4")

        round_label = tk.Label(
            round_frame,
            text="How many questions do you want? (Minimum 2)",
            font=("Kawaii", 16),
            bg="#FAC8E4",
            fg="#FF69B4"
        )
        round_label.pack()

        round_entry = tk.Entry(
            round_frame,
            width=10,
            font=("Kawaii", 14),
            justify='center'
        )
        round_entry.pack(pady=10)
        return round_frame, round_entry

    @staticmethod
    def create_topics_listbox(window):
        topics_frame = tk.Frame(window, bg="#FAC8E4")
        topics_label = tk.Label(
            topics_frame,
            text="Select Your Topics!",
            font=("Kawaii", 16),
            bg="#FAC8E4",
            fg="#FF69B4"
        )
        topics_label.pack()

        list_frame = tk.Frame(topics_frame, bg="#FAC8E4")
        list_frame.pack(pady=10)

        topics_listbox = tk.Listbox(
            list_frame,
            selectmode=tk.MULTIPLE,
            width=30,
            height=6,
            font=("Kawaii", 12),
            bg="#FFF0F5",
            selectbackground="#FF69B4"
        )

        scrollbar = tk.Scrollbar(list_frame, orient="vertical")
        scrollbar.config(command=topics_listbox.yview)
        topics_listbox.config(yscrollcommand=scrollbar.set)

        topics_listbox.pack(side=tk.LEFT)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        return topics_frame, topics_listbox

    @staticmethod
    def create_confirm_button(window, callback):
        confirm_button = tk.Button(
            window,
            text="I'm Ready! 🎮",
            command=callback,
            font=("Kawaii", 16),
            bg="#FF69B4",
            fg="white"
        )
        return confirm_button

    @staticmethod
    def validate_selections(round_entry, topics_listbox):
        try:
            rounds = int(round_entry.get())
            if rounds < 2:
                messagebox.showerror("Oopsie!", "You need at least 2 rounds! Don't be shy! 😊")
                return None, None
        except ValueError:
            messagebox.showerror("Oopsie!", "Please enter a valid number! Numbers only, no emoji allowed! 😅")
            return None, None

        # Get selected topics
        selected_indices = topics_listbox.curselection()
        if not selected_indices:
            messagebox.showerror("Oopsie!", "Please select at least one topic! Don't leave me hanging! 🎯")
            return None, None

        # Get the actual topics from the indices
        selected_topics = [topics_listbox.get(i) for i in selected_indices]

        return rounds, selected_topics

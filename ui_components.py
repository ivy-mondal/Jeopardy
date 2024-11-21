import tkinter as tk

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

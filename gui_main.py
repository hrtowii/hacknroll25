import sys
from gui_overlay import Overlay
if __name__ == "__main__":
    def close_callback(event):
        print("Closing overlay")
        sys.exit(0)

    def get_new_text_callback():
        # Simulate fetching new text
        return 1000, "New message!"

    overlay = Overlay(
        close_callback=close_callback,
        initial_text="Initial text",
        initial_delay=1000,
        get_new_text_callback=get_new_text_callback,
        image_path='./assets/images/logo.png',  # Specify image path
        image_size=(175,175)  # Specify image size
    )
    overlay.run()

# from tkinter import *

# win = Tk()

# photoimage = PhotoImage(file="assets/logo.png")

# width, height = photoimage.width(), photoimage.height()
# label = Label(win, bg="blue", width=width, height=height, image=photoimage)
# label.pack()

# win.mainloop()
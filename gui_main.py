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
        image_path='/Users/ibarahime/dev/hacknroll25/assets/images/logo.png',  # Specify image path
        image_size=(150, 150)  # Specify image size
    )
    overlay.run()
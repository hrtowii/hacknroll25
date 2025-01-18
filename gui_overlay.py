# Standard Library
import sys
import logging
import tkinter as tk
from tkinter import PhotoImage
from typing import Callable, Any

logger = logging.getLogger(__name__)


def report_callback_exception(exc_type, val, tb):
    if issubclass(exc_type, GracefulExit):
        sys.exit(0)

    logger.error('Exception occurred, exiting:', exc_info=(exc_type, val, tb))
    sys.exit(1)


class GracefulExit(Exception):
    "Allows callbacks to gracefully exit without logging error"


class Overlay:
    """
    Creates an overlay window using tkinter
    Uses the "-topmost" property to always stay on top of other Windows
    """
    def __init__(self,
                 close_callback: Callable[[Any], None],
                 initial_text: str,
                 initial_delay: int,
                 get_new_text_callback: Callable[[], tuple[int, str]],
                 image_path: str = None,  # Optional: Path to the image file
                 image_size: tuple[int, int] = (100, 100)):  # Optional: Image size (width, height)
        self.close_callback = close_callback
        self.initial_text = initial_text
        self.initial_delay = initial_delay
        self.get_new_text_callback = get_new_text_callback
        self.image_path = image_path
        self.image_size = image_size
        self.root = tk.Tk()
        self.root.report_callback_exception = report_callback_exception

        # Platform-specific transparency setup
        self.setup_transparency()

        # Set up Close Label
        # self.close_label = tk.Label(
        #     self.root,
        #     text=' X |',
        #     font=('Consolas', '14'),
        #     fg='green3',
        #     bg='systemTransparent' if sys.platform == 'darwin' else 'white'
        # )
        # self.close_label.bind("<Button-1>", close_callback)
        # self.close_label.grid(row=0, column=0)

        # Set up Ping Label
        # self.ping_text = tk.StringVar()
        # self.ping_label = tk.Label(
        #     self.root,
        #     textvariable=self.ping_text,
        #     font=('Consolas', '14'),
        #     fg='green3',
        #     bg='systemTransparent' if sys.platform == 'darwin' else 'white'
        # )
        # self.ping_label.grid(row=0, column=1)

        # Set up Canvas for Image (if image_path is provided)
        if self.image_path:
            self.canvas = tk.Canvas(
                self.root,
                width=self.image_size[0],
                height=self.image_size[1],
                bg='#cee741' if sys.platform == 'darwin' else '#cee741',
                highlightthickness=0  # Remove the border around the canvas
            )
            self.canvas.grid(row=1, column=0, columnspan=2)

            try:
                self.image = PhotoImage(file=self.image_path)
                # Resize image if necessary
                self.image = self.image.subsample(
                    max(1, int(self.image.width() / self.image_size[0])),
                    max(1, int(self.image.height() / self.image_size[1]))
                )
                # Place the image on the canvas
                self.canvas.create_image(
                    self.image_size[0] // 2,  # Center the image horizontally
                    self.image_size[1] // 2,  # Center the image vertically
                    image=self.image
                )
            except Exception as e:
                logger.error(f"Failed to load image: {e}")
                self.image = None
        else:
            self.image = None

        # Set up Chat Bubble
        # self.chat_text = tk.StringVar()
        # self.chat_label = tk.Label(
        #     self.root,
        #     textvariable=self.chat_text,
        #     font=('Consolas', '12'),
        #     fg='white',
        #     bg='grey30',  # Chat bubble background color
        #     bd=1,
        #     relief='solid',
        #     wraplength=150
        # )
        # self.chat_label.grid(row=2 if self.image_path else 1, column=0, columnspan=2, pady=5)

        # Define Window Geometry
        self.root.geometry("+5+5")
        self.root.lift()
        self.root.wm_attributes("-topmost", True)

    def setup_transparency(self):
        """
        Platform-specific setup for window transparency.
        """
        platform = sys.platform
        if platform == "linux" or platform == "linux2":
            # Linux transparency logic
            self.root.overrideredirect(True)
            self.root.wait_visibility(self.root)
            self.root.wm_attributes("-alpha", 0.5)
        elif platform == "darwin":
            # macOS transparency logic
            self.root.overrideredirect(True)
            self.root.wm_attributes("-topmost", True)
            self.root.wm_attributes("-transparent", True)
            self.root.config(bg='systemTransparent')
        elif platform == "win32":
            # Windows transparency logic
            self.root.overrideredirect(True)
            self.root.geometry("+250+250")
            self.root.lift()
            self.root.wm_attributes("-topmost", True)
            self.root.wm_attributes("-disabled", True)
            self.root.wm_attributes("-transparentcolor", "white")
            self.root.config(bg='white')

    def update_label(self) -> None:
        wait_time, update_text = self.get_new_text_callback()
        # self.ping_text.set(update_text)
        # self.chat_text.set(update_text)  # Update chat bubble text
        self.root.after(wait_time, self.update_label)

    def run(self) -> None:
        # self.ping_text.set(self.initial_text)
        # self.chat_text.set(self.initial_text)  # Set initial chat bubble text
        self.root.after(self.initial_delay, self.update_label)
        self.root.mainloop()
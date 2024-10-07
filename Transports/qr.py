import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk
import qrcode
from settings import *


class QRFrame(ctk.CTkFrame):
    def __init__(self, parent, x, y):
        # window setup
        ctk.set_appearance_mode('light')
        super().__init__(parent, fg_color='white')

        # Entry field
        self.entry_string = ctk.StringVar()
        self.entry_string.trace('w', self.create_qr)
        EntryField(self, self.entry_string)

        # QR code
        raw_image = Image.open('Placeholder.png').resize((150, 150))
        image_tk = ImageTk.PhotoImage(raw_image)

        self.qr_image = QrImage(self)
        self.qr_image.update_image(image_tk)

        self.place(relx=x / 1600 - 0.009, rely=y / 900, relwidth=0.948, relheight=0.828)

    def create_qr(self, *args):
        current_text = self.entry_string.get()
        if current_text:
            self.raw_image = qrcode.make(current_text)
            self.tk_image = ImageTk.PhotoImage(self.raw_image)
            self.qr_image.update_image(self.tk_image)


class EntryField(ctk.CTkFrame):
    def __init__(self, parent, entry_string):
        super().__init__(parent, corner_radius=20, fg_color=LIGHT_GREEN2)
        self.place(relx=0.5, rely=1, relwidth=1, relheight=0.4, anchor='center')

        # grid layout
        self.rowconfigure((0, 1), weight=1, uniform='a')
        self.columnconfigure(0, weight=1, uniform='a')

        # widgets
        self.frame = ctk.CTkFrame(self, fg_color='transparent')
        self.frame.columnconfigure(0, weight=1, uniform='b')
        self.frame.columnconfigure(1, weight=4, uniform='b')
        self.frame.columnconfigure(2, weight=2, uniform='b')
        self.frame.columnconfigure(3, weight=1, uniform='b')
        self.frame.grid(row=0, column=0)

        entry = ctk.CTkEntry(
            self.frame,
            textvariable=entry_string,
            fg_color=LIGHT_GREEN,
            border_width=0,
            text_color='white'
        )
        entry.grid(row=0, column=1, sticky='nsew')

        button = ctk.CTkButton(
            self.frame,
            text='save',
            fg_color=LIGHT_GREEN,
            hover_color=GRAY
        )
        button.grid(row=0, column=2, sticky='nsew', padx=10)


class QrImage(tk.Canvas):
    def __init__(self, parent):
        super().__init__(
            parent,
            background='white',
            bd=0,
            highlightthickness=0,
            relief='ridge'
        )

        self.place(relx=0.5, rely=0.4, width=300, height=300, anchor='center')

    def update_image(self, image_tk):
        self.create_image(0, 0, image=image_tk, anchor='nw')
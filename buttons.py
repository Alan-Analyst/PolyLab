from customtkinter import CTkButton
from settings import *

class Button(CTkButton):
    def __init__(self, parent, text, func, col, row, color='light-gray'):
        super().__init__(
            master=parent,
            text=text,
            corner_radius=0,
            command=func,
            fg_color=COLORS[color]['fg'],
            hover_color=COLORS[color]['hover'],
            text_color=COLORS[color]['text']
        )
        self.grid(column=col, row=row, sticky='NEWS')
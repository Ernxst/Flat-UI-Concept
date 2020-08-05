from tkinter import Button

from util.colour_constants import Colours
from util.constants import APP_FONT


class TkButton(Button):
    def __init__(self, parent, highlightthickness=0, relief='flat',
                 highlightbackground='white', activebackground=Colours.BUTTON_HOVER_BG,
                 fg='white', font=(APP_FONT, 10, 'bold'), bg=Colours.NAVBAR_BG,
                 activeforeground='white', command=None,
                 bd=0, highlightcolor='white', **kwargs):
        super().__init__(parent, highlightthickness=highlightthickness,
                         relief=relief, highlightbackground=highlightbackground,
                         activebackground=activebackground, fg=fg, font=font,
                         bg=bg, activeforeground=activeforeground,
                         command=command, bd=bd, highlightcolor=highlightcolor, **kwargs)


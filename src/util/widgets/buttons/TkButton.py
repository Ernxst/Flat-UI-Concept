from tkinter import Button

from util.constants import APP_FONT, BUTTON_HOVER_BG, BUTTON_BG


class TkButton(Button):
    def __init__(self, parent, highlightthickness=0, relief='flat',
                 highlightbackground='red', activebackground=BUTTON_HOVER_BG,
                 fg='white', font=(APP_FONT, 10, 'bold'), bg=BUTTON_BG,
                 activeforeground='white', command=None,
                 bd=0, highlightcolor='white', **kwargs):
        super().__init__(parent, highlightthickness=highlightthickness,
                         relief=relief, highlightbackground=highlightbackground,
                         activebackground=activebackground, fg=fg, font=font,
                         bg=bg, activeforeground=activeforeground,
                         command=command, bd=bd, highlightcolor=highlightcolor, **kwargs)


from tkinter import Frame, OptionMenu, StringVar, Label, BooleanVar, DoubleVar, IntVar

from util.colour_constants import Colours
from util.constants import APP_FONT


class TkOptionMenu(Frame):
    def __init__(self, master, title, options, variable=None, default=None,
                 anchor='center',
                 bg=Colours.NAVBAR_BG, menubg=Colours.PROFILE_BG, fg='black',
                 activeforeground='white', relief='flat', menufg='white', buttonfg='white',
                 hoverbackground=Colours.BUTTON_HOVER_BG,  font=(APP_FONT, 10)):
        super().__init__(master, highlightthickness=0, bg=master['bg'])
        default = default if default else options[0]
        self._var = variable if variable else self._get_var_type(default)
        self._var.set(default)
        self._header = Label(self, text=title, bg=self['bg'], fg=fg, font=font,
                             activebackground=self['bg'], anchor=anchor)
        width = max(len(title), len(max([str(x) for x in options], key=len)))
        self._dropdown = OptionMenu(self, self._var, *options)
        self._dropdown.config(highlightthickness=0, bg=bg, fg=buttonfg, font=font,
                              bd=0, width=width, relief=relief,
                              activebackground=hoverbackground,
                              activeforeground=activeforeground, indicatoron=False)
        self._dropdown["menu"].config(bg=menubg, fg=menufg, font=font, relief=relief,
                                      activebackground=hoverbackground,
                                      activeforeground=activeforeground,
                                      activeborderwidth=0, bd=0)
        print(self._dropdown["menu"].keys())
        print(self._dropdown.keys())

    def _get_var_type(self, first_option):
        if isinstance(first_option, int):
            return IntVar()
        if isinstance(first_option, float):
            return DoubleVar()
        if isinstance(first_option, bool):
            return BooleanVar()
        return StringVar()

    def grid(self, **kwargs):
        super(Frame, self).grid(**kwargs)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1, uniform='rows')
        self._header.grid(row=0, column=0, sticky='nesw')
        self._dropdown.grid(row=1, column=0, sticky='nesw', ipady=5)

    def get(self):
        return self._var.get()
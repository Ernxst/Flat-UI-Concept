from tkinter import Frame, Label, IntVar, DoubleVar, BooleanVar, StringVar
from tkinter.ttk import Combobox, Style

from util.colour_constants import Colours
from util.constants import APP_FONT


class TkCombobox(Frame):
    def __init__(self, master, title, options, variable=None, default=None,
                 anchor='center', bg=Colours.NAVBAR_BG, menubg=Colours.PROFILE_BG,
                 fg='black', activeforeground='white', relief='flat', menufg='white',
                 buttonfg='white', hoverbackground=Colours.BUTTON_HOVER_BG,
                 font=(APP_FONT, 10)):
        super().__init__(master, highlightthickness=0, bg=master['bg'])
        self._bg = bg
        self._button_fg = buttonfg
        self._menu_bg = menubg
        self._menu_fg = menufg
        self._active_fg = activeforeground
        self._relief = relief
        self._hoverbackground = hoverbackground

        default = default if default else options[0]
        self._var = variable if variable else self._get_var_type(default)
        self._var.set(default)
        self.header = Label(self, text=title, bg=self['bg'], fg=fg, font=font,
                            activebackground=self['bg'], anchor=anchor)
        style_name = title + '.TCombobox'
        self.style = self.set_style(font, style_name)
        self._dropdown = Combobox(self, values=options, font=font,
                                  state='readonly', textvariable=self._var,
                                  justify='center', background=bg,
                                  foreground=buttonfg, style=style_name)

        self._dropdown.bind('<Enter>', lambda event: self.on_enter(style_name))
        self._dropdown.bind('<Leave>', lambda event: self.on_leave(style_name))
        self._dropdown.bind('<<ComboboxSelected>>', lambda event: self.remove_highlight())

    def remove_highlight(self):
        self._dropdown.selection_clear()

    def on_enter(self, style_name):
        self.style.map(style_name, fieldbackground=[('readonly', self._hoverbackground)])
        self.style.map(style_name, selectbackground=[('readonly', self._hoverbackground)])
        self.style.map(style_name, background=[('readonly', self._hoverbackground)])

    def on_leave(self, style_name):
        self.style.map(style_name, fieldbackground=[('readonly', self._bg)])
        self.style.map(style_name, selectbackground=[('readonly', self._bg)])
        self.style.map(style_name, background=[('readonly', self._bg)])

    def set_style(self, font, style_name):
        self.option_add('*TCombobox*Listbox.font', font)
        self.option_add('*TCombobox*Listbox*Background', self._menu_bg)
        self.option_add('*TCombobox*Listbox*Foreground', self._menu_fg)
        self.option_add('*TCombobox*Listbox*justify', 'center')
        self.option_add('*TCombobox*Listbox*selectBackground', self._hoverbackground)
        self.option_add('*TCombobox*Listbox*selectForeground', self._active_fg)

        style = Style()
        style.map(style_name, selectbackground=[('readonly', self._bg)])
        style.map(style_name, selectforeground=[('readonly', self._active_fg)])
        style.map(style_name, fieldbackground=[('readonly', self._bg)])
        style.map(style_name, arrowsize=[('readonly', 0)])
        style.map(style_name, exportselection=[('readonly', False)])
        style.configure(style_name, fieldbackground=self._bg, background=self._bg)
        style.layout(style_name, [('Button.border', 0)])
        return style

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
        self.header.grid(row=0, column=0, sticky='nesw')
        self._dropdown.grid(row=1, column=0, sticky='nesw', ipady=10)

    def get(self):
        return self._var.get()

from tkinter import Frame

from Labels.TkLabels import TkMessage
from src.models.Model import get_model
from src.util.constants import APP_FONT, BUTTON_HOVER_BG, GREY, RED, DARK_RED, TITLE_BG
from src.util.widgets.buttons.TkButton import TkButton
from src.util.widgets.labels.ImageLabel import ImageLabel


class NotificationButton(Frame):
    def __init__(self, master, id_, name, icon, title, msg, date_sent,
                 cmd=None, clear_cmd=None, bg=None):
        bg = bg if bg else master['bg']
        super().__init__(master, bg=bg, highlightthickness=1,
                         highlightbackground=master['bg'], highlightcolor=master['bg'])
        self._active_fg = 'black'
        self._fg = 'white'
        self._active_bg = GREY
        self._bg = bg
        self._highlight_border = 'white'
        self._active_border = TITLE_BG
        self._hover_bg = BUTTON_HOVER_BG
        self._enabled = False

        self._id_ = id_
        self._clear_cmd = clear_cmd
        self._cmd = cmd

        self._icon_label = ImageLabel(self, icon, 0.45)
        self._name_lbl = TkMessage(self, text=name, font=(APP_FONT, 10, 'bold'), anchor='e',
                                   justify='left',  bg=self['bg'])
        self._title_lbl = TkMessage(self, text=title, font=(APP_FONT, 12, 'bold'), anchor='w',
                                    justify='left', bg=self['bg'])
        self._msg = TkMessage(self, text=msg, font=(APP_FONT, 10), anchor='w', justify='left')
        self._date_lbl = TkMessage(self, text=date_sent, font=(APP_FONT, 8), bg=self['bg'],
                                   anchor='e', justify='right')

    def _config_grid(self):
        self.rowconfigure((0, 1, 2), weight=1, uniform='rows')
        self.columnconfigure((1, 2), weight=1, uniform='cols')

    def grid(self, **kwargs):
        super().grid(**kwargs)
        self._config_grid()
        self._show()
        self._bind_events()

    def _bind_events(self):
        for widget in [self] + self.winfo_children():
            widget.bind('<Enter>', lambda event: self._on_enter())
            widget.bind('<Leave>', lambda event: self._on_leave())
            widget.bind('<ButtonRelease-1>', lambda event: self._on_click())

    def _show(self):
        self._title_lbl.grid(row=0, column=1, sticky='nesw', pady=(5, 0))
        self._name_lbl.grid(row=0, column=2, sticky='nesw', pady=(5, 0))
        self._msg.grid(row=1, column=1, columnspan=2, sticky='nesw')
        self._date_lbl.grid(row=2, column=1, columnspan=2, sticky='nesw')
        self._icon_label.grid(row=0, column=0, sticky='nesw', rowspan=3, padx=10)
        TkButton(self, text='X', font=(APP_FONT, 10, 'bold'), command=self._clear_notification,
                 bg=RED, activebackground=DARK_RED).grid(row=0, column=3, rowspan=3, sticky='nesw')

    def _on_click(self):
        if self._cmd is not None:
            self._cmd()

    def _on_enter(self):
        if not self._enabled:
            self.config(highlightbackground=self._highlight_border,
                        bg=self._hover_bg, highlightcolor=self._highlight_border)
            for widget in self.winfo_children()[:-1]:
                widget.config(bg=self._hover_bg)

    def _on_leave(self):
        if not self._enabled:
            self.config(highlightbackground=self._bg, bg=self._bg)
            for widget in self.winfo_children()[:-1]:
                widget.config(bg=self._bg)

    def enable(self):
        self.focus_set()
        self._enabled = True
        self.config(highlightbackground=self._active_border,
                    bg=self._active_bg, highlightcolor=self._active_border)
        for widget in self.winfo_children()[:-1]:
            widget.config(bg=self._active_bg, fg=self._active_fg)

    def disable(self):
        self._enabled = False
        self.config(highlightbackground=self._bg, bg=self._bg)
        for widget in self.winfo_children()[:-1]:
            widget.config(bg=self._bg, fg=self._fg)

    def _clear_notification(self):
        get_model().clear_notification(self._id_)
        if self._clear_cmd is not None:
            self._clear_cmd()
        if self._cmd is not None:
            self._cmd()
        self.destroy()

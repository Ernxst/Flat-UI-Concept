from tkinter import Frame

from Labels.TkLabels import TkMessage
from src.util.constants import APP_FONT, BUTTON_HOVER_BG, MAX_MSG_PREVIEW_LENGTH, GREY
from src.util.widgets.labels.ImageLabel import ImageLabel


class ChatPreview(Frame):
    def __init__(self, master, name, icon, last_msg, date_sent, cmd):
        super().__init__(master, bg=master['bg'], highlightthickness=1,
                         highlightbackground=master['bg'], highlightcolor=master['bg'])
        self._active_fg = 'black'
        self._fg = 'white'
        self._active_bg = GREY
        self._bg = master['bg']
        self._highlight_border = 'white'
        self._active_border = self._active_bg
        self._hover_bg = BUTTON_HOVER_BG
        self._enabled = False

        self._name, self._icon, self._cmd = name, icon, cmd
        self._last_msg, self._date_sent = last_msg, date_sent
        self._enabled = False
        self._icon_label = ImageLabel(self, icon, 0.45)
        self._name_lbl = TkMessage(self, text=name, font=(APP_FONT, 12, 'bold'),
                                   anchor='w', justify='left')
        self._msg = TkMessage(self, text=self._get_msg(last_msg), font=(APP_FONT, 10))
        self._date_lbl = TkMessage(self, text=date_sent, font=(APP_FONT, 8),
                                   anchor='e', justify='right')

    def _get_msg(self, msg):
        if len(msg) > MAX_MSG_PREVIEW_LENGTH:
            msg = msg[:MAX_MSG_PREVIEW_LENGTH - 4] + ' ...'
        return msg

    def _config_grid(self):
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=3, uniform='chat')
        self.columnconfigure((1, 2), weight=2, uniform='chat')

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
        self._name_lbl.grid(row=0, column=1, columnspan=2, sticky='nesw', pady=(5, 0))
        self._msg.grid(row=1, column=1, columnspan=2, sticky='nesw')
        self._date_lbl.grid(row=2, column=2, sticky='nesw')
        self._icon_label.grid(row=0, column=0, sticky='nesw', rowspan=3)

    def _on_click(self):
        self.enable()
        if self._cmd is not None:
            self._cmd()

    def _on_enter(self):
        if not self._enabled:
            self.config(highlightbackground=self._highlight_border,
                        bg=self._hover_bg, highlightcolor=self._highlight_border)
            for widget in self.winfo_children():
                widget.config(bg=self._hover_bg)

    def _on_leave(self):
        if not self._enabled:
            self.config(highlightbackground=self._bg, bg=self._bg)
            for widget in self.winfo_children():
                widget.config(bg=self._bg)

    def enable(self):
        self.focus_set()
        self._enabled = True
        self.config(highlightbackground=self._active_border,
                    bg=self._active_bg, highlightcolor=self._active_border)
        for widget in self.winfo_children():
            widget.config(bg=self._active_bg, fg=self._active_fg)

    def disable(self):
        self._enabled = False
        self.config(highlightbackground=self._bg, bg=self._bg)
        for widget in self.winfo_children():
            widget.config(bg=self._bg, fg=self._fg)
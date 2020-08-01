from abc import abstractmethod
from tkinter import Frame

from util.constants import TITLE_BG, BUTTON_HOVER_BG, GREY


class FrameButton(Frame):
    def __init__(self, master, bg=None, cmd=None, activeforeground='black',
                 fg='white', activebackground=GREY, highlightborder='white',
                 activeborder=TITLE_BG, hoverbackground=BUTTON_HOVER_BG):
        bg = bg if bg else master['bg']
        super().__init__(master, bg=bg, highlightthickness=1,
                         highlightbackground=master['bg'], highlightcolor=master['bg'])
        self._active_fg = activeforeground
        self._fg = fg
        self._active_bg = activebackground
        self._bg = bg
        self._highlight_border = highlightborder
        self._active_border = activeborder
        self._hover_bg = hoverbackground
        self._enabled = False

        self._cmd = cmd

    @abstractmethod
    def _config_grid(self):
        pass

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

    @abstractmethod
    def _show(self):
        pass

    def _on_click(self):
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
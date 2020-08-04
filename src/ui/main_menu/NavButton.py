from util.constants import MENU_PAGE_BG, BUTTON_HOVER_BG
from util.widgets.buttons.FrameButton import FrameButton
from util.widgets.buttons.TkButton import TkButton
from util.widgets.labels.ImageLabel import ImageLabel


class NavButton(FrameButton):
    def __init__(self, master, text, icon, command, fg='white', activeforeground='black',
                 activebackground=MENU_PAGE_BG, activeborder=MENU_PAGE_BG,
                 hoverforeground='black', highlightborder='white',
                 hoverbackground=BUTTON_HOVER_BG, ratio=0.25):
        super().__init__(master, cmd=command, bg=master['bg'], fg=fg,
                         activeforeground=activeforeground, highlightborder=highlightborder,
                         activebackground=activebackground, activeborder=activeborder,
                         hoverbackground=hoverbackground)
        self._grid_kw = {}
        self._icon_label = ImageLabel(self, icon, ratio)
        self._button = TkButton(self, text=text, command=command, bg=self['bg'],
                                activebackground=hoverbackground, fg=fg,
                                activeforeground=hoverforeground,
                                anchor='w', disabledforeground=self._active_fg)

    def _config_grid(self):
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1, uniform='button')
        self.columnconfigure(1, weight=3, uniform='button')

    def grid(self, **kwargs):
        super().grid(**kwargs)
        self._grid_kw = kwargs

    def _show(self):
        self._button.grid(row=0, column=1, sticky='nesw')
        self._icon_label.grid(row=0, column=0, sticky='nesw')

    def _on_click(self):
        self.enable()
        super()._on_click()

    def enable(self):
        super().enable()
        self._button.config(state='disabled')

    def disable(self):
        super().disable()
        self._button.config(state='normal')

    def minimise(self):
        self._button.grid_forget()
        self._icon_label.grid(row=0, column=0, sticky='nesw', columnspan=2)

    def maximise(self):
        self._button.grid(row=0, column=1, sticky='nesw')
        self._icon_label.grid(row=0, column=0, sticky='nesw', columnspan=1)

    def hide(self):
        self.grid_forget()

    def show(self):
        super().grid(**self._grid_kw)
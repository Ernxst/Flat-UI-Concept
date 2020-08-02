from util.constants import MENU_PAGE_BG
from util.widgets.buttons.TkButton import TkButton
from util.widgets.labels.ImageLabel import ImageLabel
from util.widgets.buttons.FrameButton import FrameButton


class NavButton(FrameButton):
    def __init__(self, master, text, icon, command):
        super().__init__(master, cmd=command, bg=master['bg'],
                         activebackground=MENU_PAGE_BG, activeborder=MENU_PAGE_BG)
        self._grid_kw = {}
        self._icon_label = ImageLabel(self, icon)
        self._button = TkButton(self, text=text, command=command, bg=self['bg'],
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
from tkinter import Frame

from Frames.ScrollableFrame import ScrollableFrame
from src.util.constants import GREY, NAVBAR_BG


class ScrolledFrame(ScrollableFrame):
    def __init__(self, parent, bg=None, highlightthickness=0, scrollbar_bg=NAVBAR_BG,
                 activescrollbar_bg='light blue', troughcolor=GREY):
        if not bg:
            bg = parent['bg']
        super().__init__(parent, bg, highlightthickness, scrollbar_bg,
                         activescrollbar_bg, troughcolor)

    def grid(self, scrollpady=10, scrollpadx=(5, 0), **kwargs):
        super(Frame, self).grid(**kwargs)
        self.canvas.grid(row=0, column=0, sticky='nesw')
        self.vsb.grid(row=0, column=1, sticky='nesw', padx=scrollpadx, pady=scrollpady)
        self.set_scroll_binding()

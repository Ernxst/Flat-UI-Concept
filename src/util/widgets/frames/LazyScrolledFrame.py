from tkinter import Canvas

from Util.tkUtilities import get_widget_dimensions
from util.constants import NAVBAR_BG, GREY
from util.widgets.frames.ScrolledFrame import ScrolledFrame


class LazyScrolledFrame(ScrolledFrame):
    def __init__(self, master, bg=None, highlightthickness=0, scrollbar_bg=NAVBAR_BG,
                 activescrollbar_bg='light blue', troughcolor=GREY, highlightbackground='white'):
        super().__init__(master, bg, highlightthickness, scrollbar_bg, activescrollbar_bg,
                         troughcolor, highlightbackground)
        self._widgets, self._shown_widgets = {}, []
        self._width, self._height = 1, 1
        self._current_row = 0
        self.canvas.yview_scroll, self.canvas.yview = self.yview_scroll, self.yview

    def _resize(self, event):
        self._width, self._height = event.width, event.height
        self._show_widgets()

    def grid(self, **kwargs):
        super().grid(**kwargs)
        self._width, self._height = get_widget_dimensions(self)
        self._show_widgets()
        self.bind('<Configure>', self._resize)

    def _show_widgets(self):
        if len(self._widgets) > 0:
            heights = self._get_heights()
            if heights > self._height:
                self.canvas.itemconfig(self.id_, height=heights)
                widgets = self._max_widgets(self._height)
            else:  # if the total height of widgets can fit, display all of them
                widgets = self._widgets
            self._show(widgets)

    def add(self, widget, **grid_kw):
        """ Add widget to drawing list"""
        self._widgets[widget] = grid_kw

    def _show(self, widgets):
        """ Display widgets """
        for widget in widgets:
            widget.grid(**self._widgets[widget])
            self._shown_widgets.append(widget)
        self._current_row = max([self._widgets[x]['row'] for x in self._shown_widgets])

    def _max_widgets(self, max_height):
        """ Return the widgets to display for the given height"""
        total_height = 0
        widgets = []
        max_row = max([y['row'] for y in self._widgets.values()])
        for i in range(self._current_row + 1, max_row + 1):
            widgets_in_row = [x for x, y in self._widgets.items() if y['row'] == i]
            new_height = max([w.winfo_reqheight() for w in widgets_in_row])
            if total_height + new_height > max_height:
                break
            total_height += new_height
            for widget in widgets_in_row:
                if widget not in self._shown_widgets:
                    widgets.append(widget)
        return widgets

    def _get_heights(self):
        """ Return the total height of widgets """
        total_height = 0
        max_row = max([y['row'] for y in self._widgets.values()])
        for i in range(max_row + 1):
            widgets_in_row = [x for x, y in self._widgets.items() if y['row'] == i]
            total_height += max([self._get_widget_height(w) for w in widgets_in_row])
        return total_height

    def _on_scroll(self):
        scroll_distance = self._scroll_distance()
        if scroll_distance > 0 and not self._all_widgets_shown():  # if scrolling downwards
            max_widgets = self._max_widgets(scroll_distance)  # generate next batch
            self._show(max_widgets)  # show next batch

    def _get_widget_height(self, widget):
        return max(widget.winfo_reqheight(), get_widget_dimensions(widget)[1])

    def _all_widgets_shown(self):
        return all(x.winfo_ismapped() for x in self._widgets)

    def _scroll_distance(self):
        """ Get the distance scrolled by the user since the last scroll """
        return self.vsb.get()[1] * self._height

    def _disable_scroll(self):
        """ Disable scrolling while showing the next batch of widgets """
        self.vsb.config(command=None)

    def _enable_scroll(self):
        """ Re-enable scrolling """
        self.vsb.config(command=self.yview)

    def yview(self, *args):
        self._disable_scroll()
        self._on_scroll()
        super(Canvas, self.canvas).yview(*args)
        self._enable_scroll()

    def yview_scroll(self, *args):
        self._disable_scroll()
        self._on_scroll()
        super(Canvas, self.canvas).yview_scroll(*args)
        self._enable_scroll()

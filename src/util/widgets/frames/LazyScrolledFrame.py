from tkinter import Canvas

from Util.tkUtilities import get_widget_dimensions
from util.constants import Colours
from util.widgets.frames.ScrolledFrame import ScrolledFrame


class LazyScrolledFrame(ScrolledFrame):
    def __init__(self, master, bg=None, highlightthickness=0, scrollbar_bg=Colours.NAVBAR_BG,
                 activescrollbar_bg='light blue', troughcolor=Colours.GREY, highlightbackground='white'):
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

    def widget_grid_info(self, widget):
        return self._widgets[widget]

    def _show_widgets(self):
        if len(self._widgets) > 0:
            heights = self._get_heights()
            if heights > self._height:
                self.canvas.itemconfig(self.id_, height=heights)
                widgets = self._max_widgets(self._height)
            else:  # if the total height of widgets can fit, display all of them
                widgets = self._widgets
            self._show(widgets, self._height)

    def add(self, widget, **grid_kw):
        """ Add widget to drawing list """
        self._widgets[widget] = grid_kw

    def _show(self, widgets, max_height):
        if len(widgets) > 0:
            max_row = max([self._widgets[x]['row'] for x in widgets])
            self._widget_loop(max_row, max_height, self._draw_widget)
            self._current_row = max([self._widgets[x]['row'] for x in self._shown_widgets]) + 1

    def _draw_widget(self, widget, *args):
        self.update_idletasks()
        widget.grid(**self._widgets[widget])
        self._shown_widgets.append(widget)

    def _max_widgets(self, max_height):
        """ Get the next batch of widgets to draw """
        return self._widget_loop(self._get_max_row(), max_height, self._append)

    def _append(self, widget, widgets):
        if widget not in self._shown_widgets:
            widgets.append(widget)
        return widgets

    def _widget_loop(self, max_row, max_height, function):
        """ Reduce repetition """
        total_height, widgets = 0, []
        for i in range(self._current_row, max_row + 1):
            row_height, widgets_in_row = self._get_row_height(i)
            if total_height + row_height > max_height:
                break
            total_height += row_height
            for widget in widgets_in_row:
                widgets = function(widget, widgets)
        return widgets

    def _get_max_row(self):
        return max([y['row'] for y in self._widgets.values()])

    def _get_row_height(self, row):
        """ Return the tallest widget in a given row """
        widgets_in_row = [x for x, y in self._widgets.items() if y['row'] == row]
        return max([self._get_widget_height(w) for w in widgets_in_row]), widgets_in_row

    def _get_heights(self):
        """ Get total height of widgets """
        return sum([self._get_row_height(x)[0] for x in range(self._get_max_row() + 1)])

    def _on_scroll(self):
        scroll_distance = self._scroll_distance()
        if scroll_distance > 0 and not self._all_widgets_shown():  # if scrolling downwards
            max_widgets = self._max_widgets(scroll_distance)  # generate next batch
            self._show(max_widgets, scroll_distance)  # show next batch

    def _get_widget_height(self, widget):
        return max(widget.winfo_reqheight(), get_widget_dimensions(widget)[1])

    def _all_widgets_shown(self):
        return all(x.winfo_ismapped() for x in self._widgets)

    def _scroll_distance(self):
        """ Convert scrollbar offset to pixels """
        return self.vsb.get()[1] * self._height

    def _disable_scroll(self):
        """ Disable scrolling while displaying a batch of widgets """
        self.vsb.config(command=None)

    def _enable_scroll(self):
        self.vsb.config(command=self.yview)

    def yview(self, *args):
        self._scroll(super(Canvas, self.canvas).yview, *args)

    def yview_scroll(self, *args):
        self._scroll(super(Canvas, self.canvas).yview_scroll, *args)

    def _scroll(self, func, *args):
        self._disable_scroll()
        self._on_scroll()
        func(*args)
        self._enable_scroll()

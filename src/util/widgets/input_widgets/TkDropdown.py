from platform import system
from tkinter import Toplevel, TclError

from Util.tkUtilities import get_widget_dimensions
from util.colour_constants import Colours
from util.constants import MAX_DROPDOWN_TEXT_LENGTH
from util.widgets.buttons.TkButton import TkButton
from util.widgets.misc.TkWin import get_win


def close_dropdown():
    TkDropdown.INSTANCE.destroy()
    TkDropdown.INSTANCE = None


def show_dropdown(widget, options, anchor='s'):
    if len(options) == 0:
        return
    if TkDropdown.INSTANCE is not None:
        if TkDropdown.INSTANCE.get_widget() == widget:
            return
        close_dropdown()
    widget.original_bg = widget['bg']
    try:
        bg = widget['activebackground']
    except TclError:
        bg = Colours.BUTTON_HOVER_BG
    widget.config(bg=bg)
    TkDropdown.INSTANCE = TkDropdown(get_win(), widget, options, anchor)


class TkDropdown(Toplevel, object):
    INSTANCE = None

    def __init__(self, master, widget, options, anchor='s'):
        super().__init__(master)
        if anchor not in ('n', 'e', 's', 'w'):
            raise TclError('Bad anchor "{}". Must be one of n, e, s, w'.format(anchor))
        self._widget = widget
        self._dropdown_options = options
        self._anchor = anchor
        self._width, self._height = 1, 1
        self._widget_width, self._widget_height = get_widget_dimensions(self._widget)
        self._show()

    def get_widget(self):
        return self._widget

    def _config_dropdown(self):
        self.columnconfigure(0, weight=1)
        self.rowconfigure(tuple(range(len(self._dropdown_options))), weight=1, uniform='drop')
        self.transient(self.master)
        if system() == 'Linux':
            self.wm_attributes('-type', 'notification')
        else:
            self.overrideredirect(True)

    def _position(self):
        width, height = self._widget_width, self._widget_height = get_widget_dimensions(self._widget)
        hw, hh = int(width / 2), int(height / 2)
        x, y = self._widget.winfo_rootx(), self._widget.winfo_rooty()
        anchors = {'n': (x, y - height), 'e': (x + width, y + hh),
                   's': (x, y + height), 'w': (x - width, y + hh)}
        self._width, self._height = get_widget_dimensions(self)
        self.geometry('{}x{}+{}+{}'.format(max(self._width, width), self._height,
                                           *anchors[self._anchor]))

    def _show(self):
        self._show_options()
        self._config_dropdown()
        self._position()
        self._bind_events()

    def _bind_events(self):
        self.master.bind('<Leave>', lambda event: self._on_leave())
        self.bind('<Leave>', lambda event: self._on_leave())
        self.master.bind('<Configure>', lambda event: self._position())

    def _on_leave(self):
        x, y = self.master.winfo_pointerxy()
        widget = self.master.winfo_containing(x, y)
        if widget != self._widget and widget not in self.winfo_children():
            self.destroy()

    def destroy(self):
        self.master.unbind('<Configure>')
        self.master.unbind('<Leave>')
        TkDropdown.INSTANCE = None
        self._widget.config(bg=self._widget.original_bg)
        super().destroy()

    def _show_options(self):
        for option, cmd in self._dropdown_options.items():
            TkButton(self, text=self._get_option(option), command=cmd, anchor='w',
                     bg=self._widget['bg'], activeforeground='black',
                     activebackground=self._widget.original_bg).grid(sticky='nesw')

    def _get_option(self, option):
        if len(option) > MAX_DROPDOWN_TEXT_LENGTH:
            return option[:MAX_DROPDOWN_TEXT_LENGTH - 4] + ' ...'
        return option

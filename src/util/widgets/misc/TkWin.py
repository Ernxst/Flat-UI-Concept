from tkinter import Tk, PhotoImage, TclError

from Entries.TransparentEntry import TransparentEntry
from Util.tkUtilities import centralise, get_screen_size, ask_ok_cancel
from models.Model import get_model
from util.VariableHolder import Vars
from util.colour_constants import convert
from util.constants import APP_FONT, WINDOW_MULTIPLIER
from util.widgets.buttons.FrameButton import FrameButton


def toggle_dark_mode():
    get_win().toggle_dark_mode()


def shutdown():
    get_model().logout()


def resize_window(width, height):
    get_win().resize_window(width, height)


def get_win():
    return TkWin.INSTANCE


def open_popup(popup, *args, **kwargs):
    return get_win().open_popup(popup, *args, **kwargs)


class TkWin(Tk):
    INSTANCE = None

    def __init__(self, title, bg, icon):
        super().__init__(className=title, baseName=title)
        TkWin.INSTANCE = self
        self.win_name = title
        self._max_width, self._max_height, self._width, self._height = self.set_win_size()
        self.set_appearance(bg, icon)
        self._popup = None
        self._dark_mode = False
        self.bind_events()

    def set_appearance(self, bg, icon):
        self.title(self.win_name)
        self.rowconfigure(0, weight=1, uniform='win')
        self.columnconfigure(0, weight=1, uniform='win')
        self.tk.call('wm', 'iconphoto', self._w, PhotoImage(file=icon))
        self.config(bg=bg)
        self.option_add('*Dialog.msg.font', '{} {}'.format(APP_FONT, 10))
        self.disable_resize()
        centralise(self, self._width, self._height, self._max_width, self._max_height)

    def set_win_size(self):
        width, height = get_screen_size(self)
        w, h = int(width * WINDOW_MULTIPLIER), int(height * WINDOW_MULTIPLIER)
        return width, height, w, h

    def bind_events(self):
        self.bind('<Escape>', lambda event: self.disable_fullscreen())
        self.bind('<F11>', lambda event: self.enable_fullscreen())
        self.protocol("WM_DELETE_WINDOW", self.destroy)

    def destroy(self, event=None):
        try:
            if ask_ok_cancel('Quit?', 'Do you really want to exit the application?'):
                self.close_win()
        except AttributeError:
            self.close_win()

    def close_win(self):
        # perform closing tasks
        shutdown()
        super().destroy()

    def enable_fullscreen(self):
        self.enable_resize()
        self.update_idletasks()
        self.wm_attributes("-fullscreen", True)
        self.update_idletasks()

    def disable_fullscreen(self):
        self.enable_resize()
        self.update_idletasks()
        self.wm_attributes("-fullscreen", False)
        self.update_idletasks()
        self.disable_resize()
        centralise(self, self._width, self._height, self._max_width, self._max_height)

    def enable_resize(self):
        self.update_idletasks()
        self.resizable(True, True)
        self.update_idletasks()

    def disable_resize(self):
        self.update_idletasks()
        self.resizable(False, False)
        self.update_idletasks()

    def resize_window(self, width, height):
        self.enable_resize()
        self._width, self._height = width, height
        centralise(self, width, height, self._max_width, self._max_height)
        self.disable_resize()

    def bring_to_front(self):
        self.attributes('-topmost', True)
        self.attributes('-topmost', False)
        self.focus_set()

    def open_popup(self, popup, *args, **kwargs):
        if not self._popup:
            self._popup = popup(self, *args, **kwargs)
        else:
            self._popup.lift()

    def toggle_dark_mode(self):
        for widget in self.winfo_children():
            self._convert_colour(widget)
            self._convert_children(widget)

    def _convert_children(self, widget):
        children = widget.winfo_children()
        if children:
            for child in children:
                self._convert_colour(child)
                self._convert_children(child)

    def _convert_colour(self, widget):
        for attribute in ('bg', 'fg', 'highlightbackground', 'highlightcolor',
                          'activebackground', 'disabledforeground', 'activeforeground'):
            self._convert(widget, attribute)
        if isinstance(widget, FrameButton):
            widget.toggle_dark_mode()
        if isinstance(widget, TransparentEntry):
            widget.bg = convert(widget.bg, Vars.DARK_MODE.get())
            widget.separator_bg = convert(widget.separator_bg, Vars.DARK_MODE.get())

    def _convert(self, widget, attribute):
        try:
            widget[attribute] = convert(widget[attribute], Vars.DARK_MODE.get())
        except (TclError, KeyError):
            pass
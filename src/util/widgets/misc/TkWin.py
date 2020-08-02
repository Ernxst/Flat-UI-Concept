from tkinter import Tk, PhotoImage

from Util.tkUtilities import centralise, get_screen_size, ask_ok_cancel
from models.Model import get_model
from src.util.constants import APP_FONT, MAX_WINDOW_MULTIPLIER, MIN_WINDOW_MULTIPLIER, WINDOW_MULTIPLIER


def shutdown():
    get_model().logout()


def get_win():
    return TkWin.INSTANCE


def open_popup(popup, *args, **kwargs):
    return get_win().open_popup(popup, *args, **kwargs)


class TkWin(Tk):
    INSTANCE = None

    def __init__(self, title, bg, icon):
        super().__init__(className=title, baseName=title)
        self.win_name = title
        max_width, max_height, w, h = self.set_win_size()
        self.set_default_size(max_width, max_height, w, h)
        self.set_appearance(bg, icon, max_width, max_height, w, h)
        self._popup = None
        self.bind_events()
        TkWin.INSTANCE = self

    def set_appearance(self, bg, icon, max_width, max_height, width, height):
        self.title(self.win_name)
        self.rowconfigure(0, weight=1, uniform='win')
        self.columnconfigure(0, weight=1, uniform='win')
        self.tk.call('wm', 'iconphoto', self._w, PhotoImage(file=icon))
        self.config(bg=bg)
        self.option_add('*Dialog.msg.font', '{} {}'.format(APP_FONT, 10))
        centralise(self, width, height, max_width, max_height)

    def set_default_size(self, max_width, max_height, w, h):
        self.wm_minsize(int(max_width * MIN_WINDOW_MULTIPLIER), int(max_height * MIN_WINDOW_MULTIPLIER))
        self.wm_maxsize(int(max_width * MAX_WINDOW_MULTIPLIER), int(max_height * MAX_WINDOW_MULTIPLIER))
        self.aspect(w, h, w, h)

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
        self.attributes("-fullscreen", True)

    def disable_fullscreen(self):
        self.attributes("-fullscreen", False)

    def bring_to_front(self):
        self.attributes('-topmost', True)
        self.attributes('-topmost', False)
        self.focus_set()

    def open_popup(self, popup, *args, **kwargs):
        if not self._popup:
            self._popup = popup(self, *args, **kwargs)
        else:
            self._popup.lift()

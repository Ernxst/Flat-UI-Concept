from tkinter import Tk, PhotoImage

from Util.tkUtilities import centralise, get_screen_size, get_widget_dimensions, ask_ok_cancel
from util.constants import APP_FONT, MAX_WINDOW_MULTIPLIER, MIN_WINDOW_MULTIPLIER, WINDOW_MULTIPLIER


class TkWin(Tk):
    def __init__(self, title, bg, icon):
        super().__init__(className=title, baseName=title)
        self.win_name = title
        self.set_win_size()
        self.set_default_size()
        self.set_appearance(bg, icon)
        self.bind_events()

    def set_appearance(self, bg, icon):
        self.title(self.win_name)
        self.rowconfigure(0, weight=1, uniform='win')
        self.columnconfigure(0, weight=1, uniform='win')
        self.tk.call('wm', 'iconphoto', self._w, PhotoImage(file=icon))
        self.config(bg=bg)
        self.option_add('*Dialog.msg.font', '{} {}'.format(APP_FONT, 10))
        centralise(self)

    def set_default_size(self):
        width, height = get_screen_size()
        self.wm_minsize(int(width * MIN_WINDOW_MULTIPLIER), int(height * MIN_WINDOW_MULTIPLIER))
        self.wm_maxsize(int(width * MAX_WINDOW_MULTIPLIER), int(height * MAX_WINDOW_MULTIPLIER))
        width, height = get_widget_dimensions(self)
        self.aspect(width, height, width, height)

    def set_win_size(self):
        width, height = get_screen_size()
        self.geometry('{}x{}'.format(int(width * WINDOW_MULTIPLIER), int(height * WINDOW_MULTIPLIER)))

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
        super().destroy()

    def enable_fullscreen(self):
        self.attributes("-fullscreen", True)

    def disable_fullscreen(self):
        self.attributes("-fullscreen", False)

    def bring_to_front(self):
        self.attributes('-topmost', True)
        self.attributes('-topmost', False)
        self.focus_set()
from tkinter import Label

from Popups.Popup import Popup
from Util.tkUtilities import centralise
from misc.TkLoadbar import TkLoadbar
from util.constants import APP_FONT, Colours


class LoadingPopup(Popup):
    def __init__(self, parent, title, message, bg=Colours.TITLE_BG):
        super().__init__(parent, title, bg)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.loadbar = TkLoadbar(self, message=message, mode='determinate',
                                 font=(APP_FONT, 28, 'bold'), loadbar_bg=Colours.BUTTON_HOVER_BG)
        self.lbl = Label(self, fg='white', bg=self['bg'], font=(APP_FONT, 12, 'bold'),
                         anchor='s')
        self.wm_attributes('-type', 'splash')
        self.progress = 0
        self.show()

    def show(self):
        self.geometry('{}x{}'.format(self.width, self.height))
        centralise(self)
        self.resizable(False, False)
        self.loadbar.grid(sticky='')
        self.lbl.grid(sticky='', pady=5)
        self.grab_set()

    def step(self, message, increment):
        self.progress += increment
        self.loadbar.progressbar['value'] = self.progress
        self.lbl.config(text='{} {}%'.format(message, self.progress))
        self.update_idletasks()
        self.update()

    def update(self):
        super().update()
        self.loadbar.update()

    def update_idletasks(self):
        super().update_idletasks()
        self.loadbar.update_idletasks()

    def destroy(self):
        self.grab_release()
        super().destroy()

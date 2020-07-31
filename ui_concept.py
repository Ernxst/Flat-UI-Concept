import sys

from models.Model import get_model
from ui.SplashScreen import SplashScreen
from ui.login_menu.LoginPage import LoginPage
from ui.main_menu.MenuView import MenuView
from util.Utilities import trace
from util.constants import APP_TITLE, APP_BG, PROFILE_ICON, APP_ICON
from util.widgets.misc.TkWin import TkWin

"""
TODO
 - Minimising the navbar then maximising the window and then maximising the navbar again 
     freezes the ui
 - Splash Screen Animation
 - Fix message frame sizes and icon sizes to always be the same in Messages.py
 - Image taking up too much space WelcomePage.py when notifications are shown
 - Resizing menu pages is too slow
 """


def run(screen='', debug=False):
    win = TkWin(APP_TITLE, APP_BG, APP_ICON)
    func = get_func(screen, win)
    if debug:
        trace(func)
    else:
        func()
    win.mainloop()


def get_func(screen, win):
    if screen == 'ui':
        get_model().login('Ernest')
        return lambda: MenuView(win, 'Ernest Jr Nkansah-Badu', PROFILE_ICON).grid(sticky='nesw')
    elif screen == 'login':
        return lambda: LoginPage(win).grid(sticky='nesw')
    else:
        return lambda: SplashScreen(win).grid(sticky='nesw')


if __name__ == '__main__':
    try:
        screen, debug = sys.argv[1:]
        run(screen, debug)
    except ValueError:
        run()

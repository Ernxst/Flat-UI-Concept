import sys

from src.models.Model import get_model
from src.ui.SplashScreen import SplashScreen
from src.ui.login_menu.LoginPage import LoginPage
from src.ui.main_menu.MenuView import MenuView
from src.util.Utilities import trace
from src.util.constants import APP_TITLE, APP_BG, PROFILE_ICON, APP_ICON
from src.util.widgets.misc.TkWin import TkWin

"""
TODO
 - Splash Screen Animation
 - Image taking up too much space WelcomePage.py when notifications are shown
 - Stop image flickering during navbar animation
 """


def profile(page='', debug=False):
    import cProfile
    pr = cProfile.Profile()
    pr.enable()
    run(page, debug)
    pr.disable()
    if debug:
        pr.print_stats(sort='cumtime')


def run(page='', debug=False):
    win = TkWin(APP_TITLE, APP_BG, APP_ICON)
    func = get_func(page, win)
    if debug:
        trace(func)
    else:
        func()
    win.mainloop()


def get_func(page, win):
    if page == 'ui':
        get_model().login('Ernest')
        return lambda: MenuView(win, 'Ernest Jr Nkansah-Badu', PROFILE_ICON).grid(sticky='nesw')
    elif page == 'login':
        return lambda: LoginPage(win).grid(sticky='nesw')
    else:
        return lambda: SplashScreen(win).grid(sticky='nesw')


if __name__ == '__main__':
    try:
        screen = sys.argv[1]
        profile(screen)
    except ValueError:
        profile()

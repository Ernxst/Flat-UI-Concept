import sys

from util.VariableHolder import Vars

PATH = '/home/ernest/Documents/Random Programs/Python/tkWidgets'
sys.path.insert(1, PATH)

from models.Model import get_model
from ui.SplashScreen import SplashScreen
from ui.login_menu.LoginPage import LoginPage
from ui.main_menu.MenuView import MenuView
from util.Utilities import trace
from util.constants import APP_TITLE
from util.icon_constants import PROFILE_ICON, APP_ICON
from util.colour_constants import Colours
from util.widgets.misc.TkWin import TkWin

"""
TODO
 - PATH should be found automatically
 - Splash Screen Animation
 - Welcome Page Animation
 - MenuPage width changes during navbar minimise and maximise on right edge
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
    win = TkWin(APP_TITLE, Colours.APP_BG, APP_ICON)
    Vars()
    func = get_func(page, win)
    if debug:
        trace(func)
    else:
        func()
    win.mainloop()


def get_func(page, win):
    if page == 'ui':
        model = get_model()
        model.login('Ernest')
        return lambda: MenuView(win, 'Ernest Jr Nkansah-Badu', PROFILE_ICON, model).grid(sticky='nesw')
    elif page == 'login':
        return lambda: LoginPage(win).grid(sticky='nesw')
    else:
        return lambda: SplashScreen(win).grid(sticky='nesw')


if __name__ == '__main__':
    try:
        profile(sys.argv[1])
    except (IndexError, ValueError):
        profile()

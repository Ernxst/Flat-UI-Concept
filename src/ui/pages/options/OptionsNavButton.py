from ui.main_menu.NavButton import NavButton
from util.colour_constants import Colours


class OptionsNavButton(NavButton):
    def __init__(self, master, text, icon, command):
        super().__init__(master, text, icon, command, fg='black', activebackground=Colours.NAVBAR_BG,
                         ratio=0.45, activeforeground=Colours.WHITE_)
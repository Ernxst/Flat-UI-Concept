from ui.main_menu.NavButton import NavButton
from util.constants import NAVBAR_BG, GREY


class OptionsNavButton(NavButton):
    def __init__(self, master, text, icon, command):
        super().__init__(master, text, icon, command, fg='black', hoverbackground='white',
                         activebackground=NAVBAR_BG, ratio=0.45, activeforeground=GREY)
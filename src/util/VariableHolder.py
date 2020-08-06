from tkinter import BooleanVar


class Vars:
    DARK_MODE = None
    _initialised_ = False

    def __init__(self):
        if not Vars._initialised_:
            self._init_vars()
            Vars._initialised_ = True

    def _init_vars(self):
        Vars.DARK_MODE = BooleanVar()
        Vars.DARK_MODE.set(False)

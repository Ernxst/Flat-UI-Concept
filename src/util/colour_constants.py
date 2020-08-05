from enum import Enum


class DarkMode(Enum):
    APP_BG = '#363537'
    WIN = APP_BG
    DARK = '#d9d9d9'
    TITLE_BG = '#282828'
    PROFILE_BG = '#00005A'
    NAVBAR_BG = '#1F45FC'
    NAVBAR_FG = 'White'
    NAVBAR_ACTIVE_FG = '#ffffff'
    MENU_PAGE_BG = APP_BG
    MENU_PAGE_FG = 'WHITE'
    MENU_PAGE_SUB_FG = 'WHiTE'
    RIBBON_BG = 'GRAY'
    BUTTON_HOVER_BG = 'light blue'
    LIGHT_GREEN = '#00FA9A'
    GREEN = "#49a362"
    YELLOW = "#e79f3c"
    DARK_RED = "#b22222"
    RED = "#cd5542"
    GREY = 'grey'
    DARK_GRAY = "#696969"
    BLACK = 'white'
    WHITE = '#000000'

    def __str__(self):
        return str(self.value)


class Colours(Enum):
    APP_BG = '#D8D8D8'
    DARK = '#363537'
    WIN = '#d9d9d9'
    TITLE_BG = '#282828'
    PROFILE_BG = '#00005A'
    NAVBAR_BG = '#1F45FC'
    NAVBAR_FG = 'White'
    NAVBAR_ACTIVE_FG = 'black'
    MENU_PAGE_BG = APP_BG
    MENU_PAGE_FG = 'BLACK'
    MENU_PAGE_SUB_FG = 'Gray'
    RIBBON_BG = '#ffffff'
    BUTTON_HOVER_BG = 'light blue'
    LIGHT_GREEN = '#00FA9A'
    GREEN = "#49a362"
    YELLOW = "#e79f3c"
    DARK_RED = "#b22222"
    RED = "#cd5542"
    GREY = "#edf0f5"
    DARK_GRAY = 'grey'
    BLACK = '#000000'
    WHITE = 'white'

    def __str__(self):
        return str(self.value)


class Conversion:
    DARK_MODE = {Colours.APP_BG: DarkMode.APP_BG,
                 Colours.WIN: DarkMode.WIN,
                 Colours.DARK: DarkMode.DARK,
                 Colours.TITLE_BG: DarkMode.TITLE_BG,
                 Colours.PROFILE_BG: DarkMode.PROFILE_BG,
                 Colours.NAVBAR_BG: DarkMode.NAVBAR_BG,
                 Colours.NAVBAR_FG: DarkMode.NAVBAR_FG,
                 Colours.NAVBAR_ACTIVE_FG: DarkMode.NAVBAR_ACTIVE_FG,
                 Colours.MENU_PAGE_BG: DarkMode.MENU_PAGE_BG,
                 Colours.MENU_PAGE_FG: DarkMode.MENU_PAGE_FG,
                 Colours.MENU_PAGE_SUB_FG: DarkMode.MENU_PAGE_SUB_FG,
                 Colours.RIBBON_BG: DarkMode.RIBBON_BG,
                 Colours.BUTTON_HOVER_BG: DarkMode.BUTTON_HOVER_BG,
                 Colours.GREEN: DarkMode.GREEN,
                 Colours.LIGHT_GREEN: DarkMode.LIGHT_GREEN,
                 Colours.RED: DarkMode.RED,
                 Colours.DARK_RED: DarkMode.DARK_RED,
                 Colours.GREY: DarkMode.GREY,
                 Colours.DARK_GRAY: DarkMode.DARK_GRAY,
                 Colours.BLACK: DarkMode.BLACK,
                 Colours.WHITE: DarkMode.BLACK, }
    DARK_MODE = {str(k): str(v) for (k, v) in DARK_MODE.items()}
    NORMAL = {v: k for (k, v) in DARK_MODE.items()}


def convert(colour, is_dark):
    colour = str(colour)
    if is_dark:
        return Conversion.DARK_MODE[colour]
    else:
        return Conversion.NORMAL[colour]

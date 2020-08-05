from enum import Enum

MEDIA_FOLDER = 'media/'
IMAGE_FOLDER = MEDIA_FOLDER + 'images/'

PROFILE_ICON = IMAGE_FOLDER + 'profile.png'
PROFILE_BLACK_ICON = IMAGE_FOLDER + 'profile_black.png'
BUTTON_ICON = IMAGE_FOLDER + 'options_black.png'
USERNAME_ENTRY_ICON = IMAGE_FOLDER + 'username.png'
PASSWORD_ENTRY_ICON = IMAGE_FOLDER + 'password.png'
DASHBOARD_ICON = IMAGE_FOLDER + 'dashboard'
INBOX_ICON = IMAGE_FOLDER + 'inbox.png'
MESSAGES_ICON = IMAGE_FOLDER + 'messages.png'
NOTIFICATIONS_ICON = IMAGE_FOLDER + 'notifications.png'
PLANNER_ICON = IMAGE_FOLDER + 'planner.png'
OPTIONS_ICON = IMAGE_FOLDER + 'options.png'

APP_TITLE = 'UI CONCEPT'
COPYRIGHT = '2020 Copyright Ernest Nkansah-Badu\nAll rights reserved'
APP_FONT = 'Monospace'
APP_ICON = PROFILE_ICON

WINDOW_MULTIPLIER = 0.9

LEFT_ARROW = u'\u276E'
RIGHT_ARROW = u'\u276F'
BULLET = u'\u2022'
BLANK = u"\u00A0"


# COLOUR SCHEME
class Colours(Enum):
    WIN = '#d9d9d9'
    APP_BG = '#D8D8D8'
    TITLE_BG = '#282828'
    PROFILE_BG = '#00005A'
    NAVBAR_BG = '#1F45FC'
    NAVBAR_FG = 'WHITE'
    MENU_PAGE_BG = APP_BG
    RIBBON_BG = 'WHITE'
    BUTTON_HOVER_BG = 'light blue'
    LIGHT_GREEN = '#00FA9A'
    GREEN = "#49a362"
    YELLOW = "#e79f3c"
    DARK_RED = "#b22222"
    RED = "#cd5542"
    GREY = "#edf0f5"
    DARK_MODE = ""

    def __str__(self):
        return str(self.value)


DROPLET_GROUPS = 50
WATER_COLOR = 'sky blue'
WATER_SIZE = 10
WATER_RADIUS = int(WATER_SIZE * 0.5)
MAX_WATER_BOUNCE = WATER_RADIUS
MIN_WATER_BOUNCE = 1
ANIMATION_DELAY = int(1000 / 60)
NAV_DELAY = ANIMATION_DELAY // 2

MAX_COL = 18
MIN_COL = 4
MAX_NAV_ROWS = 10

MAX_MSG_PREVIEW_LENGTH = len('TEST' * 15)
MAX_DROPDOWN_TEXT_LENGTH = 30
MAX_EVENT_DESC_LENGTH = 40

DAYS_IN_WEEK = 7
MONTHS_IN_YEAR = 12
WEEKDAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
MIN_YEAR = 2019
MAX_YEAR = 2022

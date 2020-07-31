from random import randint
from tkinter import Canvas

from Util.tkUtilities import get_widget_dimensions
from src.ui.login_menu.LoginPage import LoginPage
from src.util.Utilities import chunks
from src.util.constants import WATER_SIZE, WATER_COLOR, ANIMATION_DELAY, WATER_RADIUS, APP_TITLE, APP_FONT, \
    MAX_WATER_BOUNCE, MIN_WATER_BOUNCE, DROPLET_GROUPS


class Droplet:
    def __init__(self, master, x, y):
        self.master = master
        self._original_y = y
        self._x, self._y = x, y
        self._droplet = self._draw()
        self._water_below = self._draw_below()

    def _draw(self):
        return self.master.create_oval(self._x - WATER_SIZE, self._y - WATER_SIZE,
                                       self._x + WATER_SIZE, self._y + WATER_SIZE,
                                       fill=WATER_COLOR, width=0)

    def _draw_below(self):
        return self.master.create_rectangle(self._x - WATER_SIZE, self._y,
                                            self._x + WATER_SIZE, self._y + WATER_SIZE,
                                            fill=WATER_COLOR, width=0)

    def move(self, offset):
        self._y += offset
        self.master.coords(self._droplet, self._x - WATER_SIZE, self._y - WATER_SIZE,
                           self._x + WATER_SIZE, self._y + WATER_SIZE)
        self.master.coords(self._water_below, self._x - WATER_SIZE,
                           self._y, self._x + WATER_SIZE, self._original_y)

    def position(self):
        return self._y


class SplashScreen(Canvas):
    def __init__(self, master):
        super().__init__(master, bg=master['bg'], highlightthickness=0)
        self._width, self._height = 1, 1
        self._points = []
        self._point_chunks = []
        self._divisor = 60
        self._font_sizes = self._set_font_sizes()

    def grid(self, **kwargs):
        super().grid(**kwargs)
        self._width, self._height = get_widget_dimensions(self)
        self.create_rectangle(0, self._height, self._width, self._height,
                              fill=WATER_COLOR, width=0, tags='water')
        self.create_text(self._width / 2, self._height / 2, text='Loading',
                         tags='text', fill='white', font=(APP_FONT, 40, 'bold'))
        # self._animate()
        self._finish_animation()

    def _animate(self):
        self._points, self._point_chunks = self._create_points()
        i = 0
        while self._get_water_height() <= self._height:
            self._animate_chunks(i)
            self._animate_text(i)
            self.update()
            i += 1
            self.after(ANIMATION_DELAY)

    def _set_font_sizes(self):
        sizes = {}
        half = self._divisor // 2
        for i in range(half + 1):
            sizes[i] = 40 + i
        for i in range(half + 1):
            sizes[half + i] = sizes[half + i - 1] - 1
        return sizes

    def _create_points(self):
        points = []
        max_points = 2 * int(self._width / WATER_SIZE)
        for i in range(max_points):
            points.append(Droplet(self, i * WATER_RADIUS, self._height))
        return points, chunks(points, min(max_points, DROPLET_GROUPS))

    def _animate_text(self, index):
        self.itemconfig('text', font=(APP_FONT,
                                      self._font_sizes[index % self._divisor],
                                      'bold'))
        self.tag_raise('text')

    def _animate_chunks(self, index):
        up_1, up_2 = -MAX_WATER_BOUNCE, - MIN_WATER_BOUNCE
        down_1, down_2 = MIN_WATER_BOUNCE, MAX_WATER_BOUNCE
        for chunk_index, chunk in enumerate(self._point_chunks):
            lower, upper = self._get_bounds(chunk_index, index, up_1,
                                            up_2, down_1, down_2)
            increment = randint(lower, upper) - randint(MIN_WATER_BOUNCE, MAX_WATER_BOUNCE)
            [droplet.move(randint(increment - 1, increment + 1)) for droplet in chunk]

    def _get_bounds(self, chunk_index, index, up_1, up_2, down_1, down_2):
        if chunk_index % 2 == 0:
            if index % 2 == 0:
                return up_1, up_2
            else:
                return down_1, down_2
        else:
            if index % 2 == 0:
                return down_1, down_2
            else:
                return up_1, up_2

    def _get_water_height(self):
        return self._height - max([droplet.position() for droplet in self._points])

    def _finish_animation(self):
        self.itemconfig('text', text='Welcome to ' + APP_TITLE, font=(APP_FONT, 30, 'bold'))
        self.update()
        self.after(500)
        LoginPage(self.master).grid(row=0, column=0, sticky='nesw')
        self.destroy()

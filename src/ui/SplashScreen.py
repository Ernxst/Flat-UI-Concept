from math import sin, pi
from tkinter import Canvas

from Util.tkUtilities import get_widget_dimensions
from ui.login_menu.LoginPage import LoginPage
from util.constants import WATER_SIZE, WATER_COLOR, ANIMATION_DELAY, APP_TITLE, APP_FONT, \
    UP, WATER_BOUNCE, MAX_ANGLE, WAVES

RADS = pi / 180


class Droplet:
    def __init__(self, master, x, y):
        self.master = master
        self._x, self._y, self._original_y = x, y, y
        self._x1, self._x2 = x - WATER_SIZE, x + WATER_SIZE,
        self._droplet = self._draw()
        self._background = self._draw_background()

    def _draw(self):
        return self.master.create_oval(self._x1, self._y - WATER_SIZE,
                                       self._x2, self._y + WATER_SIZE,
                                       fill=WATER_COLOR, width=0)

    def _draw_background(self):
        return self.master.create_oval(self._x1, self._y, self._x2, 2500,
                                       fill=WATER_COLOR, width=0)

    def move(self, offset):
        self._y += offset
        self.master.move(self._droplet, 0, offset)
        self.master.move(self._background, 0, offset)

    def y(self):
        return self._y


class SplashScreen(Canvas):
    def __init__(self, master):
        super().__init__(master, bg=master['bg'], highlightthickness=0)
        self._width, self._height = 1, 1
        self._width, self._height, self._h_ratio = 1, 1, 1
        self._angles = []
        self._divisor = 60
        self._font_sizes = self._set_font_sizes()

    def grid(self, **kwargs):
        super().grid(**kwargs)
        self._width, self._height = get_widget_dimensions(self)
        self.create_text(self._width / 2, self._height / 2, text='Loading',
                         tags='text', fill='white', font=(APP_FONT, 40, 'bold'))
        self._animate()
        self._finish_animation()

    def _draw_points(self):
        self._angles = [(x, sin(x * RADS)) for x in range(MAX_ANGLE * WAVES + 1)]
        self._h_ratio = self._height / 24
        w_ratio = self._width / len(self._angles)
        return [Droplet(self, x * w_ratio, self._h_ratio * y +
                        self._height) for x, y in self._angles]

    def _animate(self):
        points = self._draw_points()
        index = 0
        i = 0
        while self._get_water_height(points) <= self._height:
            self._animate_droplets(points, index)
            self._animate_text(i)
            i += 1
            index += WATER_BOUNCE
            self.update()
            self.after(ANIMATION_DELAY)

    def _animate_droplets(self, points, index):
        for (x, y), point in zip(self._angles, points):
            new_y = sin((x + index) * RADS) * self._h_ratio
            point.move(new_y / WATER_BOUNCE)
        [point.move(UP) for point in points]

    def _set_font_sizes(self):
        sizes = {}
        half = self._divisor // 2
        for i in range(half + 1):
            sizes[i] = 40 + i
        for i in range(half + 1):
            sizes[half + i] = sizes[half + i - 1] - 1
        return sizes

    def _animate_text(self, index):
        self.itemconfig('text', font=(APP_FONT, self._font_sizes[index % self._divisor],
                                      'bold'))
        self.tag_raise('text')

    def _get_water_height(self, points):
        return self._height - max([droplet.y() for droplet in points])

    def _finish_animation(self):
        self.itemconfig('text', text='Welcome to ' + APP_TITLE, font=(APP_FONT, 30, 'bold'))
        self.update()
        self.after(500)
        LoginPage(self.master).grid(row=0, column=0, sticky='nesw')
        self.destroy()

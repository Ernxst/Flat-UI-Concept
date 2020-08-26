from math import sin, pi
from tkinter import Canvas

from Util.tkUtilities import get_widget_dimensions
from ui.login_menu.LoginPage import LoginPage
from util.constants import WATER_SIZE, WATER_COLOR, ANIMATION_DELAY, APP_TITLE, APP_FONT, \
    UP, WATER_BOUNCE, MAX_ANGLE, WAVES

RADS = pi / 180


class Droplet:
    def __init__(self, master, x, y):
        self.master, self._y = master, y
        x1, x2 = x - WATER_SIZE, x + WATER_SIZE,
        self._droplet = self._draw(x1, y - WATER_SIZE, x2, y + WATER_SIZE)
        self._background = self._draw(x1, y, x2, 3000)
        self.y = lambda: self._y

    def _draw(self, x1, y1, x2, y2):
        return self.master.create_oval(x1, y1, x2, y2, fill=WATER_COLOR, width=0)

    def move(self, offset):
        self._y += offset
        self.master.move(self._droplet, 0, offset)
        self.master.move(self._background, 0, offset)


class SplashScreen(Canvas):
    def __init__(self, master):
        super().__init__(master, bg=master['bg'], highlightthickness=0)
        self._angles = []

    def grid(self, **kwargs):
        super().grid(**kwargs)
        width, height = get_widget_dimensions(self)
        self.create_text(width / 2, height / 2, text='LOADING', tags='text',
                         fill='white', font=(APP_FONT, 40, 'bold'))
        x1, y1, x2, y2 = self.bbox('text')
        self.create_text(width / 2, y2, text='Preparing app data', tags='subtitle',
                         fill='white', font=(APP_FONT, 15, 'bold'), width=x2 - x1)
        self._animate(*self._draw_points(width, height))
        self._finish_animation()

    def _draw_points(self, width, height):
        h_ratio = 0.5 * height / WATER_BOUNCE
        self._angles = [(x, sin(x * RADS) * h_ratio)
                        for x in range(MAX_ANGLE * WAVES + 1)]
        length = len(self._angles)
        w_ratio = width / length
        return [Droplet(self, x * w_ratio, y + height)
                for x, y in self._angles], length

    def _animate(self, points, length):
        index, i = 0, 0
        while max([droplet.y() for droplet in points]) > 0:
            for x, point in enumerate(points):
                y = self._angles[(x + index) % length][1]
                point.move(UP + y / WATER_BOUNCE)
            self.tag_raise('text')
            self.tag_raise('subtitle')
            index += WATER_BOUNCE
            self.update()
            self.after(ANIMATION_DELAY)

    def _finish_animation(self):
        self.itemconfig('text', text='Welcome to ' + APP_TITLE, font=(APP_FONT, 30, 'bold'))
        self.delete('subtitle')
        self.update()
        self.after(500)
        LoginPage(self.master).grid(row=0, column=0, sticky='nesw')
        self.destroy()

from tkinter import Label, BooleanVar

from PIL.ImageTk import PhotoImage

from Util.tkUtilities import get_widget_dimensions
from util.ImageUtilities import open_image, resize_image, get_image


class ToggleSwitch(Label):
    def __init__(self, master, off_image, on_image, onvalue=True, offvalue=False,
                 command=None, variable=None, ondefault=False):
        super().__init__(master, bg=master['bg'], activebackground=master['bg'],
                         relief='flat', highlightthickness=0, bd=0,
                         highlightbackground=master['bg'], highlightcolor=master['bg'])
        if isinstance(off_image, str):
            off_image = open_image(off_image)
        if isinstance(on_image, str):
            on_image = open_image(on_image)
        self._off_img, self._on_img = off_image, on_image
        self._image = self._on_img if ondefault else self._off_img
        self._lbl_img = None

        self._off_value = offvalue
        self._on_value = onvalue
        self._variable = variable if variable else BooleanVar()
        if variable:
            value = variable.get()
        else:
            value = onvalue if ondefault else offvalue
        self._variable.set(value)
        self._width, self._height = 1, 1
        self._command = command

    def _toggle(self):
        if self._variable.get() == self._off_value:
            self._image = self._on_img
            self._variable.set(self._on_value)
        else:
            self._image = self._off_img
            self._variable.set(self._off_value)
        self._create_image()
        self._run()

    def grid(self, **kwargs):
        super().grid(**kwargs)
        self._show()

    def pack(self, **kwargs):
        super().pack(**kwargs)
        self._show()

    def place(self, **kwargs):
        super().place(**kwargs)
        self._show()

    def _show(self):
        self._create_image()
        self.bind('<ButtonRelease-1>', lambda event: self._toggle())
        self.bind('<Configure>', lambda event: self._resize_image(event.width, event.height))

    def _run(self):
        if self._command:
            self._command()

    def _create_image(self):
        self._width, self._height = get_widget_dimensions(self)
        self._image = resize_image(self._image, (self._width, self._height))
        self._lbl_img = PhotoImage(get_image(self._image))
        self.config(image=self._lbl_img)

    def _resize_image(self, width, height):
        if self._width != width or self._height != height:
            self._width, self._height = width, height
            self._image = resize_image(self._image, (width, height))
            self._lbl_img = PhotoImage(get_image(self._image))
            self.config(image=self._lbl_img)

    def get(self):
        return self._variable.get()

    def toggle(self):
        self._toggle()

    def select(self):
        if self._variable.get() == self._off_value:
            self._toggle()

    def deselect(self):
        if self._variable.get() == self._on_value:
            self._toggle()
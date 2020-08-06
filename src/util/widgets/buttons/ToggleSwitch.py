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
        self._on_default = ondefault

        self._off_value = offvalue
        self._on_value = onvalue
        self._variable = variable if variable else BooleanVar()
        if variable:
            value = variable.get()
        else:
            value = onvalue if ondefault else offvalue
        self._variable.set(value)
        self._command = command
        self._variable.trace_add('write', lambda *args: self._swap_image())

    def _toggle(self):
        if self._variable.get() == self._off_value:
            image = self._on_image_lbl
            self._variable.set(self._on_value)
        else:
            image = self._off_image_lbl
            self._variable.set(self._off_value)
        self.config(image=image)

    def _swap_image(self):
        if self._variable.get() == self._off_value:
            self.config(image=self._off_image_lbl)
        else:
            self.config(image=self._on_image_lbl)

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
        self.bind('<ButtonRelease-1>', lambda event: self._run())

    def _run(self):
        self._toggle()
        if self._command:
            self._command()

    def _create_image(self):
        width, height = get_widget_dimensions(self)
        self._off_image = resize_image(self._off_img, (width, height))
        self._off_image_lbl = PhotoImage(get_image(self._off_image))
        self._on_image = resize_image(self._on_img, (width, height))
        self._on_image_lbl = PhotoImage(get_image(self._on_image))
        img = self._on_image_lbl if self._on_default else self._off_image_lbl
        self.config(image=img)

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
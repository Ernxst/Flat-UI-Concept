from tkinter import Label

from PIL.ImageTk import PhotoImage

from Util.tkUtilities import get_widget_dimensions
from util.ImageUtilities import open_image, get_image, resize_image, get_image_size


class ImageLabel(Label):
    def __init__(self, master, image_location, ratio=None, bg=None):
        bg = bg if bg else master['bg']
        super().__init__(master, bg=bg, relief='flat',
                         highlightthickness=0, bd=0)
        self._original_image = open_image(image_location)
        self._image = self._original_image
        self._lbl_img = None
        self._ratio = ratio if ratio else 0.75

    def grid_forget(self):
        self.unbind('<Configure>')
        super().grid_forget()

    def grid(self, **kwargs):
        super().grid(**kwargs)
        self._create_image()
        self.bind('<Configure>', lambda event: self._resize_image(event.width, event.height))

    def _create_image(self):
        width, height = get_widget_dimensions(self)
        self._image = resize_image(self._original_image, self._get_size(width, height))
        self._lbl_img = PhotoImage(get_image(self._image))
        self.config(image=self._lbl_img)

    def _resize_image(self, width, height):
        w, h = get_image_size(self._image)
        if w != width and h != height:
            size = self._get_size(width, height)
            self._images = resize_image(self._original_image, size)
            self._lbl_img = PhotoImage(get_image(self._image))
            self.config(image=self._lbl_img)

    def _get_size(self, width, height):
        min_size, max_size = min(width, height), max(width, height)
        size = int(max_size * self._ratio)
        if size > min_size:
            size = int(max(max_size / 2, min_size) * self._ratio)
        return size, size
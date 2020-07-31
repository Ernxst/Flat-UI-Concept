from PIL.ImageTk import PhotoImage

from Util.tkUtilities import get_widget_dimensions
from src.util.ImageUtilities import open_image, get_image, resize_image
from src.util.widgets.buttons.TkButton import TkButton


class ImageButton(TkButton):
    def __init__(self, master, image_location, ratio=0.25, command=None):
        super().__init__(master, bg=master['bg'], command=command)
        self._original_image = open_image(image_location)
        self._image = self._original_image
        self._ratio = ratio

    def grid_forget(self):
        self.unbind('<Configure>')
        super().grid_forget()

    def grid(self, **kwargs):
        super().grid(**kwargs)
        self._resize_image(*get_widget_dimensions(self))
        self.bind('<Configure>', self._resize)

    def _resize(self, event):
        self._resize_image(event.width, event.height)

    def _resize_image(self, width, height):
        self._image = resize_image(self._original_image, self._get_size(width, height))
        self._lbl_img = PhotoImage(get_image(self._image))
        self.config(image=self._lbl_img)

    def _get_size(self, width, height):
        size = int(max(width, height) * self._ratio)
        return size, size
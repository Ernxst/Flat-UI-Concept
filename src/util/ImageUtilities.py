import cv2
from PIL import Image, ImageDraw

from src.util.constants import IMAGE_FOLDER


def get_icon_location(name):
    return IMAGE_FOLDER + name.lower() + '.png'


def get_image(img):
    return Image.fromarray(img)


def open_image(location):
    img = cv2.imread(location, cv2.IMREAD_UNCHANGED)
    if img is not None:
        return cv2.cvtColor(img, cv2.COLOR_BGRA2RGBA)
    return img


def save_image(location, img):
    cv2.imwrite(location, cv2.cvtColor(img, cv2.COLOR_BGRA2RGBA))


def rotate_image(img):
    return cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)


def get_image_size(img):
    if img is not None:
        return reversed(img.shape[:2])
    return -1, -1


def resize_image(img, size):
    return cv2.resize(img, size, cv2.INTER_LANCZOS4)


def get_pos(row, col, size, padding=10):
    return col * (size + padding), row * (size + padding)


def is_image(filename):
    try:
        cv2.imread(filename)
        return True
    except IOError:
        return False


def create_thumbnail(radius, image):
    width = height = (radius - 1) * 2
    image = resize_image(image, (width, height))
    mask = Image.new('L', (width, height))
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.ellipse((0, 0, width, height), fill=255)
    img = get_image(image)
    img.putalpha(mask)
    return img
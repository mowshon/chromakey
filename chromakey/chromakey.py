from PIL import Image
import numpy
import cv2
from scipy.ndimage.morphology import binary_erosion
from pymatting.alpha.estimate_alpha_cf import estimate_alpha_cf
from pymatting.foreground.estimate_foreground_ml import estimate_foreground_ml
from pymatting.util.util import stack_images


class Chromakey:

    __image = None

    __mask = None

    def __init__(self, image, color=None, hsv_color_lower=None, hsv_color_upper=None, lower_ratio=0.5, upper_ratio=0.5):
        if isinstance(image, (numpy.ndarray, numpy.generic)):
            self.__image = Image.fromarray(image)
        else:
            self.__image = Image.open(image)

        hsv_color = self.color_to_hsv(self.background_color(color))

        # Get the color range in HSV.
        color_range = self.hsv_range(hsv_color, lower_ratio, upper_ratio)
        hsv_low = hsv_color_lower if hsv_color_lower else color_range[0]
        hsv_hight = hsv_color_upper if hsv_color_upper else color_range[1]

        # Convert image to HSV.
        hsv_image = self.__image.copy()
        hsv_image = hsv_image.convert('HSV')
        hsv_array = numpy.array(hsv_image)
        hsv_image.close()

        mask = cv2.inRange(hsv_array, hsv_low, hsv_hight)
        mask = cv2.bitwise_not(mask)
        self.__mask = Image.fromarray(mask)

    def alpha_matting_cutout(
            self,
            foreground_threshold=240,
            background_threshold=10,
            erode_structure_size=10,
    ):
        base_size = (1000, 1000)
        size = self.__image.size

        self.__image.thumbnail(base_size, Image.LANCZOS)
        mask = self.__mask.resize(self.__image.size, Image.LANCZOS)

        img = numpy.asarray(self.__image)
        mask = numpy.asarray(mask)

        self.__image.close()
        self.__mask.close()

        # Guess likely foreground/background
        is_foreground = mask > foreground_threshold
        is_background = mask < background_threshold

        # Erode foreground/background
        structure = None
        if erode_structure_size > 0:
            structure = numpy.ones((erode_structure_size, erode_structure_size), dtype=numpy.int)

        is_foreground = binary_erosion(is_foreground, structure=structure)
        is_background = binary_erosion(is_background, structure=structure, border_value=1)

        trimap = numpy.full(mask.shape, dtype=numpy.uint8, fill_value=128)
        trimap[is_foreground] = 255
        trimap[is_background] = 0

        # Build the cutout image
        img_normalized = img / 255.0
        trimap_normalized = trimap / 255.0

        alpha = estimate_alpha_cf(img_normalized, trimap_normalized)
        foreground = estimate_foreground_ml(img_normalized, alpha)
        cutout = stack_images(foreground, alpha)

        cutout = numpy.clip(cutout * 255, 0, 255).astype(numpy.uint8)
        cutout = Image.fromarray(cutout)
        cutout = cutout.resize(size, Image.LANCZOS)

        return cutout

    def simple_cutout(self):
        empty = Image.new("RGBA", self.__image.size, 0)
        image = Image.composite(
            self.__image, empty, self.__mask.resize(self.__image.size, Image.LANCZOS)
        )

        self.__image.close()
        empty.close()
        self.__mask.close()

        return image

    @staticmethod
    def hsv_range(hsv_color: list, lower_ratio: float, upper_ratio: float) -> [numpy.array, numpy.array]:
        color_low = [
            hsv_color[0] - int(hsv_color[0] * lower_ratio),
            hsv_color[1] - int(hsv_color[1] * lower_ratio),
            hsv_color[2] - int(hsv_color[2] * lower_ratio),
        ]

        color_high = [
            hsv_color[0] + int(hsv_color[0] * upper_ratio),
            hsv_color[1] + int(hsv_color[1] * upper_ratio),
            hsv_color[2] + int(hsv_color[2] * upper_ratio),
        ]

        return [
            numpy.array(color_low), numpy.array(color_high)
        ]

    def background_color(self, color):
        """
        Get the color we need to be removed.

        Parameters
        ----------
        color : str, list, tuple
            1. If the color is not specified (color = None), then we take the color from the first pixel.
            2. If we got a list with two positions (color = [5, 10]), then we take the color of the pixel
            at these coordinates.
            3. Otherwise, return the color as it is. Most likely the color is given by the text or the RGB list.

        Returns
        ----------
        background_color : str, list, tuple
            The color to be removed.
        """
        if color is None:
            return self.__image.getpixel((0, 0))

        if len(color) == 2:
            return self.__image.getpixel((color[0], color[1]))

        return color

    @staticmethod
    def color_to_hsv(color):
        if type(color) is not str:
            color = tuple(color)

        temp_image = Image.new('RGB', (1, 1), color=color).convert('HSV')
        hsv_color = temp_image.getpixel((0, 0))
        temp_image.close()
        return hsv_color
from PIL import Image
from random import randint
# https://www.geeksforgeeks.org/how-to-manipulate-the-pixel-values-of-an-image-using-python/
# .exists() возвращает True если на месте пути существует файл, иначе - False !!!!!!!!!!!!!!!!!! <---------


class Filter:
    def apply_to_pixel(self, pixel: tuple) -> tuple:
        """
        param:
        pixel:
        return:
        """
        raise NotImplementedError()

    def apply_to_image(self, img: Image.Image) -> Image.Image:
        """
        Применяет фильтр к изображению.
        param:
        img: исходное изображение
        return: новое изображение
        """

        # получаем цвет pixel = img.getpixel((i, j)) как-либо меняем цвет new_pixel = self.apply_to_pixel(pixel) сохраняем пиксель обратно img.putpixel((i, j), new_pixel) return img class
        for i in range(img.width):
            for j in range(img.height):
                pixel = img.getpixel((i, j))
                new_pixel = self.apply_to_pixel(pixel)
                img.putpixel((i, j), new_pixel)
        return img


class RedFilter(Filter):
    def apply_to_pixel(self, pixel: tuple) -> tuple:
        return tuple([pixel[0], 0, 0])


class GreenFilter(Filter):
    def apply_to_pixel(self, pixel: tuple) -> tuple:
        return tuple([0, pixel[1], 0])


class BlueFilter(Filter):
    def apply_to_pixel(self, pixel: tuple) -> tuple:
        return tuple([0, 0, pixel[2]])


class BrightFilter(Filter):
    def apply_to_pixel(self, pixel: tuple):
        return tuple(min(round(i * 1.25), 255) for i in pixel)


class DarkFilter(Filter):
    def apply_to_pixel(self, pixel: tuple) -> tuple:
        return tuple(round(i * 0.7) for i in pixel)


class InversionFilter(Filter):
    def apply_to_pixel(self, pixel: tuple) -> tuple:
        return tuple((255 - i) for i in pixel)


class GreyFilter(Filter):
    def apply_to_pixel(self, pixel: tuple) -> tuple:
        return tuple(round((0.299 * pixel[0]) + (0.587 * pixel[1]) + (0.114 * pixel[2])) for i in pixel)
        # используется формула i = 0.299 * R + 0.587 * G + 0.114 * B


class JustAMess(Filter):
    def apply_to_pixel(self, pixel: tuple) -> tuple:
        return tuple([randint(0, 255), randint(0, 255), randint(0, 255)]) if pixel == tuple([0, 0, 0]) else pixel


class ChaoticFilter(Filter):
    def apply_to_image(self, img: Image.Image) -> Image.Image:
        r, g, b = randint(-100, 100), randint(-100, 100), randint(-100, 100)
        print(r, g, b)
        for i in range(img.width):
            for j in range(img.height):
                pixel = img.getpixel((i, j))
                new_pixel = tuple(pixel[i] + [r, g, b][i] if (0 <= i <= 255) else pixel[i] for i in range(3))
                img.putpixel((i, j), new_pixel)
        return img


class ShinyFilter(Filter):
    def apply_to_pixel(self, pixel: tuple, k) -> tuple:
        return tuple([min(round(i * k), 255) for i in pixel])


    def apply_to_image(self, img: Image.Image) -> Image.Image:
        count = img.size[0] * img.size[1]
        summ = sum([sum([sum(img.getpixel((i, j))) for j in range(img.height)]) for i in range(img.width)])
        mid = summ // count
        for i in range(img.width):
            for j in range(img.height):
                pixel = img.getpixel((i, j))
                k = mid / sum(pixel) if sum(pixel) < mid and sum(pixel) != 0 else False
                if k:
                    new_pixel = self.apply_to_pixel(pixel, k)
                    img.putpixel((i, j), new_pixel)
        return img


FILTERS = {
    1: {
        'name': 'Red filter',
        'description': 'Данный фильтр отображает только красный спектр на картинке',
        'class': RedFilter
    },
    2: {
        'name': 'Green filter',
        'description': 'Данный фильтр отображает только зелёный спектр на картинке',
        'class': GreenFilter
    },
    3: {
        'name': 'Blue filter',
        'description': 'Данный фильтр отображает только синий спектр на картинке',
        'class': BlueFilter
    },
    4: {
        'name': 'Bright filter',
        'description': 'Фильтр увеличивает яркость изображения',
        'class': BrightFilter
    },
    5: {
        'name': 'Dark filter',
        'description': 'Фильтр уменьшает яркость изображения',
        'class': DarkFilter
    },
    6: {
        'name': 'Inversion filter',
        'description': 'Фильтр возвращает изображение с инвертированными (противоположными) цветами',
        'class': InversionFilter
    },
    7: {
        'name': 'Grey filter',
        'description': 'Фильтр возвращает изображение в серых тонах',
        'class': GreyFilter
    },
    8: {
        'name': 'Just A Mess',
        'description': 'Фильтр превращает все черные пиксели изображения в случайные\n'
                       '(применимо для черного фона - он станет гораздо ярче)',
        'class': JustAMess
    },
    9: {
        'name': 'Chaotic filter',
        'description': 'Фильтр, который случайным образом преобразует цветовую гамму изображения',
        'class': ChaoticFilter
    },
    10: {
        'name': 'Shiny filter',
        'description': 'Этот фильтр подсвечивает все тусклые оттенки на картинке',
        'class': ShinyFilter
    },
}


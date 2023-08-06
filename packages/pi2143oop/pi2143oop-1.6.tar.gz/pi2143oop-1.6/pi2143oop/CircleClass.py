from math import pi

from .ErrorClass import Error
from .DotClass import Dot
from .TriangleClass import Triangle
from .Settings import check_input


class Circle(Dot):
    'Класс круга'

    def __init__(self, canvas, x: int = 0, y: int = 0, r: int = 0):
        self.cnv = canvas
        self.Board = [self.cnv.default_symbol] * self.cnv.size * self.cnv.size

        self.__x, self.__y, self.__r = self._check_circle(x, y, r)

    def _check_circle(self, *args):
        x, y, r = args

        check_input([x], self.cnv.size)
        check_input([y], self.cnv.size)
        check_input([r], self.cnv.size)

        if x + r >= self.cnv.size or x + r < 0 or y + r >= self.cnv.size or y - r < 0:
            raise Error('Фигура выходит за пределы поля')

        if r == 0:
            raise Error('Радиус должен быть больше 0')

        return [x], [y], r

    def _get_value_y(self, x: int):
        return (self.__r ** 2 - (x - self.__x[0]) ** 2) ** 0.5

    def _get_value_x(self, y: int):
        return (self.__r ** 2 - (y - self.__y[0]) ** 2) ** 0.5

    def _set_line_y(self, x: list):
        dots = []

        for i in range(min(x[0], x[1]), max(x[0], x[1]) + 1):
            if 0 <= i <= self.cnv.size:
                k = self._get_value_y(i) + self.__y[0]

                if 0 <= int(k) <= self.cnv.size:
                    if int(k) == float(k):
                        dots.append(i)
                        dots.append(int(k))
                    else:
                        a = k - int(k)

                        if a >= 0.4:
                            if 0 <= int(k + 1) <= self.cnv.size:
                                dots.append(i)
                                dots.append(int(k + 1))
                        if a <= 0.6:
                            if 0 <= int(k) <= self.cnv.size:
                                dots.append(i)
                                dots.append(int(k))

        for i in range(min(x[0], x[1]), max(x[0], x[1]) + 1):
            if 0 <= i <= self.cnv.size:
                k = -self._get_value_y(i) + self.__y[0]

                if 0 <= int(k) <= self.cnv.size:
                    if int(k) == float(k):
                        dots.append(i)
                        dots.append(int(k))
                    else:
                        a = k - int(k)

                        if a >= 0.4:
                            if 0 <= int(k + 1) <= self.cnv.size:
                                dots.append(i)
                                dots.append(int(k + 1))
                        if a <= 0.6:
                            if 0 <= int(k) <= self.cnv.size:
                                dots.append(i)
                                dots.append(int(k))

        return dots

    def _set_line_x(self, y: list):
        dots = []

        for i in range(min(y[0], y[1]), max(y[0], y[1]) + 1):
            if 0 <= i <= self.cnv.size:
                k = self._get_value_x(i) + self.__x[0]

                if 0 <= int(k) <= self.cnv.size:
                    if int(k) == float(k):
                        dots.append(int(k))
                        dots.append(i)
                    else:
                        a = k - int(k)

                        if a >= 0.4:
                            if 0 <= int(k + 1) <= self.cnv.size:
                                dots.append(int(k + 1))
                                dots.append(i)
                        if a <= 0.6:
                            if 0 <= int(k) <= self.cnv.size:
                                dots.append(int(k))
                                dots.append(i)

        for i in range(min(y[0], y[1]), max(y[0], y[1]) + 1):
            if 0 <= i <= self.cnv.size:
                k = -self._get_value_x(i) + self.__x[0]

                if 0 <= int(k) <= self.cnv.size:
                    if int(k) == float(k):
                        dots.append(int(k))
                        dots.append(i)
                    else:
                        a = k - int(k)

                        if a >= 0.4:
                            if 0 <= int(k + 1) <= self.cnv.size:
                                dots.append(int(k + 1))
                                dots.append(i)
                        if a <= 0.6:
                            if 0 <= int(k) <= self.cnv.size:
                                dots.append(int(k))
                                dots.append(i)

        return dots

    def _set_dots(self, x: list, y: list):
        dots = []

        x = [x[0] - self.__r, x[0] + self.__r]
        dots.extend(self._set_line_y(x))
        y = [y[0] - self.__r, y[0] + self.__r]
        dots.extend(self._set_line_x(y))

        return dots

    def fill(self, symbol: str = '', *args):
        if symbol == '':
            symbol = self.cnv.default_symbol

        x, y = self._check_values(*args)

        symbol2 = self.get_dot(x[0] - self.__r, y[0])

        dots = self._set_fill_dots(x, y)
        self.draw_dot(symbol[0], *dots)

        dots = self._set_dots(x, y)
        self.draw_dot(symbol2, *dots)

    def cut_piece(self, symbol: str = '', x1: int = 0, y1: int = 0, x2: int = 0, y2: int = 0):
        'Функция вырезания сектора круга'

        if symbol == '':
            symbol = self.cnv.default_symbol

        t = Triangle(x1, y1, x2, y2, self.__x[0], self.__y[0])

        dots = t._set_dots(t.x, t.y)
        dots.extend(t._set_fill_dots(t.x, t.y))

        self.draw_dot(symbol[0], *dots)

    def draw_c(self, symbol: str = ''):
        if symbol == '':
            symbol = self.cnv.default_symbol

        dots = []
        for y in range(self.cnv.size):
            k = self.Board[y * self.cnv.size: (y + 1) * self.cnv.size]
            if symbol[0] in k:
                for x in range(len(k)):
                    if k[x] == symbol[0]:
                        dots.append(x)
                        dots.append(y)

        self.cnv.canvas.draw_dot(symbol[0], *dots)

    @property
    def x(self):
        'Свойство: координата(ы) x'

        return self.__x

    @property
    def y(self):
        'Свойство: координата(ы) y'

        return self.__y

    @property
    def r(self):
        'Свойство: радиус'

        return self.__r

    @property
    def xyr(self):
        'Свойство: не используется'

        return True

    @xyr.setter
    def xyr(self, *args):
        'Свойство: смена точек и радиуса'

        self.__x, self.__y, self.__r = self._check_circle(*args[0])

    @property
    def square(self):
        'Свойство: площадь фигуры'

        s = pi * self.__r ** 2

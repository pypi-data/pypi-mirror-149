from .DotClass import Dot


class Rectangle(Dot):
    'Класс прямоугольника'

    def __init__(self, canvas, x1: int = 0, y1: int = 0, x2: int = 0, y2: int = 0):
        self.cnv = canvas
        self.Board = [self.cnv.default_symbol] * self.cnv.size * self.cnv.size

        self.__x, self.__y = self._check_values(x1, y1, x2, y2)

    def _set_dots(self, x: list, y: list):
        dots = []

        for i in range(min(x[0], x[1]), max(x[0], x[1]) + 1):
            dots.append(i)
            dots.append(y[0])
            dots.append(i)
            dots.append(y[1])
        for i in range(min(y[0], y[1]) + 1, max(y[0], y[1])):
            dots.append(x[0])
            dots.append(i)
            dots.append(x[1])
            dots.append(i)

        return dots

    @property
    def x(self):
        'Свойство: координата(ы) x'

        return self.__x

    @property
    def y(self):
        'Свойство: координата(ы) y'

        return self.__y

    @property
    def xy(self):
        'Свойство: не используется'

        return True

    @xy.setter
    def xy(self, *args):
        'Свойство: смена точек'

        self.__x, self.__y = self._check_values(*args[0])

    @property
    def square(self):
        'Свойство: площадь фигуры'

        s = abs(self.__x[0] - self.__y[1]) * abs(self.__x[1] - self.__y[0])

        return s

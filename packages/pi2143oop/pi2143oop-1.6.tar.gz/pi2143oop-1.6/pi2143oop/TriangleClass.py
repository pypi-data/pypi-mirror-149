from .ErrorClass import Error
from .DotClass import Dot
from .LineClass import Line


class Triangle(Dot):
    'Класс треугольника'

    def __init__(self, canvas, x1: int = 0, y1: int = 0, x2: int = 0, y2: int = 0, x3: int = 0, y3: int = 0):
        self.cnv = canvas
        self.Board = [self.cnv.default_symbol] * self.cnv.size * self.cnv.size

        self.__x, self.__y = self._check_values(x1, y1, x2, y2, x3, y3)

        self.a = ((self.__x[0] - self.__x[1]) ** 2 + (self.__y[0] - self.__y[1]) ** 2) ** 0.5
        self.b = ((self.__x[0] - self.__x[2]) ** 2 + (self.__y[0] - self.__y[2]) ** 2) ** 0.5
        self.c = ((self.__x[1] - self.__x[2]) ** 2 + (self.__y[1] - self.__y[2]) ** 2) ** 0.5

        self._check_triangle()

    def _check_triangle(self):
        if not (self.a + self.b > self.c and self.a + self.c > self.b and self.b + self.c > self.a):
            raise Error('Невозможно построить такой треугольник')

    def _set_dots(self, x: list, y: list):
        dots = []

        l1 = Line(self.cnv, x[0], y[0], x[1], y[1])
        l2 = Line(self.cnv, x[0], y[0], x[2], y[2])
        l3 = Line(self.cnv, x[1], y[1], x[2], y[2])
        l = [l1, l2, l3]

        for i in l:
            dots.extend(i._set_dots())

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

        p = (self.a + self.b + self.c) / 2

        s = (p * (p - self.a) * (p - self.b) * (p - self.c)) ** 0.5

        return s

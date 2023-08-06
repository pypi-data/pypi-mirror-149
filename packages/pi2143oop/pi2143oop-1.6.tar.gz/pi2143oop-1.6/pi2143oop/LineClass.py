from .ErrorClass import Error
from .Settings import check_input, to_print


class Line():
    'Класс линии'

    def __init__(self, canvas, x1: int = 0, y1: int = 0, x2: int = 0, y2: int = 0):
        self.cnv = canvas
        self.Board = [self.cnv.default_symbol] * self.cnv.size * self.cnv.size

        self.__x, self.__y = self._check_values(x1, y1, x2, y2)

    def _check_values(self, *args):
        x = list(args)[::2]
        y = list(args)[1::2]

        if len(x) != len(y):
            raise Error('У точки не хватает аргумента x или y')

        check_input(x, self.cnv.size)
        check_input(y, self.cnv.size)

        return x, y

    def _get_value_y(self, x: int):
        return ((x - self.__x[0]) * (self.__y[1] - self.__y[0])) / (self.__x[1] - self.__x[0]) + self.__y[0]

    def _get_value_x(self, y: int):
        return ((y - self.__y[0]) * (self.__x[1] - self.__x[0])) / (self.__y[1] - self.__y[0]) + self.__x[0]

    def _set_line_y(self, x: list):
        dots = []

        for i in range(min(x[0], x[1]), max(x[0], x[1]) + 1):
            if 0 <= i <= self.cnv.size:
                k = self._get_value_y(i)

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
                k = self._get_value_x(i)

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

    def _set_dots(self):
        dots = []

        if abs(self.__y[0] - self.__y[1]) == abs(self.__x[0] - self.__x[1]):
            k = 0
            for i in range(min(self.__x[0], self.__x[1]), max(self.__x[0], self.__x[1]) + 1):
                dots.append(i)
                if self.__y[0] < self.__y[1]:
                    if self.__x[0] < self.__x[1]:
                        dots.append(self.__y[0] + k)
                    else:
                        dots.append(self.__y[1] - k)
                else:
                    if self.__x[0] < self.__x[1]:
                        dots.append(self.__y[0] - k)
                    else:
                        dots.append(self.__y[1] + k)
                k += 1
            print()
        elif self.__x[0] == self.__x[1]:
            for i in range(min(self.__y[0], self.__y[1]), max(self.__y[0], self.__y[1]) + 1):
                dots.append(self.__x[0])
                dots.append(i)
        elif self.__y[0] == self.__y[1]:
            for i in range(min(self.__x[0], self.__x[1]), max(self.__x[0], self.__x[1]) + 1):
                dots.append(i)
                dots.append(self.__y[0])
        else:
            x = [self.__x[0], self.__x[1]]
            dots.extend(self._set_line_y(x))
            y = [self.__y[0], self.__y[1]]
            dots.extend(self._set_line_x(y))

        return dots

    def draw(self, symbol: str = ''):
        'Функция рисования фигуры на локальном экране. \
                Если нужна обычная функция рисования точек, используйте функцию "draw_dot"'

        if symbol == '':
            symbol = self.cnv.default_symbol

        dots = self._set_dots()

        for i in range(1, len(dots), 2):
            self.Board[dots[i - 1] + dots[i] * self.cnv.size] = symbol[0]

    def draw_c(self, symbol: str = ''):
        'Функция рисования фигуры на общем экране'

        if symbol == '':
            symbol = self.cnv.default_symbol

        dots = self._set_dots()

        self.cnv.draw_dot(symbol[0], *dots)

    def print(self):
        'Функция вывода локального экрана в консоль'

        a = list(range(self.cnv.size))

        print('    ', end='')
        for i in a:
            print(' ' * (2 - len(str(i))) + str(i), end=' ')
        print('\n')

        for i in range(self.cnv.size):
            print(' ' * (2 - len(str(i))) + str(i) + '  ',
                  '  '.join(self.Board[i * self.cnv.size: (i + 1) * self.cnv.size]))

    def print_c(self, symbol: str = ''):
        'Функция цветного вывода локального экрана в консоль'

        if symbol == '':
            symbol = self.cnv.default_symbol

        to_print(self.Board, symbol[0])

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

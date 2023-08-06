from .ErrorClass import Error
from .Settings import check_input, to_print


class Dot():
    'Класс точки'

    def __init__(self, canvas, x: int = 0, y: int = 0):
        self.cnv = canvas
        self.Board = [self.cnv.default_symbol] * self.cnv.size * self.cnv.size

        self.__x, self.__y = self._check_values(x, y)

    def _check_values(self, *args):
        x = [0]
        y = [0]

        if len(args) == 0:
            try:
                x = self.x
                y = self.y
            except:
                raise Error('У фигуры нет собственных точек. Укажите входные данные')
        else:
            x = list(args)[::2]
            y = list(args)[1::2]

            if len(x) != len(y):
                raise Error('У точки не хватает аргумента x или y')

            check_input(x, self.cnv.size)
            check_input(y, self.cnv.size)

        return x, y

    def _set_dots(self, x: list, y: list):
        dots = []
        for i in range(len(x)):
            dots.append(x[i])
            dots.append(y[i])

        return dots

    def _set_fill_dots(self, x: list, y: list):
        dots = self._set_dots(x, y)
        x = []
        y = []
        for i in range(0, len(dots), 2):
            x.append(dots[i])
            y.append(dots[i + 1])

        dots = []

        for i in range(len(y)):
            for j in range(len(y)):
                if y[i] == y[j]:
                    for k in range(min(x[i], x[j]) + 1, max(x[i], x[j])):
                        dots.append(k)
                        dots.append(y[i])

        return dots

    def draw(self, symbol: str = '', *args):
        'Функция рисования фигуры на локальном экране. \
                Если нужна обычная функция рисования точек, используйте функцию "draw_dot"'

        if symbol == '':
            symbol = self.cnv.default_symbol

        x, y = self._check_values(*args)

        dots = self._set_dots(x, y)

        for i in range(1, len(dots), 2):
            self.Board[dots[i - 1] + dots[i] * self.cnv.size] = symbol[0]

    def draw_dot(self, symbol: str = '', *args):
        'Функция рисования точки(ек) на локальном экране'

        if symbol == '':
            symbol = self.cnv.default_symbol

        x, y = self._check_values(*args)

        for i in range(len(x)):
            self.Board[x[i] + y[i] * self.cnv.size] = symbol[0]

    def fill(self, symbol: str = '', *args):
        'Функция заливки фигуры. Работает для всех классов, кроме точки и линии'

        if symbol == '':
            symbol = self.cnv.default_symbol

        x, y = self._check_values(*args)

        symbol2 = self.get_dot(x[0], y[0])

        dots = self._set_fill_dots(x, y)
        self.draw_dot(symbol[0], *dots)

        dots = self._set_dots(x, y)
        self.draw_dot(symbol2, *dots)

    def get_dot(self, x: int = 0, y: int = 0):
        'Функция получения значения в точке'

        return self.Board[x + y * self.cnv.size]

    def draw_c(self, symbol: str = ''):
        'Функция рисования фигуры на общем экране'

        if symbol == '':
            symbol = self.cnv.default_symbol

        dots = self._set_dots(self.x, self.y)

        self.cnv.draw_dot(symbol[0], *dots)

    def fill_c(self, symbol: str = ''):
        'Функция заполнения фигуры на общем экране'

        if symbol == '':
            symbol = self.cnv.default_symbol

        dots = self._set_fill_dots(self.x, self.y)

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

    @property
    def square(self):
        'Свойство: площадь фигуры'

        return 0

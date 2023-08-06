from .ErrorClass import Error
from .Settings import check_input, to_print


class Canvas:
    'Класс для рисования фигур на общем экране'

    def __init__(self, default_symbol: str = '-', size: int = 40):
        self.size = size
        self.default_symbol = default_symbol
        self.Board = [default_symbol] * size * size

    def _check_values(self, *args):

        x, y = [], []

        if len(args) == 0:
            raise Error('У фигуры нет собственных точек')
        else:
            x = list(args)[::2]
            y = list(args)[1::2]

            if len(x) != len(y):
                raise Error('У точки не хватает аргумента x или y')

            check_input(x, self.size)
            check_input(y, self.size)

        return x, y

    def draw_dot(self, symbol: str = '', *args):
        'Функция рисования в точке(ах) на общем экране'

        if symbol == '':
            symbol = self.default_symbol

        x, y = self._check_values(*args)

        for i in range(len(x)):
            self.Board[x[i] + y[i] * self.size] = symbol[0]

    def fill(self, symbol: str = ''):
        'Функция заполнения общего экрана символами'

        if symbol == '':
            symbol = self.default_symbol

        self.Board = [symbol[0]] * self.size * self.size

    def get_dot(self, x: int = 0, y: int = 0):
        'Функция получения значения в точке'

        return self.Board[x + y * self.size]

    def print(self):
        'Функция вывода общего экрана в консоль'

        a = list(range(self.size))

        print('    ', end='')
        for i in a:
            print(' ' * (2 - len(str(i))) + str(i), end=' ')
        print('\n')

        for i in range(self.size):
            print(' ' * (2 - len(str(i))) + str(i) + '  ', '  '.join(self.Board[i * self.size: (i + 1) * self.size]))

    def print_c(self, symbol: str = ''):
        'Функция цветного вывода общего экрана в консоль'

        if symbol == '':
            symbol = self.default_symbol

        to_print(self.Board, symbol[0])

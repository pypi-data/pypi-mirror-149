from .ErrorClass import Error


default_font_color = 37
default_background_color = 40
font_color = 31
background_color = 40


def to_print(board: list, symbol: str):
    'Функция цветного вывода на экран'

    size = int(len(board) ** 0.5)

    a = list(range(size))

    print('\033[{1}m\033[{0}m    '.format(default_font_color, default_background_color), end='')
    for i in a:
        print('\033[{1}m\033[{0}m '.format(default_font_color, default_background_color) *
              (2 - len(str(i))) + str(i), end=' ')
    print('\n')

    for i in range(size):
        print('\033[{0}m\033[{1}m '.format(default_font_color, default_background_color) * (2 - len(str(i))) + str(i),
              end='   ')

        k = board[i * size: (i + 1) * size]

        for j in k:
            if j == symbol[0]:
                print('\033[{1}m\033[{0}m{2}  '.format(default_font_color, default_background_color, j),
                      end='')
            else:
                print('\033[{1}m\033[{0}m{2}  '.format(font_color, background_color, j), end='')

        print()


def check_input(x: list, size: int):
    'Функция проверки введенных значений'

    s = 'На вход подаются числа от (0) до (размер поля - 1)'

    for i in x:
        if not isinstance(i, int):
            raise Error(s)
        elif i >= size or i < 0:
            raise Error(s)

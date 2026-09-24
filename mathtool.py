"""
mathtool.py — решение уравнений вида A*x^2 + B*x + C = 0.

Использование:
    python mathtool.py                          вывод справки
    python mathtool.py --help                   вывод справки
    python mathtool.py solve                    ввод коэффициентов с клавиатуры
    python mathtool.py solve -a 1 -b -3 -c 2     решение с заданными коэффициентами
"""

import sys
import math

# Предельное по модулю значение коэффициента
MAX_VALUE = 10000

HELP_TEXT = (
    "mathtool — решение уравнений вида A*x^2 + B*x + C = 0\n"
    "\n"
    "Использование:\n"
    "    python mathtool.py                          вывод справки\n"
    "    python mathtool.py --help                    вывод справки\n"
    "    python mathtool.py solve                     ввод коэффициентов с клавиатуры\n"
    "    python mathtool.py solve -a 1 -b -3 -c 2      решение с заданными коэффициентами\n"
    "\n"
    "Коэффициенты A, B, C — целые числа, по модулю не превышающие 10000."
)


def print_error(message):
    """Вывод сообщения об ошибке в поток ошибок."""
    print(message, file=sys.stderr)


def read_coefficients_from_keyboard():
    """Запрашивает коэффициенты A, B, C у пользователя с клавиатуры.
    Возвращает кортеж строк (a_str, b_str, c_str)."""
    a_str = input("Введите A: ")
    b_str = input("Введите B: ")
    c_str = input("Введите C: ")
    return a_str, b_str, c_str


def parse_arguments(argv):
    """Разбор параметров командной строки.
    Возвращает кортеж строк (a_str, b_str, c_str) с исходными данными,
    либо завершает работу приложения при ошибке / запросе справки."""

    # Параметров нет или запрошена справка
    if len(argv) == 0 or argv[0] == "--help":
        print(HELP_TEXT)
        sys.exit(0)

    # Первая команда должна быть "solve"
    if argv[0] != "solve":
        print_error(f"ОШИБКА: неизвестная команда \"{argv[0]}\"")
        sys.exit(1)

    # Только "solve" — коэффициенты вводятся с клавиатуры
    if len(argv) == 1:
        return read_coefficients_from_keyboard()

    # "solve -a .. -b .. -c .." — коэффициенты заданы параметрами
    if len(argv) == 7:
        if argv[1] != "-a" or argv[3] != "-b" or argv[5] != "-c":
            print_error("ОШИБКА: неизвестный параметр")
            sys.exit(1)
        return argv[2], argv[4], argv[6]

    # Любой другой набор параметров считается неверным
    print_error("ОШИБКА: неверный набор параметров")
    sys.exit(1)


def convert_to_int(a_str, b_str, c_str):
    """Преобразование строковых коэффициентов в целые числа.
    При ошибке преобразования завершает работу приложения с кодом 1."""
    try:
        a = int(a_str)
        b = int(b_str)
        c = int(c_str)
    except ValueError:
        print_error("ОШИБКА: коэффициент не является целым числом")
        sys.exit(1)
    return a, b, c


def validate_range(a, b, c):
    """Проверка коэффициентов на соответствие допустимому диапазону.
    При выходе за диапазон завершает работу приложения с кодом 1."""
    if abs(a) > MAX_VALUE or abs(b) > MAX_VALUE or abs(c) > MAX_VALUE:
        print_error("ОШИБКА: значение вне допустимого диапазона")
        sys.exit(1)


def solve_linear(b, c):
    """Решение уравнения B*x + C = 0."""
    if b != 0:
        print("Уравнение линейное")
        x = -c / b
        print(f"x = {x:.3f}")
    else:
        # B = 0: неизвестное отсутствует, записью уравнения это не является
        print_error("ОШИБКА: это не уравнение, неизвестное отсутствует")
        sys.exit(1)


def solve_quadratic(a, b, c):
    """Решение уравнения A*x^2 + B*x + C = 0 при A != 0."""
    print("Уравнение квадратное")

    d = b * b - 4 * a * c
    print(f"D = {d}")

    if d > 0:
        x1 = (-b + math.sqrt(d)) / (2 * a)
        x2 = (-b - math.sqrt(d)) / (2 * a)
        print(f"x1 = {x1:.3f}")
        print(f"x2 = {x2:.3f}")
    elif d == 0:
        x = -b / (2 * a)
        print(f"x = {x:.3f}")
    else:
        print("Действительных корней нет")


def main():
    # 1. Разбор параметров командной строки, получение исходных данных
    a_str, b_str, c_str = parse_arguments(sys.argv[1:])

    # 2. Преобразование исходных данных в целые числа
    a, b, c = convert_to_int(a_str, b_str, c_str)

    # 3. Проверка значений на соответствие ограничениям
    validate_range(a, b, c)

    # 4. Решение уравнения и вывод результата
    if a == 0:
        solve_linear(b, c)
    else:
        solve_quadratic(a, b, c)

    sys.exit(0)


if __name__ == "__main__":
    main()

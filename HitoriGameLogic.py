from collections import defaultdict
from copy import deepcopy
from enum import Enum
from typing import List


class SquareState(Enum):
    ERASED = "-"
    UNSOLVED = " "
    KEPT = "+"
    INVALID = "!"

    """Выводит состояние клетки"""

    def __str__(self):
        return self.value


class HitoriSquare:
    def __init__(self, digit):
        self.digit = digit
        self.state = SquareState.UNSOLVED

    """Выводит ячейку в виде строки и ее состояние"""

    def __str__(self):
        return f"{self.digit}{self.state} "

    """Метод устанавливает состояние"""

    def set_state(self, state):
        if self.state != SquareState.UNSOLVED and self.state != state:
            self.state = SquareState.INVALID
        else:
            self.state = state


class HitoriBoard:
    def __init__(self, sizeA, sizeB, digits, checker):
        self.unsolvable = False
        self.undetermined = False
        self.checker = checker
        self._init_squares(sizeA, sizeB, digits)
        self._init_solution_steps()

    def _init_squares(self, sizeA, sizeB, digits):
        self.squares = []
        for row in range(sizeA):
            self.squares.append([])
            for col in range(sizeB):
                self.squares[row].append(HitoriSquare(digits[row * sizeB + col]))

    def _init_solution_steps(self):
        self.current_step = 0
        self.solution_steps = [
            self.apply_basic_search,
            self.apply_advanced_search,
            self.check_validity,
            self.apply_local_search,
        ]

    """Выводит доску в таблице с +, - и пробелами"""

    def __str__(self):
        res = ""
        for row in range(len(self)):
            for col in range(len(self[0])):
                res += str(self.squares[row][col])
            res += "\n"
        return res

    """Выводит высоту доски"""

    def __len__(self):
        return len(self.squares)

    """Выводит ширину доски"""

    def __getitem__(self, index: int) -> List[HitoriSquare]:
        return self.squares[index]

    """
    Решает сначала базовым поиском, затем продвинутым, если есть ошибки, то решения нет.
    После чего запускается локальный поиск
    """

    def solve(self):
        while self.current_step < len(self.solution_steps) and not self.unsolvable:
            self.solution_steps[self.current_step]()
            self.current_step += 1



    @staticmethod
    def apply_basic_search():
        pass

    @staticmethod
    def apply_advanced_search():
        pass

    def check_validity(self):
        if not self.checker.is_valid(self):  # Головоломка не решается, если есть ошибки
            self.unsolvable = True

    @staticmethod
    def apply_local_search():
        pass

    """Отдает нужный столбец"""

    def get_column(self, index):
        return [row[index] for row in self]

    """Проверяет, находится ли данная клетка в пределах доски"""

    def is_in_bounds(self, row, col):
        return 0 <= row < len(self) and 0 <= col < len(self[0])

    """Хранит секрет, случилась ли где ошибка или нет"""

    def has_invalid_squares(self):
        for row in self:
            for square in row:
                if square.state == SquareState.INVALID:
                    return True
        return False

    """
    Проверяет решенность.
    Если остались прозрачные клетки, то головоломка не решена
    """

    def is_solved(self):
        for row in self:
            for square in row:
                if square.state == SquareState.UNSOLVED:
                    return False
        return True

    """Методы сравнения, сравнивают доски по значению и состоянию каждой клетки"""

    def __eq__(self, other):
        if len(self[0]) != len(other[0]) or len(self) != len(other):
            return False
        for i in range(len(self)):
            for j in range(len(self[0])):
                if self[i][j].digit == other[i][j].digit and self[i][j].state == other[i][j].state:
                    continue
                else:
                    return False
        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    """Копирует доску по каждой ее клеточке и затем устанавливает состояние соответственно оригинальной доске"""

    def __copy__(self):
        list_for_copy = []
        for i in range(len(self)):
            for j in range(len(self[0])):
                list_for_copy.append(self[i][j].digit)
        copy = HitoriBoard(len(self), len(self[0]), list_for_copy, self.checker)
        for i in range(len(self)):
            for j in range(len(self[0])):
                copy[i][j].set_state(self[i][j].state)
        return copy


class HitoriBasicSearch:
    @staticmethod
    def apply(board):
        HitoriBasicSearch._apply_to_corners(board)
        HitoriBasicSearch._apply_to_rows(board)
        HitoriBasicSearch._apply_to_cols(board)

    """Применяет базовый поиск к угловым клеткам (a и d из файла)"""

    @staticmethod
    def _apply_to_corners(board):
        if board.__lenA__() == 1 or board.__lenB__() == 1:
            return
        for i in range(-1, 1):
            for j in range(-1, 1):
                corner = board[i][j]
                diagonal = board[1 + 3 * i][1 + 3 * j]
                adjacent_1 = board[i][1 + 3 * j]
                adjacent_2 = board[1 + 3 * i][j]
                HitoriBasicSearch._apply_figure_a(corner, adjacent_1, adjacent_2)
                HitoriBasicSearch._apply_figure_a(diagonal, adjacent_1, adjacent_2)
                HitoriBasicSearch._apply_figure_d(corner, adjacent_1, adjacent_2)

    """Применяет базовый поиск к строкам (b и c из файла)"""

    @staticmethod
    def _apply_to_rows(board):
        for row in board:
            HitoriBasicSearch._apply_figure_b(row)
            for square in range(len(row)):
                HitoriBasicSearch._apply_figure_c(row, square)

    """Применяет базовый поиск к столбцам (b и c из файла)"""

    @staticmethod
    def _apply_to_cols(board):
        for i in range(board.__lenB__()):
            col = board.get_column(i)
            HitoriBasicSearch._apply_figure_b(col)
            for square in range(board.__lenA__()):
                HitoriBasicSearch._apply_figure_c(col, square)

    """Применяет фигуру а из файла"""

    @staticmethod
    def _apply_figure_a(central, adjacent_1, adjacent_2):
        if central.digit == adjacent_1.digit:
            adjacent_2.set_state(SquareState.KEPT)
        elif central.digit == adjacent_2.digit:
            adjacent_1.set_state(SquareState.KEPT)

    """Применяет фигуру b из файла"""

    @staticmethod
    def _apply_figure_b(row: List[HitoriSquare]):
        paired_digits = HitoriBasicSearch._find_pairs(row)
        HitoriBasicSearch._erase_unpaired_in_row(row, paired_digits)

    """Применяет фигуру c из файла"""

    @staticmethod
    def _apply_figure_c(row, index):
        if index >= 2 and row[index].digit == row[index - 2].digit:
            row[index - 1].set_state(SquareState.KEPT)

    """Применяет фигуру d из файла"""

    @staticmethod
    def _apply_figure_d(central, adjacent_1, adjacent_2):
        if adjacent_1.digit == adjacent_2.digit == central.digit:
            central.set_state(SquareState.ERASED)

    """Находит пары одинаковых цифр в строке и возвращает их в виде списка пар"""

    @staticmethod
    def _find_pairs(row):
        paired_digits = set()
        for i in range(1, len(row)):
            if row[i].digit == row[i - 1].digit:
                paired_digits.add(row[i].digit)
        return paired_digits

    """Удаляет из строки все элементы, не входящие в пары одинаковых и стоящих рядом для всех строк"""

    @staticmethod
    def _erase_unpaired_in_row(row: List[HitoriSquare], digits):
        for i in range(len(row)):
            if row[i].digit in digits:
                HitoriBasicSearch._erase_unpaired_digit(row, i)

    """Удаляет из строки все элементы, не входящие в пары одинаковых и стоящих рядом"""

    @staticmethod
    def _erase_unpaired_digit(row, index):
        if HitoriBasicSearch._should_erase_digit(row, index):
            row[index].set_state(SquareState.ERASED)

    """Проверяет, есть ли под боком у цифры еще одна такая же"""

    @staticmethod
    def _should_erase_digit(row, index):
        return (index < 1 or row[index].digit != row[index - 1].digit) \
            and (index >= len(row) - 1 or row[index].digit != row[index + 1].digit)

    @staticmethod
    def place_unique_diagonals(self):
        for i in range(self.size - 1):
            for j in range(self.size - 1):
                if self[i, j].digit == self[i + 1, j + 1].digit:
                    self[i, j].state = SquareState.INVALID
                    self[i + 1, j + 1].state = SquareState.INVALID


class HitoriAdvancedSearch:
    @staticmethod
    def apply(board):
        HitoriAdvancedSearch._apply_to_each_square(board)
        HitoriAdvancedSearch._apply_enumeration(board)

    """Буквально цикл смерти, делает продвинутый поиск, пока доска не перестанет меняться"""

    @staticmethod
    def board_stable(board):
        while True:
            copy_board_2 = board.__copy__()
            HitoriAdvancedSearch.apply(board)
            if board == copy_board_2:
                return board

    """Применяет продвинутый поиск к каждой клетке (фигуры e и f из файла)"""

    @staticmethod
    def _apply_to_each_square(board):
        for row in range(board.__lenA__()):
            for col in range(board.__lenB__()):
                HitoriAdvancedSearch._apply_figure_e(board, row, col)
                HitoriAdvancedSearch._apply_figure_f(board, row, col)

    """Перебирает строки и столбцы для фигур g и h"""

    @staticmethod
    def _apply_enumeration(board):
        for row in range(board.__lenA__()):
            for col in range(board.__lenB__()):
                HitoriAdvancedSearch._apply_figure_g(board, row, col)
                HitoriAdvancedSearch._apply_figure_h(board, row, col)

    """Применяет фигуру e из файла"""

    @staticmethod
    def _apply_figure_e(board, row, col):
        if board[row][col].state == SquareState.ERASED:
            for square in HitoriAdvancedSearch._get_neighbours(board, row, col):
                square.set_state(SquareState.KEPT)

    """Применяет фигуру f из файла"""

    @staticmethod
    def _apply_figure_f(board, row, col):
        d = HitoriAdvancedSearch._get_neighbours_by_state(board, row, col)
        if len(d[SquareState.ERASED]) == len(HitoriAdvancedSearch._get_neighbours(board, row, col)) - 1 \
                and len(d[SquareState.UNSOLVED]) > 0:
            d[SquareState.UNSOLVED][0].set_state(SquareState.KEPT)

    """Применяет фигуру g из файла"""

    @staticmethod
    def _apply_figure_g(board, row, col):
        have_not_copy_in_rows = True
        have_not_copy_in_cols = True
        if board[row][col].state != SquareState.ERASED:
            for row_i in range(0, board.__lenA__()):
                if board[row_i][col].digit == board[row][col].digit and row_i != row:
                    if board[row_i][col].state != SquareState.ERASED:
                        have_not_copy_in_rows = False
            for col_i in range(0, board.__lenB__()):
                if board[row][col_i].digit == board[row][col].digit and col_i != col:
                    if board[row][col_i].state != SquareState.ERASED:
                        have_not_copy_in_cols = False

            if have_not_copy_in_rows and have_not_copy_in_cols:
                board[row][col].set_state(SquareState.KEPT)

    """Применяет фигуру h из файла"""

    @staticmethod
    def _apply_figure_h(board, row, col):
        if board[row][col].state == SquareState.KEPT:
            for i in range(0, board.__lenB__()):
                if board[row][i].digit == board[row][col].digit and i != col:
                    board[row][i].set_state(SquareState.ERASED)
            for i in range(0, board.__lenA__()):
                if board[i][col].digit == board[row][col].digit and i != row:
                    board[i][col].set_state(SquareState.ERASED)

    """Возвращает соседей клетки"""

    @staticmethod
    def _get_neighbours(board, row, col):
        res = []
        for row_off in range(-1, 2):
            for col_off in range(-1, 2):
                if abs(row_off) != abs(col_off) and board.is_in_bounds(row + row_off, col + col_off):
                    res.append(board[row + row_off][col + col_off])
        return res

    """Возвращает соседей клетки с состоянием"""

    @staticmethod
    def _get_neighbours_by_state(board, row, col):
        res = defaultdict(list)
        for square in HitoriAdvancedSearch._get_neighbours(board, row, col):
            res[square.state].append(square)
        return res


class HitoriLocalSearch:
    @staticmethod
    def apply(board):
        while not board.is_solved():
            prev_board = board.__copy__()
            HitoriLocalSearch._apply_step_one(board)  # Apply step one
            HitoriAdvancedSearch.apply(board)  # Apply advanced search
            if not board.checker.is_valid(board):  # Check validity
                board.unsolvable = True
                return
            if prev_board == board:  # Check if no progress is made
                board.undetermined = True
                return

    @staticmethod
    def _apply_step_one(board):
        for row in range(board.__lenA__()):
            for col in range(board.__lenB__()):
                HitoriLocalSearch._apply_step_one_to_square(board, row, col)

    @staticmethod
    def _apply_step_one_to_square(board, row, col):
        if board[row][col].state != SquareState.UNSOLVED:
            return
        new_board = deepcopy(board)
        new_board[row][col].set_state(SquareState.KEPT)
        HitoriAdvancedSearch.board_stable(new_board)
        if not board.checker.is_valid(new_board):
            board[row][col].set_state(SquareState.ERASED)


# Статические методы присутствуют в этом коде для того, чтобы сделать их доступными без необходимости создания
# экземпляров данных классов
class HitoriBoard:
    def __init__(self, sizeA, sizeB, digits, checker):
        self.unsolvable = False
        self.undetermined = False
        self.checker = checker
        self._init_squares(sizeA, sizeB, digits)
        self._init_solution_steps()

    def _init_squares(self, sizeA, sizeB, digits):
        self.squares = []
        for row in range(sizeA):
            self.squares.append([])
            for col in range(sizeB):
                self.squares[row].append(HitoriSquare(digits[row * sizeB + col]))

    def _init_solution_steps(self):
        self.current_step = 0
        self.solution_steps = [
            HitoriBasicSearch.apply,
            HitoriAdvancedSearch.apply,
            HitoriBoard._check_validity,
            HitoriLocalSearch.apply,
        ]

    """Выводит доску в таблице с +, - и пробелами"""

    def __str__(self):
        res = ""
        for row in range(self.__lenA__()):
            for col in range(self.__lenB__()):
                res += str(self.squares[row][col])
            res += "\n"
        return res

    """Выводит высоту доски"""

    def __lenA__(self):
        return len(self.squares)

    """Выводит ширину доски"""

    def __lenB__(self):
        return len(self.squares[0])

    """Возвращает элемент с доски"""

    def __getitem__(self, index: int) -> List[HitoriSquare]:
        return self.squares[index]

    """
    Решает сначала базовым поиском, затем продвинутым, если есть ошибки, то решения нет.
    После чего запускается локальный поиск
    """

    def solve(self):
        while self.current_step < len(self.solution_steps) and not self.unsolvable:
            self.solution_steps[self.current_step](self)
            self.current_step += 1

    """Отдает нужный столбец"""

    def get_column(self, index):
        return [row[index] for row in self]

    """Проверяет, находится ли данная клетка в пределах доски"""

    def is_in_bounds(self, row, col):
        return 0 <= row < self.__lenA__() and 0 <= col < self.__lenB__()

    """Хранит секрет, случилась ли где ошибка или нет"""

    def has_invalid_squares(self):
        for row in self:
            for square in row:
                if square.state == SquareState.INVALID:
                    return True
        return False

    """
    Проверяет решенность.
    Если остались прозрачные клетки, то головоломка не решена
    """

    def is_solved(self):
        for row in self:
            for square in row:
                if square.state == SquareState.UNSOLVED:
                    return False
        return True

    """Методы сравнения, сравнивают доски по значению и состоянию каждой клетки"""

    def __eq__(self, other):
        if self.__lenB__() != other.__lenB__() or self.__lenA__() != other.__lenA__():
            return False
        for i in range(0, self.__lenA__()):
            for j in range(0, self.__lenB__()):
                if self.squares[i][j].digit == other.squares[i][j].digit and self.squares[i][j].state == \
                        other.squares[i][j].state:
                    continue
                else:
                    return False
        return True

    def __ne__(self, other):
        if self == other:
            return False
        return True

    """Копирует доску по каждой ее клеточке и затем устанавливает состояние соотвественно оригинальной доске"""

    def __copy__(self):
        list_for_copy = []
        for i in range(0, self.__lenA__()):
            for j in range(0, self.__lenB__()):
                list_for_copy.append(self.squares[i][j].digit)
        copy = HitoriBoard(self.__lenA__(), self.__lenB__(), list_for_copy, self.checker)
        for i in range(0, self.__lenA__()):
            for j in range(0, self.__lenB__()):
                copy.squares[i][j].set_state(self.squares[i][j].state)
        return copy

    @staticmethod
    def _check_validity(board):
        if not board.checker.is_valid(board):  # Головоломка не решается, если есть ошибки
            board.unsolvable = True


class HitoriBoardChecker:
    def __init__(self, number_components):
        self.number_components = number_components

    def is_valid(self, board):  # Отвечает на вопрос о нормальности доски
        if board.has_invalid_squares():
            return False
        return HitoriBoardChecker._count_components(board) <= self.number_components

    @staticmethod
    def _count_components(board: HitoriBoard):
        connected = set()
        count = 0
        for row in range(board.__lenA__()):
            for col in range(board.__lenB__()):
                square = board[row][col]
                if square not in connected:
                    if square.state != SquareState.ERASED:
                        count += 1
                    HitoriBoardChecker._connect_square(board, row, col, connected)
        return count

    @staticmethod
    def _connect_square(board, row, col, connected: set):
        connected.add(board[row][col])
        if board[row][col].state == SquareState.ERASED:
            return
        for neighbour in HitoriBoardChecker._get_neighbour_coords(board, row, col):
            r = neighbour[0]
            c = neighbour[1]
            if not board[r][c] in connected:
                HitoriBoardChecker._connect_square(board, r, c, connected)

    @staticmethod
    def _get_neighbour_coords(board, row, col):  # Возвращает листик со значениями соседних клеточек
        res = []
        for row_off in range(-1, 2):
            for col_off in range(-1, 2):
                if abs(row_off) != abs(col_off) and board.is_in_bounds(row + row_off, col + col_off):
                    res.append((row + row_off, col + col_off))
        return res




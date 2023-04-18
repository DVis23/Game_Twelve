import random
import copy
from enum import Enum


class Game_State(Enum):
    PLAYING = 0
    WIN = 1
    DEFEAT = 2


class Twelve:
    def __init__(self, length: int, count: int):
        self._length = length  # Длина игрового поля
        self._count = count  # Количество начальных значений в клетках
        self._score = 0  # Игровой счет
        self._game_state = Game_State.PLAYING  # Состояние игры
        self._game_board = [[0 for i in range(self.length)] for j in range(self.length)]  # Игровое поле
        self._generate_random_cells(self.count, 1, 3, True)  # Генерируем начальные числа на игровом поле

    @property
    def score(self) -> int:
        return self._score

    @property
    def length(self) -> int:
        return self._length

    @property
    def count(self) -> int:
        return self._count

    @property
    def game_state(self) -> Game_State:
        return self._game_state

    @score.setter
    def score(self, value):
        self._score = value

    @game_state.setter
    def game_state(self, value):
        self._game_state = value

    def __getitem__(self, indices: tuple) -> int:
        return self._game_board[indices[0]][indices[1]]

    def game_board(self):
        return copy.deepcopy(self._game_board)

    def move(self, x1, y1, x2, y2):
        # Делаем проверку на осуществимость данного шага
        if self._game_board[x1][y1] != 0 and (x1, y1) != (x2, y2) and self._check_way(x1, y1, x2, y2):

            # Если мы делаем слияние двух клеток
            if self._game_board[x1][y1] == self._game_board[x2][y2]:
                self._game_board[x2][y2], self._game_board[x1][y1] = self._game_board[x2][y2] + 1, 0
                # Обновляем игровой счет
                self.score += self._game_board[x2][y2]
                # Если мы победили, меняем состояние игры
                if self._game_board[x2][y2] == 12:
                    self.game_state = Game_State.WIN
                # Иначе добавляем новые значения в ячейки
                else:
                    count_zero_cells = self._count_zero_cells()
                    if count_zero_cells > self.count - 2:
                        self._generate_random_cells(self.count - 2, 1, 3, False)
                    elif count_zero_cells == self.count - 2:
                        self._generate_random_cells(self.count - 2, 1, 3, False)
                        # Если у нас не осталось свободных и нет вариантов хода, меняем состояние игры на проигрыш
                        if not self._check_pairs():
                            self.game_state = Game_State.DEFEAT
                    # Если у нас осталось меньше свободных клеток, чем должно быть сгенерировано,
                    # меняем состояние игры на проигрыш
                    else:
                        self.game_state = Game_State.DEFEAT

            # Если мы перемещаем клетку на пустое место
            elif self._game_board[x2][y2] == 0:
                self._game_board[x2][y2], self._game_board[x1][y1] = self._game_board[x1][y1], 0
                # Добавляем новые значения в ячейки
                count_zero_cells = self._count_zero_cells()
                if count_zero_cells > self.count - 1:
                    self._generate_random_cells(self.count - 1, 1, 3, False)
                elif count_zero_cells == self.count - 1:
                    self._generate_random_cells(self.count - 1, 1, 3, False)
                    # Если у нас не осталось свободных и нет вариантов хода, меняем состояние игры на проигрыш
                    if not self._check_pairs():
                        self.game_state = Game_State.DEFEAT
                # Если у нас осталось меньше свободных клеток, чем должно быть сгенерировано,
                # меняем состояние игры на проигрыш
                else:
                    self.game_state = Game_State.DEFEAT

    # Проверка на наличие пути от одной клетки к другой
    def _check_way(self, x1, y1, x2, y2):
        visited = set()
        matrix = self.game_board()
        matrix[x1][y1] = 0
        return self._dfs(x1, y1, x2, y2, matrix, visited)

    # Обход в глубину
    def _dfs(self, x1, y1, x2, y2, matrix, visited):
        # Проверяем, находится ли ячейка в матрице
        if x1 < 0 or x1 >= len(matrix) or y1 < 0 or y1 >= len(matrix[0]):
            return False
        # Проверяем, посещали ли уже мы эту ячейку
        if (x1, y1) in visited:
            return False
        if x1 == x2 and y1 == y2:
            return True
        if matrix[x1][y1] != 0:
            return False
        # Добавляем ячейку в посещения
        visited.add((x1, y1))
        if self._dfs(x1 + 1, y1, x2, y2, matrix, visited):
            return True
        if self._dfs(x1 - 1, y1, x2, y2, matrix, visited):
            return True
        if self._dfs(x1, y1 + 1, x2, y2, matrix, visited):
            return True
        if self._dfs(x1, y1 - 1, x2, y2, matrix, visited):
            return True
        return False

    # Генерируем в случайных ячейках случайные значения в заданном диапазоне
    def _generate_random_cells(self, count, a, b, empty):
        occupied_cells = []
        # Выбираем случайные ячейки на поле
        if empty:
            while len(occupied_cells) < count:
                cell_x, cell_y = random.randint(0, self.length - 1), random.randint(0, self.length - 1)
                if (cell_x, cell_y) not in occupied_cells:
                    occupied_cells.append((cell_x, cell_y))
        else:
            while len(occupied_cells) < count:
                cell_x, cell_y = random.randint(0, self.length - 1), random.randint(0, self.length - 1)
                # Если поле не пустое, добавляется условие проверки на пустые клетки
                if (cell_x, cell_y) not in occupied_cells and self._game_board[cell_x][cell_y] == 0:
                    occupied_cells.append((cell_x, cell_y))

        # Заполняем выбранные ячейки значениями от a до b
        for cell in occupied_cells:
            self._game_board[cell[0]][cell[1]] = random.randint(a, b)

    # Количество нулевых клеток
    def _count_zero_cells(self):
        zero_cells = 0
        for row in self._game_board:
            for cell in row:
                if cell == 0:
                    zero_cells += 1
        return zero_cells

    # Проверка на то, существуют ли рядом стоящие одинаковые значения
    def _check_pairs(self):
        for i in range(len(self._game_board)):
            for j in range(len(self._game_board[0])):
                # Проверка для всех ячеек кроме крайних правых и крайних нижних
                if i != len(self._game_board) - 1 and j != len(self._game_board[0]) - 1:
                    if self._game_board[i][j] == self._game_board[i + 1][j] != 0 or self._game_board[i][j] == self._game_board[i][j + 1] != 0:
                        return True
                # Проверка для ячеек крайних нижних, кроме самой правой нижней
                elif i == len(self._game_board) - 1 and j != len(self._game_board[0]) - 1:
                    if self._game_board[i][j] == self._game_board[i][j + 1] != 0:
                        return True
                # Проверка для ячеек крайних правых, кроме самой правой нижней
                elif j == len(self._game_board[0]) - 1 and i != len(self._game_board) - 1:
                    if self._game_board[i][j] == self._game_board[i + 1][j] != 0:
                        return True
        # Если не найдено никаких совпадающих пар, возвращаем False
        return False




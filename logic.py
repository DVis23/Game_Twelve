import random
import math
from enum import Enum


class Game_State(Enum):
    IN_PROGRESS = 0
    WIN = 1
    DEFEAT = 2


class Twelve:
    def __init__(self):
        self.score = 0
        self.game_state = None
        self.game_board = None
        self.generate_new()

    def generate_new(self):
        self.game_board = [[0 for i in range(5)] for j in range(5)]
        self.game_state = Game_State.IN_PROGRESS
        self.generate_random_cells(3, 1, 3, True)

    def move(self, x1, y1, x2, y2):
        if self.game_board[x1][y1] != 0 and (x1, y1) != (x2, y2) and self.can_reach_end(x1, y1, x2, y2):

            if self.game_board[x1][y1] == self.game_board[x2][y2]:
                self.game_board[x2][y2], self.game_board[x1][y1] = self.game_board[x2][y2] + 1, 0
                self.score += self.game_board[x2][y2]
                if self.game_board[x2][y2] == 12:
                    self.game_state = Game_State.WIN
                else:
                    if self.check_zero_cells() >= 1:
                        self.generate_random_cells(1, 1, 3, False)
                        if self.check_zero_cells() == 0:
                            if not self.check_pairs():
                                self.game_state = Game_State.DEFEAT
                    else:
                        self.game_state = Game_State.DEFEAT

            elif self.game_board[x2][y2] == 0:
                self.game_board[x2][y2], self.game_board[x1][y1] = self.game_board[x1][y1], 0
                if self.check_zero_cells() >= 2:
                    self.generate_random_cells(2, 1, 3, False)
                    if self.check_zero_cells() == 0:
                        if not self.check_pairs():
                            self.game_state = Game_State.DEFEAT
                else:
                    self.game_state = Game_State.DEFEAT

    def can_reach_end(self, x1, y1, x2, y2):
        if math.fabs(x1 - x2) == 1 or math.fabs(y1 - y2):
            return True

        # Создаем список посещенных клеток и очередь,
        # чтобы хранить клетки, которые еще не были обработаны
        visited = set()
        queue = [(x1, y1)]

        # Пока очередь не пуста, извлекаем первый элемент и проверяем его соседей
        while queue:
            curr_x, curr_y = queue.pop(0)

            # Если мы нашли конечную точку, то мы можем достичь её
            if curr_x == x2 and curr_y == y2:
                return True

            # Обходим всех соседей, чтобы проверить возможность перемещения до них
            for x, y in [(curr_x - 1, curr_y), (curr_x, curr_y - 1), (curr_x + 1, curr_y), (curr_x, curr_y + 1)]:
                # Проверяем границы поля, что были посещены и что значение клетки равно 0
                if 0 <= x < 5 and 0 <= y < 5 and (x, y) not in visited and self.game_board[y][x] == 0:
                    # Добавляем соседнюю клетку в очередь на проверку
                    visited.add((x, y))
                    queue.append((x, y))

        # Если очередь пуста, то путь до конечной точки не существует, возвращаем False
        return False

    def generate_random_cells(self, count, a, b, empty):
        if empty:
            # Выбираем случайные три ячейки на поле
            occupied_cells = []
            while len(occupied_cells) < count:
                cell_x, cell_y = random.randint(0, 4), random.randint(0, 4)
                if (cell_x, cell_y) not in occupied_cells:
                    occupied_cells.append((cell_x, cell_y))
        else:
            # Выбираем случайные три ячейки на поле
            occupied_cells = []
            while len(occupied_cells) < count:
                cell_x, cell_y = random.randint(0, 4), random.randint(0, 4)
                if (cell_x, cell_y) not in occupied_cells and self.game_board[cell_x][cell_y] == 0:
                    occupied_cells.append((cell_x, cell_y))

        # Заполняем выбранные ячейки значениями от a до b
        for cell in occupied_cells:
            self.game_board[cell[0]][cell[1]] = random.randint(a, b)

    def check_zero_cells(self):
        zero_cells = 0
        for row in self.game_board:
            for cell in row:
                if cell == 0:
                    zero_cells += 1
        return zero_cells

    def check_pairs(self):
        # Проверяем рядом стоящие элементы для каждого элемента в массиве, кроме последней строки и последнего столбца
        for i in range(len(self.game_board) - 1):
            for j in range(len(self.game_board[0]) - 1):
                if self.game_board[i][j] == self.game_board[i + 1][j] or self.game_board[i][j] == self.game_board[i][j + 1]:
                    # Если одна из пар совпадает, возвращаем True
                    return True
        # Если не найдено никаких совпадающих пар, возвращаем False
        return False

    def print_game_board(self):
        for i in range(5):
            print("|", end="")
            for j in range(5):
                print("{:<2}".format(self.game_board[i][j]), end="|")
            print("\n" + "-" * 13)




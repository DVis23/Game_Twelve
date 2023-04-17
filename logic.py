import random
import copy
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
        # Делаем проверку на осуществимость данного шага
        if self.game_board[x1][y1] != 0 and (x1, y1) != (x2, y2) and self.check_way(x1, y1, x2, y2):

            # Если мы делаем слияние двух клеток
            if self.game_board[x1][y1] == self.game_board[x2][y2]:
                self.game_board[x2][y2], self.game_board[x1][y1] = self.game_board[x2][y2] + 1, 0
                # Обновляем игровой счет
                self.score += self.game_board[x2][y2]
                # Если мы победили, меняем состояние игры
                if self.game_board[x2][y2] == 12:
                    self.game_state = Game_State.WIN
                else:
                    if self.count_zero_cells() >= 1:
                        self.generate_random_cells(1, 1, 3, False)
                        if self.count_zero_cells() == 0:
                            if not self.check_pairs():
                                self.game_state = Game_State.DEFEAT
                    else:
                        self.game_state = Game_State.DEFEAT

            # Если мы перемещаем клетку на пустое место
            elif self.game_board[x2][y2] == 0:
                self.game_board[x2][y2], self.game_board[x1][y1] = self.game_board[x1][y1], 0
                if self.count_zero_cells() >= 2:
                    self.generate_random_cells(2, 1, 3, False)
                    if self.count_zero_cells() == 0:
                        if not self.check_pairs():
                            self.game_state = Game_State.DEFEAT
                else:
                    self.game_state = Game_State.DEFEAT

    def check_way(self, x1, y1, x2, y2):
        visited = set()
        matrix = copy.deepcopy(self.game_board)
        matrix[x1][y1] = 0
        return self.dfs(x1, y1, x2, y2, matrix, visited)

    def dfs(self, x1, y1, x2, y2, matrix, visited):
        if x1 < 0 or x1 >= len(matrix) or y1 < 0 or y1 >= len(matrix[0]):
            return False
        if (x1, y1) in visited:
            return False
        if x1 == x2 and y1 == y2:
            return True
        if matrix[x1][y1] != 0:
            return False
        visited.add((x1, y1))
        if self.dfs(x1 + 1, y1, x2, y2, matrix, visited):
            return True
        if self.dfs(x1 - 1, y1, x2, y2, matrix, visited):
            return True
        if self.dfs(x1, y1 + 1, x2, y2, matrix, visited):
            return True
        if self.dfs(x1, y1 - 1, x2, y2, matrix, visited):
            return True
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

    def count_zero_cells(self):
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




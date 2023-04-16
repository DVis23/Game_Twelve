from PyQt5 import QtWidgets
import os
import sys
import logic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QTableWidget, QTableWidgetItem, QPushButton, QLabel, QVBoxLayout, QWidget, QHBoxLayout
from PyQt5.QtWidgets import QMessageBox
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = 'venv\Lib\site-packages\PyQt5\Qt5\plugins'


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.game = logic.Twelve()
        self.matrix = self.game.game_board
        self.previous_cell = None
        self.current_cell = None
        self.background_color_1 = QColor(34, 30, 40)
        self.background_color_2 = QColor(23, 20, 27)
        self.foreground_color = QColor(255, 255, 255)
        self.previous_color = QColor(78, 238, 184)
        self.current_color = QColor(236, 67, 67)
        self.dark_theme = True
        self.number_font = QFont('Arial', 23)

        self.setFixedSize(600, 450)
        self.setStyleSheet(f'background-color: {self.background_color_2.name()}; color: white;')
        self.setWindowTitle("TWELVE")
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        layout = QHBoxLayout()

        # Игровое поле
        self.gameTable = QTableWidget(5, 5)
        layout.addWidget(self.gameTable)
        self.gameTable.setStyleSheet(f'QTableView {{gridline-color: {self.foreground_color.name()}}}')
        self.gameTable.horizontalHeader().setVisible(False)  # удаляем заголовки столбцов
        self.gameTable.verticalHeader().setVisible(False)  # удаляем заголовки строк
        self.gameTable.setFixedSize(5 * 80 + 2, 5 * 80 + 2)  # фиксированный размер ячеек
        self.gameTable.cellClicked.connect(self.on_cell_clicked)

        # изменяем размер ячеек
        for i in range(self.gameTable.rowCount()):
            self.gameTable.setRowHeight(i, 80)
            for j in range(self.gameTable.columnCount()):
                self.gameTable.setColumnWidth(j, 80)
                newItem = QTableWidgetItem("")
                newItem.setFlags(Qt.ItemIsEnabled)
                self.gameTable.setItem(i, j, newItem)
                self.gameTable.item(i, j).setTextAlignment(Qt.AlignCenter)
                self.gameTable.item(i, j).setFont(self.number_font)
                self.gameTable.item(i, j).setBackground(self.background_color_1)
                self.gameTable.item(i, j).setForeground(self.foreground_color)
        self.drawMatrix()

        # убираем полосы прокрутки
        self.gameTable.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.gameTable.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # Панель управления игрой
        controlLayout = QVBoxLayout()

        self.updateButton = QPushButton("Сделать ход")
        self.updateButton.clicked.connect(self.updateMatrix)
        self.updateButton.setStyleSheet(f'background-color: {self.background_color_1.name()}; color: {self.foreground_color.name()};')
        controlLayout.addWidget(self.updateButton)

        self.scoreLabel = QLabel("Счет: 0")
        self.scoreLabel.setAlignment(Qt.AlignCenter)
        controlLayout.addWidget(self.scoreLabel)

        controlLayout.addStretch(1)
        layout.addLayout(controlLayout)
        self.centralWidget.setLayout(layout)

        # Меню
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&Настройки')
        newGameAction = QAction('Новая игра', self)
        newGameAction.setShortcut('Ctrl+E')
        newGameAction.triggered.connect(self.start_new_game)
        fileMenu.addAction(newGameAction)
        changeTheme = QAction('Поменять тему', self)
        changeTheme.setShortcut('Ctrl+S')
        changeTheme.triggered.connect(self.change_theme)
        fileMenu.addAction(changeTheme)
        exitAction = QAction('Выход', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.triggered.connect(self.close)
        fileMenu.addAction(exitAction)

    def drawMatrix(self):
        # устанавливаем значения в таблицу
        for i in range(self.gameTable.rowCount()):
            for j in range(self.gameTable.columnCount()):
                if self.matrix[i][j] != 0:
                    self.gameTable.item(i, j).setText(str(self.matrix[i][j]))
                else:
                    self.gameTable.item(i, j).setText('')

    def updateMatrix(self):
        # генерируем новую матрицу
        if self.previous_cell is not None and self.current_cell is not None:
            self.game.move(self.previous_cell[0], self.previous_cell[1], self.current_cell[0], self.current_cell[1])
            self.gameTable.item(self.previous_cell[0], self.previous_cell[1]).setBackground(self.background_color_1)
            self.gameTable.item(self.current_cell[0], self.current_cell[1]).setBackground(self.background_color_1)
            self.previous_cell = None
            self.current_cell = None
        self.matrix = self.game.game_board
        self.drawMatrix()
        self.scoreLabel.setText("Счет: " + str(self.game.score))
        if self.game.game_state != logic.Game_State.IN_PROGRESS:
            self.show_message()

    def on_cell_clicked(self, row, column):
        # Если это первый клик, запоминаем координаты ячейки и выделяем ее зеленым
        if self.previous_cell is None:
            self.previous_cell = (row, column)
            self.gameTable.setCurrentCell(row, column)
            self.gameTable.item(row, column).setBackground(self.previous_color)
        # Если это второй клик, запоминаем координаты ячейки и выделяем ее красным
        elif self.current_cell is None:
            self.current_cell = (row, column)
            self.gameTable.setCurrentCell(row, column)
            self.gameTable.item(row, column).setBackground(self.current_color)
        # Если это третий клик, сбрасываем значения и выделение ячеек
        else:
            self.gameTable.item(self.previous_cell[0], self.previous_cell[1]).setBackground(self.background_color_1)
            self.gameTable.item(self.current_cell[0], self.current_cell[1]).setBackground(self.background_color_1)
            self.previous_cell = None
            self.current_cell = None

    def start_new_game(self):
        self.game = logic.Twelve()
        self.updateMatrix()

    def show_message(self):
        msg_box = QMessageBox()
        msg_box.setStandardButtons(QMessageBox.Ok)
        if self.game.game_state == logic.Game_State.WIN:
            msg_box.setText("ВЫ ПОБЕДИЛИ! \n ВАШ СЧЕТ: " + str(self.game.score))
        elif self.game.game_state == logic.Game_State.DEFEAT:
            msg_box.setText("ВЫ ПРОИГРАЛИ\n ВАШ СЧЕТ: " + str(self.game.score))
        msg_box.buttonClicked.connect(self.start_new_game)
        msg_box.exec_()

    def change_theme(self):
        if self.dark_theme:
            self.background_color_1 = QColor(255, 255, 255)
            self.background_color_2 = QColor(245, 245, 245)
            self.foreground_color = QColor(0, 0, 0)
            self.setStyleSheet(f'background-color: {self.background_color_2.name()}; color: {self.foreground_color.name()};')
            self.gameTable.setStyleSheet(f'QTableView {{gridline-color: {self.foreground_color.name()}}}')
            self.updateButton.setStyleSheet(
                f'background-color: {self.background_color_2.name()}; color: {self.foreground_color.name()};')
            self.dark_theme = False
        else:
            self.background_color_1 = QColor(34, 30, 40)
            self.background_color_2 = QColor(23, 20, 27)
            self.foreground_color = QColor(255, 255, 255)
            self.setStyleSheet(f'background-color: {self.background_color_2.name()}; color: {self.foreground_color.name()};')
            self.gameTable.setStyleSheet(f'QTableView {{gridline-color: {self.foreground_color.name()}}}')
            self.updateButton.setStyleSheet(f'background-color: {self.background_color_1.name()}; color: {self.foreground_color.name()};')
            self.dark_theme = True
        for i in range(self.gameTable.rowCount()):
            for j in range(self.gameTable.columnCount()):
                self.gameTable.item(i, j).setBackground(self.background_color_1)
                self.gameTable.item(i, j).setForeground(self.foreground_color)
        self.drawMatrix()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
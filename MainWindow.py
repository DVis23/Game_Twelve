import os
import Twelve
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFontDatabase, QFont
from PyQt5.QtWidgets import QMainWindow, QAction, QTableWidget, QTableWidgetItem
from PyQt5.QtWidgets import QMessageBox, QPushButton, QLabel, QVBoxLayout, QWidget, QHBoxLayout
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = 'venv\Lib\site-packages\PyQt5\Qt5\plugins'


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.length = 5
        self.count = 3
        self.game = Twelve.Twelve(self.length, self.count)
        self.matrix = self.game._game_board
        self.previous_cell = None
        self.current_cell = None
        self.background_color_1 = QColor(34, 30, 40)
        self.background_color_2 = QColor(23, 20, 27)
        self.foreground_color = QColor(255, 255, 255)
        self.previous_color = QColor(78, 238, 184)
        self.current_color = QColor(236, 67, 67)
        self.dark_theme = True

        font_id = QFontDatabase.addApplicationFont('font/font_1.ttf')
        font_1 = QFontDatabase.applicationFontFamilies(font_id)[0]
        self.font_text = QFont(font_1, 12)
        self.font_button = QFont(font_1, 18)
        self.number_font = QFont(font_1, 23)

        self.setFixedSize(600, 450)
        self.setStyleSheet(f'background-color: {self.background_color_2.name()}; color: white;')
        self.setWindowTitle("TWELVE")
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        layout = QHBoxLayout()

        # Игровое поле
        self.gameTable = QTableWidget(self.length, self.length)
        layout.addWidget(self.gameTable)
        self.gameTable.setStyleSheet(f'QTableView {{gridline-color: {self.foreground_color.name()}}};')
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
        self.draw_matrix()

        # убираем полосы прокрутки
        self.gameTable.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.gameTable.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # Панель управления игрой
        controlLayout = QVBoxLayout()

        self.updateButton = QPushButton("Сделать ход")
        self.updateButton.setFixedSize(173, 60)
        self.updateButton.clicked.connect(self.update_view)
        self.updateButton.setStyleSheet(f'background-color: {self.background_color_1.name()}; color: {self.previous_color.name()};')
        self.updateButton.setFont(self.font_button)
        controlLayout.addWidget(self.updateButton)

        self.scoreLabel = QLabel("Счет: 0")
        self.scoreLabel.setFont(self.font_text)
        self.scoreLabel.setStyleSheet(f'color: {self.current_color.name()};')
        self.scoreLabel.setAlignment(Qt.AlignCenter)
        controlLayout.addWidget(self.scoreLabel)

        controlLayout.addStretch(1)
        layout.addLayout(controlLayout)
        self.centralWidget.setLayout(layout)

        # Меню
        self.menubar = self.menuBar()
        self.menubar.setStyleSheet(f'color: {self.previous_color.name()};')
        fileMenu = self.menubar.addMenu('&Настройки')
        self.menubar.setFont(self.font_text)
        fileMenu.setFont(self.font_text)
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

    def draw_matrix(self):
        # устанавливаем значения в таблицу
        for i in range(self.gameTable.rowCount()):
            for j in range(self.gameTable.columnCount()):
                if self.matrix[i][j] != 0:
                    self.gameTable.item(i, j).setText(str(self.matrix[i][j]))
                else:
                    self.gameTable.item(i, j).setText('')

    def update_view(self):
        # генерируем новую матрицу
        if self.previous_cell is not None and self.current_cell is not None:
            self.game.move(self.previous_cell[0], self.previous_cell[1], self.current_cell[0], self.current_cell[1])
            self.gameTable.item(self.previous_cell[0], self.previous_cell[1]).setBackground(self.background_color_1)
            self.gameTable.item(self.current_cell[0], self.current_cell[1]).setBackground(self.background_color_1)
            self.previous_cell = None
            self.current_cell = None
        self.matrix = self.game._game_board
        self.draw_matrix()
        self.scoreLabel.setText("Счет: " + str(self.game.score))
        if self.game.game_state != Twelve.Game_State.PLAYING:
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
        self.game = Twelve.Twelve(self.length, self.count)
        self.update_view()

    def show_message(self):
        msg_box = QMessageBox()
        msg_box.setStandardButtons(QMessageBox.Ok)
        if self.game.game_state == Twelve.Game_State.WIN:
            msg_box.setText("ВЫ ПОБЕДИЛИ! \n ВАШ СЧЕТ: " + str(self.game.score))
        elif self.game.game_state == Twelve.Game_State.DEFEAT:
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
            self.updateButton.setStyleSheet(f'background-color: {self.background_color_2.name()}; color: {self.foreground_color.name()};')
            self.menubar.setStyleSheet(f'color: {self.foreground_color.name()};')
            self.scoreLabel.setStyleSheet(f'color: {self.foreground_color.name()};')
            self.dark_theme = False
        else:
            self.background_color_1 = QColor(34, 30, 40)
            self.background_color_2 = QColor(23, 20, 27)
            self.foreground_color = QColor(255, 255, 255)
            self.setStyleSheet(f'background-color: {self.background_color_2.name()}; color: {self.foreground_color.name()};')
            self.gameTable.setStyleSheet(f'QTableView {{gridline-color: {self.foreground_color.name()}}}')
            self.updateButton.setStyleSheet(f'background-color: {self.background_color_1.name()}; color: {self.previous_color.name()};')
            self.menubar.setStyleSheet(f'color: {self.previous_color.name()};')
            self.scoreLabel.setStyleSheet(f'color: {self.current_color.name()};')
            self.dark_theme = True
        for i in range(self.gameTable.rowCount()):
            for j in range(self.gameTable.columnCount()):
                self.gameTable.item(i, j).setBackground(self.background_color_1)
                self.gameTable.item(i, j).setForeground(self.foreground_color)
        self.draw_matrix()
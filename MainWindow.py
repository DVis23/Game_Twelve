import os
import Twelve
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFontDatabase, QFont, QPalette
from PyQt5.QtWidgets import QMainWindow, QAction, QTableWidget, QTableWidgetItem, QColorDialog, QDialog, QApplication
from PyQt5.QtWidgets import QMessageBox, QPushButton, QLabel, QVBoxLayout, QWidget, QHBoxLayout
from DesignThemeWindow import DesignThemeWindow, DESIGN_THEME
from GameRulesWindow import GameRulesWindow

os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = 'venv\Lib\site-packages\PyQt5\Qt5\plugins'


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.length = 5
        self.count = 3
        self.game = Twelve.Twelve(self.length, self.count)
        self.design_theme = None
        self.previous_cell = None
        self.current_cell = None
        self.current_color = QColor(236, 67, 67)
        self.previous_color = QColor(78, 238, 184)

        font_id = QFontDatabase.addApplicationFont('font/font_1.ttf')
        font_1 = QFontDatabase.applicationFontFamilies(font_id)[0]
        self.font_text = QFont(font_1, 12)
        self.font_button = QFont(font_1, 18)
        self.number_font = QFont(font_1, 23)

        self.setFixedSize(600, 450)
        self.setWindowTitle("TWELVE")
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        layout = QHBoxLayout()

        # Игровое поле
        self.gameTable = QTableWidget(self.length, self.length)
        layout.addWidget(self.gameTable)
        self.gameTable.horizontalHeader().setVisible(False)  # удаляем заголовки столбцов
        self.gameTable.verticalHeader().setVisible(False)  # удаляем заголовки строк
        self.gameTable.setFixedSize(5 * 80 + 2, 5 * 80 + 2)  # фиксированный размер ячеек
        self.gameTable.cellClicked.connect(self.on_cell_clicked)

        # Изменяем размер ячеек
        for i in range(self.gameTable.rowCount()):
            self.gameTable.setRowHeight(i, 80)
            for j in range(self.gameTable.columnCount()):
                self.gameTable.setColumnWidth(j, 80)
                new_item = QTableWidgetItem("")
                new_item.setFlags(Qt.ItemIsEnabled)
                self.gameTable.setItem(i, j, new_item)
                self.gameTable.item(i, j).setTextAlignment(Qt.AlignCenter)
                self.gameTable.item(i, j).setFont(self.number_font)

        # Убираем полосы прокрутки
        self.gameTable.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.gameTable.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # Панель управления игрой
        controlLayout = QVBoxLayout()

        self.updateButton = QPushButton("Сделать ход")
        self.updateButton.setFixedSize(173, 60)
        self.updateButton.clicked.connect(self.update_view)
        self.updateButton.setFont(self.font_button)
        controlLayout.addWidget(self.updateButton)

        self.scoreLabel = QLabel("Счет: 0")
        self.scoreLabel.setFont(self.font_text)
        self.scoreLabel.setAlignment(Qt.AlignCenter)
        controlLayout.addWidget(self.scoreLabel)

        controlLayout.addStretch(1)
        layout.addLayout(controlLayout)
        self.centralWidget.setLayout(layout)

        # Меню
        self.menubar = self.menuBar()
        fileMenu = self.menubar.addMenu('&Настройки')
        self.menubar.setFont(self.font_text)
        fileMenu.setFont(self.font_text)
        newGameAction = QAction('Новая игра', self)
        newGameAction.setShortcut('Ctrl+E')
        newGameAction.triggered.connect(self.start_new_game)
        fileMenu.addAction(newGameAction)
        changeTheme = QAction('Сменить тему', self)
        changeTheme.setShortcut('Ctrl+S')
        changeTheme.triggered.connect(self.change_theme)
        fileMenu.addAction(changeTheme)
        gameRules = QAction('Правила игры', self)
        gameRules.setShortcut('Ctrl+W')
        gameRules.triggered.connect(self.show_game_rules)
        fileMenu.addAction(gameRules)
        exitAction = QAction('Выход', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.triggered.connect(self.close)
        fileMenu.addAction(exitAction)

        self.enter_theme(DESIGN_THEME.DARK_THEME)

    def draw_matrix(self):
        # Устанавливаем значения в таблицу
        for i in range(self.gameTable.rowCount()):
            for j in range(self.gameTable.columnCount()):
                if self.game.game_board[i][j] != 0:
                    self.gameTable.item(i, j).setText(str(self.game.game_board[i][j]))
                else:
                    self.gameTable.item(i, j).setText('')

    def update_view(self):
        # Если у нас выбраны ячейки, делаем ход
        if self.previous_cell is not None and self.current_cell is not None:
            # Убираем графическое выделение ячеек
            color = self.gameTable.palette().color(QPalette.Base)
            self.gameTable.item(self.previous_cell[0], self.previous_cell[1]).setBackground(color)
            self.gameTable.item(self.current_cell[0], self.current_cell[1]).setBackground(color)
            # Делаем ход
            self.game.move(self.previous_cell[0], self.previous_cell[1], self.current_cell[0], self.current_cell[1])
            # Убираем выделение ячеек
            self.previous_cell = None
            self.current_cell = None
        self.draw_matrix()
        # Меняем счет
        self.scoreLabel.setText("Счет: " + str(self.game.score))
        # Если состояние игры изменилось, выводим сообщение о ПОБЕДЕ/ПРОИГРЫШЕ
        if self.game.game_state != Twelve.Game_State.PLAYING:
            self.show_message()

    def on_cell_clicked(self, row, column):
        color = self.gameTable.palette().color(QPalette.Base)
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
            self.gameTable.item(self.previous_cell[0], self.previous_cell[1]).setBackground(color)
            self.gameTable.item(self.current_cell[0], self.current_cell[1]).setBackground(color)
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

    def show_game_rules(self):
        rules_dialog = GameRulesWindow(self.design_theme)
        rules_dialog.exec_()

    def change_theme(self):
        theme_dialog = DesignThemeWindow(self.design_theme)
        if theme_dialog.exec_() == QDialog.Accepted and theme_dialog.design_theme is not None:
            design_theme = theme_dialog.design_theme
            self.enter_theme(design_theme)

    def enter_theme(self, design_theme: DESIGN_THEME):
        # Создаем словарь для соответствия темы и файлов QSS
        theme_files = {
            DESIGN_THEME.DAY_THEME: "theme/day_theme.qss",
            DESIGN_THEME.DARK_THEME: "theme/dark_theme.qss"
        }
        # Проверяем, есть ли файл QSS для выбранной темы
        if design_theme not in theme_files:
            raise ValueError("Не найден файл QSS для выбранной темы")
        # Загружаем стиль из файла QSS
        with open(theme_files[design_theme], "r") as file:
            style = file.read()
            self.setStyleSheet(style)
        # Добавляем вызов repaint(), чтобы гарантировать отрисовку стиля
        self.repaint()
        # Обрабатываем события для принудительной отрисовки
        QApplication.processEvents()
        self.design_theme = design_theme
        color = self.gameTable.palette().color(QPalette.Base)
        # Устанавливаем цвет фона для всех ячеек таблицы
        for i in range(self.gameTable.rowCount()):
            for j in range(self.gameTable.columnCount()):
                self.gameTable.item(i, j).setBackground(color)
        self.draw_matrix()

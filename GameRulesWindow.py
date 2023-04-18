from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFontDatabase, QFont
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QWidget, QPushButton
from DesignThemeWindow import DESIGN_THEME


class GameRulesWindow(QDialog):
    def __init__(self, design_theme: DESIGN_THEME):
        super().__init__()
        self.background_color_1 = None
        self.background_color_2 = None
        self.foreground_color = None
        self.previous_color = None
        self.current_color = None
        self.now_design_theme = design_theme
        self.setWindowTitle('Правила игры')
        self.label = QLabel(self)
        self.label.setText("""Логическая игра «Twelve» является аналогом игры 2048 с некоторыми отличиями. 
        Размер поля фиксирован — 5х5 клеток. 
        Нужно собрать число 12. Нумерация фишек идет по порядку от единицы с шагом 1. 

        Соединяясь, пара фишек с одинаковыми числами образуют одну фишку с числом, на единицу большим, чем у соединяющихся. 
        Обязательное скольжение фишки к краю при перемещении отсутствует. 
        Если на поле не осталось возможных ходов, и отсутствует место для генерации новых фишек, игра считается проигранной.
        
        """)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setWordWrap(True)
        size = self.label.sizeHint()
        self.setFixedSize(size.width() + 20, size.height() + 70)
        self.close_button = QPushButton("Закрыть")
        self.close_button.clicked.connect(self.close)

        font_id = QFontDatabase.addApplicationFont('font/font_1.ttf')
        font_1 = QFontDatabase.applicationFontFamilies(font_id)[0]
        self.font_text = QFont(font_1, 9)
        self.font_button = QFont(font_1, 15)
        self.label.setFont(self.font_text)
        self.close_button.setFont(self.font_button)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.close_button)
        self.setLayout(layout)
        self.dialog_theme()

    def dialog_theme(self):
        if self.now_design_theme == DESIGN_THEME.DAY_THEME:
            self.background_color_1 = QColor(255, 255, 255)
            self.background_color_2 = QColor(245, 245, 245)
            self.foreground_color = QColor(0, 0, 0)
            self.previous_color = QColor(78, 238, 184)
            self.current_color = QColor(236, 67, 67)
            self.setStyleSheet(f'background-color: {self.background_color_2.name()}; color: {self.foreground_color.name()};')
            self.close_button.setStyleSheet(f'background-color: {self.background_color_2.name()}; color: {self.foreground_color.name()};')
            self.label.setStyleSheet(f'color: {self.foreground_color.name()};')
        elif self.now_design_theme == DESIGN_THEME.DARK_THEME:
            self.background_color_1 = QColor(34, 30, 40)
            self.background_color_2 = QColor(23, 20, 27)
            self.foreground_color = QColor(255, 255, 255)
            self.previous_color = QColor(78, 238, 184)
            self.current_color = QColor(236, 67, 67)
            self.setStyleSheet(f'background-color: {self.background_color_2.name()}; color: {self.foreground_color.name()};')
            self.close_button.setStyleSheet(f'background-color: {self.background_color_1.name()}; color: {self.previous_color.name()};')
            self.label.setStyleSheet(f'color: {self.current_color.name()};')



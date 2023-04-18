from enum import Enum

from PyQt5.QtGui import QColor, QFontDatabase, QFont
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton


class DESIGN_THEME(Enum):
    DARK_THEME = 0
    DAY_THEME = 1


class DesignThemeWindow(QDialog):
    def __init__(self, now_design_theme: DESIGN_THEME):
        super().__init__()
        self.current_color = None
        self.previous_color = None
        self.now_design_theme = now_design_theme
        self.background_color_1 = None
        self.background_color_2 = None
        self.foreground_color = None
        self.design_theme = None
        self.setWindowTitle("Выбор темы")
        self.setFixedSize(400, 120)
        self.layout = QVBoxLayout(self)
        self.label = QLabel("Выберете тему:")
        self.layout.addWidget(self.label)
        self.button_dark_theme = QPushButton("DARK_THEME")
        self.button_day_theme = QPushButton("DAY_THEME")
        self.layout.addWidget(self.button_dark_theme)
        self.layout.addWidget(self.button_day_theme)
        font_id = QFontDatabase.addApplicationFont('font/font_1.ttf')
        font_1 = QFontDatabase.applicationFontFamilies(font_id)[0]
        self.font_text = QFont(font_1, 10)
        self.font_button = QFont(font_1, 11)
        self.button_dark_theme.setFont(self.font_button)
        self.button_day_theme.setFont(self.font_button)
        self.label.setFont(self.font_text)

        self.dialog_theme()

        self.button_dark_theme.clicked.connect(self.enter_dark_theme)
        self.button_day_theme.clicked.connect(self.enter_day_theme)

    def enter_dark_theme(self):
        self.design_theme = DESIGN_THEME.DARK_THEME
        self.accept()

    def enter_day_theme(self):
        self.design_theme = DESIGN_THEME.DAY_THEME
        self.accept()

    def dialog_theme(self):
        if self.now_design_theme == DESIGN_THEME.DAY_THEME:
            self.background_color_1 = QColor(255, 255, 255)
            self.background_color_2 = QColor(245, 245, 245)
            self.foreground_color = QColor(0, 0, 0)
            self.previous_color = QColor(78, 238, 184)
            self.current_color = QColor(236, 67, 67)
            self.setStyleSheet(f'background-color: {self.background_color_2.name()}; color: {self.foreground_color.name()};')
            self.button_dark_theme.setStyleSheet(f'background-color: {self.background_color_2.name()}; color: {self.foreground_color.name()};')
            self.button_day_theme.setStyleSheet(f'background-color: {self.background_color_2.name()}; color: {self.foreground_color.name()};')
            self.label.setStyleSheet(f'color: {self.foreground_color.name()};')
        elif self.now_design_theme == DESIGN_THEME.DARK_THEME:
            self.background_color_1 = QColor(34, 30, 40)
            self.background_color_2 = QColor(23, 20, 27)
            self.foreground_color = QColor(255, 255, 255)
            self.previous_color = QColor(78, 238, 184)
            self.current_color = QColor(236, 67, 67)
            self.setStyleSheet(f'background-color: {self.background_color_2.name()}; color: {self.foreground_color.name()};')
            self.button_dark_theme.setStyleSheet(f'background-color: {self.background_color_1.name()}; color: {self.previous_color.name()};')
            self.button_day_theme.setStyleSheet(f'background-color: {self.background_color_1.name()}; color: {self.previous_color.name()};')
            self.label.setStyleSheet(f'color: {self.current_color.name()};')

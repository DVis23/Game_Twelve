from PyQt5.QtGui import QFontDatabase, QFont
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton


class DesignThemeWindow(QDialog):
    def __init__(self, now_design_theme):
        super().__init__()
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

        self.button_dark_theme.clicked.connect(self.enter_dark_theme)
        self.button_day_theme.clicked.connect(self.enter_day_theme)

        self.setStyleSheet(now_design_theme)

    def enter_dark_theme(self):
        with open('theme/dark_theme.qss', "r") as file:
            style = file.read()
            self.design_theme = style
        self.accept()

    def enter_day_theme(self):
        with open('theme/day_theme.qss', "r") as file:
            style = file.read()
            self.design_theme = style
        self.accept()

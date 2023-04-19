from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFontDatabase, QFont
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QWidget, QPushButton


class GameRulesWindow(QDialog):
    def __init__(self, design_theme):
        super().__init__()
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

        self.setStyleSheet(design_theme)



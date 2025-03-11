from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QFrame,
                             QHBoxLayout, QVBoxLayout, QLabel, QSizePolicy, QToolButton,
                             QLineEdit, QPushButton, QMessageBox, QStackedWidget)
from PyQt5.QtGui import QFont, QFontDatabase, QIcon
from PyQt5.QtCore import Qt, QSize


class SettingsPanel(QWidget):

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.initUI()

    def initUI(self):

        self.left_layout = QVBoxLayout(self)
        self.left_layout.setContentsMargins(0, 0, 0, 0)
        self.left_layout.setSpacing(15)

        container = QWidget(self)
        container.setStyleSheet("background-color: #f3f3f3;")
        container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(0, 10, 0, 0)
        container_layout.setSpacing(15)

        # Title
        title_label = QLabel("Graphing Calculator", self)
        title_label.setStyleSheet("color: #595959; font-weight: bold; font-size: 32px; font-family: Righteous")
        container_layout.addWidget(title_label, 0)

        # Toolbar
        backbar = self.setup_backbar()
        container_layout.addWidget(backbar, 0)

        container_layout.addStretch(1)

        self.left_layout.addWidget(container)

    def setup_backbar(self):

        backbar = QFrame()
        backbar.setStyleSheet("background-color: #d9d9d9; border: none;")
        backbar.setFixedHeight(50)
        backbar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        backbar_layout = QHBoxLayout(backbar)
        backbar_layout.setContentsMargins(0, 0, 0, 0)
        backbar_layout.setSpacing(0)
        backbar_layout.setAlignment(Qt.AlignCenter)

        back_label = QLabel("Back", self)
        back_label.setStyleSheet("color: white; font-size: 14px; font-family: Calibri;")
        back_label.setAlignment(Qt.AlignCenter)
        back_label.setCursor(Qt.PointingHandCursor)

        back_label.mousePressEvent = self.go_back_to_equations
        backbar_layout.addWidget(back_label)

        return backbar

    def go_back_to_equations(self, event):
        # Switches back to the main equation panel.
        self.main_window.left_section.setCurrentIndex(0)

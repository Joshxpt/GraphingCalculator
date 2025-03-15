import os
from PyQt5.QtWidgets import (QWidget, QFrame,
                             QHBoxLayout, QVBoxLayout, QLabel, QSizePolicy, QToolButton,
                             QListWidget, QMessageBox, QRadioButton, QButtonGroup, QPushButton)
from PyQt5.QtGui import QFont, QIcon, QDoubleValidator
from PyQt5.QtCore import Qt, QSize

from calculations import parse_linear_equation
from operations import solve_equation, differentiate, integrate, find_maximum, find_minimum


ICON_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets", "icons"))

class Pick_Equation_Panel(QWidget):

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.selected_equation = None
        self.initUI()

    def initUI(self):
        # Sets up the Pick Equation Panel UI.
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
        container_layout.addWidget(title_label, 0, Qt.AlignTop)

        # Toolbar (Back Button)
        backbar = self.setup_backbar()
        container_layout.addWidget(backbar, 0)

        # Operations Title
        operations_text = QLabel("Pick an equation", self)
        operations_text.setStyleSheet("color: #595959; font-weight: bold; font-size: 20px; font-family: Calibri")
        container_layout.addWidget(operations_text, 0, Qt.AlignCenter)

        self.equation_group = QButtonGroup(self)
        self.equation_container = QWidget()
        self.equation_layout = QVBoxLayout(self.equation_container)
        self.equation_container.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.equation_layout.setAlignment(Qt.AlignCenter)
        self.equation_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.load_equations()

        container_layout.addWidget(self.equation_container, 0, Qt.AlignCenter)
        container_layout.addStretch(1)  # Push everything upwards

        self.left_layout.addWidget(container)

    def setup_backbar(self):
        # Creates the back bar for navigation.
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

        back_label.mousePressEvent = self.go_back_to_mathspanel
        backbar_layout.addWidget(back_label)

        return backbar

    def go_back_to_mathspanel(self, event):
        self.main_window.left_section.setCurrentIndex(2)

    def load_equations(self):
        # Loads equations from MainWindow and displays them as radio buttons."""
        for i in reversed(range(self.equation_layout.count())):
            widget = self.equation_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        equations = self.main_window.get_all_equations()

        if not equations:
            placeholder = QLabel("No equations entered.")
            placeholder.setStyleSheet("color: #595959; font-size: 16px;")
            self.equation_layout.addWidget(placeholder)
        else:
            self.equation_group.setExclusive(False)

            radio_buttons = []

            for equation in equations:
                radio_button = QRadioButton(equation)
                radio_button.setStyleSheet("font-size: 16px; color: #595959;")
                radio_button.setChecked(False)
                radio_button.clicked.connect(lambda checked, eq=equation: self.execute_operation(eq))
                self.equation_group.addButton(radio_button)
                self.equation_layout.addWidget(radio_button)
                radio_buttons.append(radio_button)

            for button in radio_buttons:
                button.setAutoExclusive(False)
                button.setChecked(False)
                button.setAutoExclusive(True)
            self.equation_group.setExclusive(True)

            self.setFocus()

    def execute_operation(self, equation):
        # Executes the stored operation from Maths Panel on the selected equation."""
        self.selected_equation = equation
        self.main_window.maths_panel.perform_operation(self.selected_equation)
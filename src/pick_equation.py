import os
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QRadioButton, QButtonGroup, QLabel,
                                 QPushButton, QMessageBox, QScrollArea, QGroupBox,
                                 QHBoxLayout, QCheckBox, QLineEdit, QSizePolicy, QFrame)
from PyQt5.QtCore import Qt

ICON_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets", "icons"))

class Pick_Equation_Panel(QWidget):

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.selected_equation = None
        self.selected_equations = []
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

        title_label = QLabel("Graphing Calculator", self)
        title_label.setStyleSheet("color: #595959; font-weight: bold; font-size: 32px; font-family: Righteous")
        container_layout.addWidget(title_label, 0, Qt.AlignTop)

        backbar = self.setup_backbar()
        container_layout.addWidget(backbar, 0)

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
        back_label.mousePressEvent = self.go_back_to_mathspanel
        backbar_layout.addWidget(back_label)

        return backbar

    def go_back_to_mathspanel(self, event):
        self.main_window.left_section.setCurrentIndex(2)

    def load_equations(self, multi_select=False):
        for i in reversed(range(self.equation_layout.count())):
            widget = self.equation_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        equations = self.main_window.get_all_equations()
        self.equation_group.setExclusive(not multi_select)
        self.selected_equations = []

        if not equations:
            placeholder = QLabel("No equations entered.")
            placeholder.setStyleSheet("color: #595959; font-size: 16px;")
            self.equation_layout.addWidget(placeholder)
        else:
            if multi_select:
                for equation in equations:
                    row = QWidget()
                    row_layout = QHBoxLayout(row)
                    row_layout.setContentsMargins(0, 0, 0, 0)
                    row_layout.setSpacing(5)

                    checkbox = QCheckBox(equation)
                    checkbox.setStyleSheet("font-size: 16px; color: #595959;")
                    row_layout.addWidget(checkbox)

                    lower_input = QLineEdit()
                    lower_input.setFixedWidth(50)
                    lower_input.setPlaceholderText("Lower")
                    lower_input.setStyleSheet("font-size: 14px; padding: 3px; color: #595959;")

                    upper_input = QLineEdit()
                    upper_input.setFixedWidth(50)
                    upper_input.setPlaceholderText("Upper")
                    upper_input.setStyleSheet("font-size: 14px; padding: 3px; color: #595959;")

                    row_layout.addWidget(lower_input)
                    row_layout.addWidget(upper_input)

                    self.selected_equations.append((checkbox, lower_input, upper_input))
                    self.equation_layout.addWidget(row)

                confirm = QPushButton("Calculate Area")
                confirm.setStyleSheet("padding: 8px 15px; font-size: 14px; background-color: #d9d9d9; color: #595959;")
                confirm.clicked.connect(self.execute_area_operation)
                self.equation_layout.addWidget(confirm)

            else:
                for equation in equations:
                    radio_button = QRadioButton(equation)
                    radio_button.setStyleSheet("font-size: 16px; color: #595959;")
                    radio_button.clicked.connect(lambda checked, eq=equation: self.execute_operation(eq))
                    self.equation_group.addButton(radio_button)
                    self.equation_layout.addWidget(radio_button)

    def execute_operation(self, equation):
        self.selected_equation = equation
        self.main_window.maths_panel.perform_operation(self.selected_equation)

    def execute_area_operation(self):
        selected = [
            (cb.text(), lo.text().strip(), hi.text().strip())
            for cb, lo, hi in self.selected_equations
            if cb.isChecked()
        ]
        if not selected:
            QMessageBox.warning(self, "No Equations", "Please select at least one equation.")
            return
        self.main_window.maths_panel.perform_area_operation(selected)

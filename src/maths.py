from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QFrame, QHBoxLayout,
                             QRadioButton, QButtonGroup, QSizePolicy, QMessageBox,
                             QDialog, QPushButton)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import matplotlib.pyplot as plt
import tempfile
import os
from pick_equation import Pick_Equation_Panel
from calculations import parse_linear_equation
from operations import solve_equation, differentiate, integrate, find_maximum, find_minimum
import sympy as sp

class MathsPanel(QWidget):

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.selected_operation = None  # ✅ Stores selected operation
        self.initUI()

    def initUI(self):
        """Sets up the Maths Panel UI (Operation Selection)."""
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

        # Toolbar (Back Button)
        backbar = self.setup_backbar()
        container_layout.addWidget(backbar, 0)

        # Operations Title
        operations_text = QLabel("Pick an Operation", self)
        operations_text.setStyleSheet("color: #595959; font-weight: bold; font-size: 20px; font-family: Calibri")
        container_layout.addWidget(operations_text, 0, Qt.AlignCenter)

        # ✅ Operation Selection (Radio Buttons)
        operations_container = QWidget()
        operations_layout = QVBoxLayout(operations_container)
        operations_layout.setAlignment(Qt.AlignCenter)

        self.operations_group = QButtonGroup(self)  # Group for mutual exclusivity

        operations = ["Solve Equation", "Find Maximum", "Find Minimum", "Differentiate", "Integrate"]
        for operation in operations:
            radio_button = QRadioButton(operation)
            radio_button.setStyleSheet("font-size: 16px; color: #595959;")
            radio_button.setFocusPolicy(Qt.NoFocus)
            radio_button.clicked.connect(lambda checked, op=operation: self.go_to_equation_selection(op))
            self.operations_group.addButton(radio_button)

            operations_layout.addWidget(radio_button)
            operations_layout.addSpacing(5)

        container_layout.addWidget(operations_container, 0, Qt.AlignCenter)
        container_layout.addStretch(1)  # Push everything upwards

        self.left_layout.addWidget(container)

    def setup_backbar(self):
        """Creates the back bar for navigation."""
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
        """Switches back to the main equation panel."""
        self.main_window.left_section.setCurrentIndex(0)

    def go_to_equation_selection(self, operation):
        """Stores the selected operation and moves to the Pick Equation Panel."""
        self.selected_operation = operation
        self.main_window.pick_equation_panel.load_equations()
        self.main_window.left_section.setCurrentIndex(3)

    def perform_operation(self, equation_str):
        # Runs the stored operation on the selected equation and returns to Maths Panel.
        parsed_equation = parse_linear_equation(equation_str)

        if parsed_equation:
            m, b, _, indep_var = parsed_equation  # ✅ Remove unused dependent variable

            independent_symbol = sp.Symbol(indep_var)
            sympy_equation = m * independent_symbol + b  # ✅ Only used for differentiation/integration

            if self.selected_operation == "Solve Equation":
                result = solve_equation(m, b, independent_symbol)
            elif self.selected_operation == "Differentiate":
                result = sp.diff(sympy_equation, independent_symbol)
            elif self.selected_operation == "Integrate":
                result = sp.integrate(sympy_equation, independent_symbol)
            elif self.selected_operation == "Find Maximum":
                result = find_maximum(m, b)
            elif self.selected_operation == "Find Minimum":
                result = find_minimum(m, b)
            else:
                result = "Operation not implemented yet"

            result = result.rewrite(sp.Rational)
            result = sp.nsimplify(result, rational=True)

            formatted_result = sp.latex(result)

            self.show_result_dialog(formatted_result)

            self.operations_group.setExclusive(False)
            for button in self.operations_group.buttons():
                button.setChecked(False)
            self.operations_group.setExclusive(True)
        self.main_window.left_section.setCurrentIndex(2)

    def show_result_dialog(self, latex_expression):
        # Displays the result in a properly formatted popup using QLabel with MathML support.
        temp_dir = tempfile.gettempdir()
        img_path = os.path.join(temp_dir, "result.png")

        #  Create a Matplotlib figure to render LaTeX
        fig, ax = plt.subplots(figsize=(3, 1))
        ax.text(0.5, 0.5, f"${latex_expression}$", fontsize=20, ha='center', va='center', color='white')
        ax.axis("off")
        plt.savefig(img_path, dpi=300, bbox_inches='tight', transparent=True)
        plt.close(fig)

        dialog = QDialog(self)
        dialog.setWindowTitle(self.selected_operation)
        layout = QVBoxLayout()

        result_label = QLabel()
        result_label.setPixmap(QPixmap(img_path))
        layout.addWidget(result_label)

        close_button = QPushButton("Close")
        close_button.clicked.connect(dialog.accept)
        layout.addWidget(close_button)

        dialog.setLayout(layout)
        dialog.exec_()
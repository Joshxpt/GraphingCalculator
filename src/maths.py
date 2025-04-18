import re
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QFrame, QHBoxLayout,
                             QRadioButton, QButtonGroup, QSizePolicy,
                             QDialog, QPushButton)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import matplotlib.pyplot as plt
import tempfile
import os
from calculations import parse_equation
from operations import solve_equation, find_maximum, find_minimum, convert_to_sympy
import sympy as sp

class MathsPanel(QWidget):

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.selected_operation = None
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

        operations_container = QWidget()
        operations_layout = QVBoxLayout(operations_container)
        operations_layout.setAlignment(Qt.AlignCenter)

        self.operations_group = QButtonGroup(self)

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

        # Advanced Operations Title
        advanced_text = QLabel("Advanced Operations", self)
        advanced_text.setStyleSheet("color: #595959; font-weight: bold; font-size: 20px; font-family: Calibri;")
        container_layout.addWidget(advanced_text, 0, Qt.AlignCenter)

        # Advanced Operation Radio
        area_button = QRadioButton("Find Area Under Graphs")
        area_button.setStyleSheet("font-size: 16px; color: #595959;")
        area_button.setFocusPolicy(Qt.NoFocus)
        area_button.clicked.connect(lambda checked, op="Find Area Under Graphs": self.go_to_area_panel(op))
        self.operations_group.addButton(area_button)

        stationary_button = QRadioButton("Find Stationary Points")
        stationary_button.setStyleSheet("font-size: 16px; color: #595959;")
        stationary_button.setFocusPolicy(Qt.NoFocus)
        stationary_button.clicked.connect(
            lambda checked, op="Find Stationary Points": self.go_to_equation_selection(op))
        self.operations_group.addButton(stationary_button)

        container_layout.addWidget(area_button, 0, Qt.AlignCenter)
        container_layout.addWidget(stationary_button, 0, Qt.AlignCenter)

        container_layout.addStretch(1)

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
        parsed_equation = parse_equation(equation_str)

        if parsed_equation:
            equation_type, coefficients, _, indep_var = parsed_equation
            independent_symbol = sp.Symbol(indep_var)

            if equation_type == "symbolic":
                sympy_equation = coefficients
            else:
                sympy_equation = convert_to_sympy(coefficients, equation_type, indep_var)

            if self.selected_operation == "Solve Equation":
                result = solve_equation(equation_type, coefficients, indep_var)
                self.show_plain_text_result_dialog(result)

            elif self.selected_operation == "Find Stationary Points":
                # First and second derivatives
                first_diff = sp.diff(sympy_equation, independent_symbol)
                second_diff = sp.diff(first_diff, independent_symbol)

                # Solve dy/dx = 0
                critical_points = sp.solve(first_diff, independent_symbol)

                result_lines = [
                    f"First derivative: {sp.latex(first_diff)}",
                    f"Second derivative: {sp.latex(second_diff)}"
                ]

                if not critical_points:
                    result_lines.append("No stationary points found.")
                else:
                    for point in critical_points:
                        try:
                            point_val = float(point)
                            y_val = sympy_equation.subs(independent_symbol, point_val)
                            curvature = second_diff.subs(independent_symbol, point_val)
                            if curvature > 0:
                                nature = "Minimum"
                            elif curvature < 0:
                                nature = "Maximum"
                            else:
                                nature = "Point of Inflection"

                            result_lines.append(
                                f"At x = {point_val:.2f}, y = {y_val.evalf():.2f} → {nature}"
                            )
                        except Exception as e:
                            result_lines.append(f"Could not evaluate point {point}: {e}")

                result = "\n".join(result_lines)
                self.show_plain_text_result_dialog(result)

            else:
                # Other symbolic operations
                if self.selected_operation == "Differentiate":
                    result = sp.diff(sympy_equation, independent_symbol)
                elif self.selected_operation == "Integrate":
                    result = sp.integrate(sympy_equation, independent_symbol)
                    result = sp.nsimplify(result, rational=True)
                elif self.selected_operation == "Find Maximum":
                    result = find_maximum(equation_type, coefficients)
                elif self.selected_operation == "Find Minimum":
                    result = find_minimum(equation_type, coefficients)
                else:
                    result = "Operation not implemented yet"

                if isinstance(result, sp.Basic):
                    if isinstance(result, sp.Piecewise):
                        result = result.args[0][0]
                    result = sp.nsimplify(result, rational=True)
                    formatted_result = sp.latex(result, mode='plain').replace("log", "ln")
                elif isinstance(result, tuple):
                    formatted_result = f"({result[0]}, {result[1]})"
                else:
                    formatted_result = str(result)

                self.show_result_dialog(formatted_result)

            # Reset operation button states
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

    def show_plain_text_result_dialog(self, result_text):

        dialog = QDialog(self)
        dialog.setWindowTitle(self.selected_operation)
        layout = QVBoxLayout()

        result_label = QLabel(result_text)
        result_label.setStyleSheet("""
            font-size: 14pt;
            font-family: 'Arial';
            padding: 20px;
            color: white;
            border: 1px solid #ccc;
            border-radius: 5px;
        """)
        layout.addWidget(result_label)

        close_button = QPushButton("Close")
        close_button.clicked.connect(dialog.accept)
        layout.addWidget(close_button)

        dialog.setLayout(layout)
        dialog.exec_()

    def go_to_area_panel(self, operation):
        self.selected_operation = operation
        self.main_window.pick_equation_panel.load_equations(multi_select=True)  # Pass flag for checkboxes
        self.main_window.left_section.setCurrentIndex(3)

    def perform_area_operation(self, equation_info_list):
        total_area = sp.S(0)
        results = []

        for eq, lower_text, upper_text in equation_info_list:
            parsed = parse_equation(eq)
            if not parsed:
                results.append(f"Could not parse: {eq}")
                continue

            equation_type, coefficients, _, indep_var = parsed

            if equation_type != "symbolic":
                expr = convert_to_sympy(coefficients, equation_type, indep_var)
            else:
                expr = coefficients

            x = sp.Symbol(indep_var)

            # Convert limits or fallback to intercepts
            try:
                lower = sp.sympify(lower_text) if lower_text else None
                upper = sp.sympify(upper_text) if upper_text else None
            except ValueError:
                results.append(f"Invalid bounds for `{eq}`. Skipped.")
                continue

            if lower is None or upper is None:
                try:
                    solution = solve_equation(equation_type, coefficients, indep_var)
                    match = re.search(r"When y=0: (.*?)\n", solution + "\n")
                    if not match:
                        raise ValueError("Could not extract x-intercepts")
                    values_str = match.group(1)
                    x_vals = [float(val.strip()) for val in re.findall(r"[-+]?\d*\.?\d+", values_str)]
                    if len(x_vals) < 2:
                        raise ValueError("Not enough intercepts")
                    x_vals.sort()
                    lower = lower if lower is not None else x_vals[0]
                    upper = upper if upper is not None else x_vals[-1]
                except:
                    results.append(f"Failed to infer bounds for `{eq}`. Skipped.")
                    continue


            if lower >= upper:
                results.append(f"Lower bound must be less than upper bound for `{eq}`. Skipped.")
                continue

            try:
                integral = sp.integrate(expr, (x, lower, upper))
                area = abs(integral)

                if isinstance(area, sp.Rational):
                    formatted_area = f"{area} (≈ {float(area):.2f})"
                else:
                    formatted_area = f"{area.evalf():.2f}"

                results.append(f"Area under `{eq}` from {lower} to {upper}: {formatted_area} units²")

                if isinstance(area, sp.Rational):
                    total_area += area
                else:
                    total_area += area.evalf()

            except Exception as e:
                results.append(f"Error integrating `{eq}`: {str(e)}")

        if isinstance(total_area, sp.Rational):
            formatted_total = f"{total_area} (≈ {float(total_area):.2f})"
        else:
            formatted_total = f"{total_area.evalf():.2f}"

        results.append(f"\nTotal area: {formatted_total} units²")
        self.show_plain_text_result_dialog("\n".join(results))
        self.main_window.left_section.setCurrentIndex(2)

    def perform_stationary_operation(self, equation_str):
        parsed = parse_equation(equation_str)
        if not parsed:
            self.show_plain_text_result_dialog("Invalid equation.")
            return

        equation_type, coefficients, _, indep_var = parsed
        x = sp.Symbol(indep_var)

        if equation_type != "symbolic":
            expr = convert_to_sympy(coefficients, equation_type, indep_var)
        else:
            expr = coefficients

        first_deriv = sp.diff(expr, x)
        second_deriv = sp.diff(first_deriv, x)
        critical_points = sp.solve(first_deriv, x)

        results = [f"Second Derivative: {sp.latex(second_deriv)}", ""]

        if not critical_points:
            results.append("No stationary points found.")
        else:
            for point in critical_points:
                if not point.is_real:
                    continue
                y_val = expr.subs(x, point)
                second_val = second_deriv.subs(x, point)

                if second_val > 0:
                    nature = "Minimum"
                elif second_val < 0:
                    nature = "Maximum"
                else:
                    nature = "Point of Inflection"

                results.append(f"Stationary Point at ({point}, {y_val}): {nature}")

        self.show_plain_text_result_dialog("\n".join(results))
        self.main_window.left_section.setCurrentIndex(2)
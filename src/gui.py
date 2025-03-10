import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QFrame,
                             QHBoxLayout, QVBoxLayout, QLabel, QSizePolicy, QToolButton,
                             QLineEdit, QPushButton, QMessageBox)
from PyQt5.QtGui import QFont, QFontDatabase, QIcon
from PyQt5.QtCore import Qt, QSize

from graphing import GraphCanvas
from calculations import parse_linear_equation



# Define constants for paths
FONT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets", "fonts", "Righteous-Regular.ttf"))
ICON_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets", "icons"))

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.equation_boxes = []
        self.equations = []
        self.undo_stack = []
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Python Graphing Calculator")
        self.setFixedSize(1100, 650)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Add Font of Application
        font_id = QFontDatabase.addApplicationFont(FONT_PATH)
        if font_id < 0:
            print("Error adding font")
            app_font = QFont("Arial", 30)  # Fallback font
        else:
            families = QFontDatabase.applicationFontFamilies(font_id)
            app_font = QFont(families[0], 30) if families else QFont("Arial", 30)

        # --- MENU SECTION ---
        left_section = QWidget()
        left_section.setStyleSheet("background-color: #f3f3f3;")

        self.left_layout = QVBoxLayout(left_section)
        self.left_layout.setContentsMargins(0, 10, 0, 0)
        self.left_layout.setSpacing(15)

        # Title
        title_label = QLabel("Graphing Calculator", self)
        title_label.setStyleSheet("color: #595959;")
        title_label.setFont(app_font)

        # Menu Bar
        toolbar = self.setup_toolbar()

        # Add New Equation Button (+)
        self.add_button = QPushButton("+")
        self.add_button.setFixedSize(40, 40)
        self.add_button.setStyleSheet("border-radius: 20px; background-color: #d9d9d9; font-size: 20px;")
        self.add_button.clicked.connect(self.add_equation_box)

        self.left_layout.addWidget(title_label, 0)
        self.left_layout.addWidget(toolbar, 0)
        self.left_layout.addWidget(self.add_button, 0, Qt.AlignCenter)
        self.left_layout.addStretch(1)
        self.add_equation_box()

        # --- GRAPH SECTION ---
        self.graph_section = QWidget()
        self.graph_layout = QVBoxLayout(self.graph_section)
        self.graph_layout.setContentsMargins(0, 0, 0, 0)

        # Create Graph Canvas
        self.graph_canvas = GraphCanvas(self)
        self.graph_canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.graph_layout.addWidget(self.graph_canvas, 1)

        self.graph_section.setLayout(self.graph_layout)

        # Adding sections to window
        main_layout.addWidget(left_section, 1)
        main_layout.addWidget(self.graph_section, 5)

        # Adding sections to window
        main_layout.addWidget(left_section, 1)
        main_layout.addWidget(self.graph_section, 3)

    def setup_toolbar(self):
        # Creates the toolbar with buttons
        toolbar = QFrame()
        toolbar.setStyleSheet("background-color: #d9d9d9; border: none;")
        toolbar.setFixedHeight(50)
        toolbar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        toolbar_layout = QHBoxLayout(toolbar)
        toolbar_layout.setContentsMargins(0, 0, 0, 0)
        toolbar_layout.setSpacing(0)

        buttons = [
            ("white_settings.png", self.on_settings_clicked),
            ("white_math.png", self.on_maths_clicked),
            ("white_undo.png", self.on_undo_clicked),
            ("white_redo.png", self.on_redo_clicked)
        ]

        for icon, function in buttons:
            toolbar_layout.addWidget(self.create_toolbar_button(icon, function))

        return toolbar

    def create_toolbar_button(self, icon_name, callback):
        # Creates a QToolButton with an icon and connects it to a function.
        icon_path = os.path.join(ICON_PATH, icon_name)
        btn = QToolButton()
        btn.setIcon(QIcon(icon_path))
        btn.setIconSize(QSize(32, 32))
        btn.setStyleSheet("border: none;")
        btn.clicked.connect(callback)
        return btn

    def add_equation_box(self):
        """Creates a new equation input box and updates the UI."""

        if len(self.equation_boxes) >= 10:
            QMessageBox.warning(self, "Limit Reached", "You have reached the maximum allowed equations.")
            return

        index = len(self.equation_boxes) + 1  # Equation Number

        equation_widget = QWidget()
        equation_layout = QHBoxLayout(equation_widget)
        equation_layout.setContentsMargins(0, 0, 0, 0)
        equation_layout.setSpacing(5)

        # Number label
        number_label = QLabel(str(index))
        number_label.setFixedWidth(20)
        number_label.setAlignment(Qt.AlignCenter)
        number_label.setStyleSheet("color: #595959; font-weight: bold; font-family: Helvetica;")

        # Eye button (for toggling visibility in future)
        eye_button = QToolButton()
        eye_button.setIcon(QIcon(os.path.join(ICON_PATH, "grey_open_eye.png")))
        eye_button.setIconSize(QSize(20, 20))
        eye_button.setStyleSheet("border: none;")

        # Equation input box
        equation_input = QLineEdit()
        equation_input.setPlaceholderText("Enter equation...")
        equation_input.setFont(QFont("Times New Roman", 14))
        equation_input.setStyleSheet("color: #595959; background-color: white; border: 1px solid #ccc; padding: 5px;")

        equation_input.returnPressed.connect(lambda: self.process_equation(equation_input, equation_widget))

        # Store equation input field for reference
        equation_widget.equation_input = equation_input

        # Add widgets to layout
        equation_layout.addWidget(number_label)
        equation_layout.addWidget(eye_button)
        equation_layout.addWidget(equation_input)

        self.left_layout.insertWidget(self.left_layout.count() - 2, equation_widget)
        self.equation_boxes.append(equation_widget)

    def process_equation(self, equation_input, equation_widget):
        """Processes the input equation, updates tracking, and redraws the graph."""
        equation_text = equation_input.text().strip()

        # ✅ Ensure parsing was successful
        parsed_equation = parse_linear_equation(equation_text)
        if parsed_equation is None:
            QMessageBox.warning(self, "Invalid Equation", "Please enter a valid linear equation (e.g., 'y = 2x + 1').")
            return  # ✅ Exit function if parsing failed

        m, b = parsed_equation  # ✅ Only runs if parsing was successful

        # ✅ Check if equation already exists
        for i, (widget, _, _, _) in enumerate(self.equations):
            if widget == equation_widget:
                color = self.graph_canvas.plot_equation(m, b)  # ✅ Get line color
                self.equations[i] = (equation_widget, m, b, color)  # ✅ Update equation entry
                self.update_equation_label_color(equation_widget, color)  # ✅ Update label color
                self.update_graph()
                return

        # ✅ New equation
        color = self.graph_canvas.plot_equation(m, b)
        self.equations.append((equation_widget, m, b, color))
        self.update_equation_label_color(equation_widget, color)

    def on_settings_clicked(self):
        print("Settings button clicked!")

    def on_maths_clicked(self):
        print("Maths button clicked!")

    def on_undo_clicked(self):
        # Undo last added equation (Remove from UI and store for redo).
        if self.equation_boxes:
            equation_widget = self.equation_boxes.pop()

            for eq in self.equations:
                if eq[0] == equation_widget:
                    self.undo_stack.append(eq)
                    self.equations.remove(eq)
                    break

            self.left_layout.removeWidget(equation_widget)
            equation_widget.setParent(None)

            self.update_graph()

            if len(self.equation_boxes) < 10:
                self.add_button.setDisabled(False)

    def on_redo_clicked(self):
        # Redo (Restore last undone equation with the correct color) and update graph.
        if self.undo_stack:
            equation_widget, m, b, color = self.undo_stack.pop()
            self.equation_boxes.append(equation_widget)
            self.left_layout.insertWidget(self.left_layout.count() - 2, equation_widget)

            self.equations.append((equation_widget, m, b, color))

            self.graph_canvas.plot_equation(m, b, color)

            self.update_equation_label_color(equation_widget, color)

            self.update_graph()

    def delete_last_equation(self):
        # Removes the last added equation and stores it for undo.
        if self.equation_boxes:
            equation_widget = self.equation_boxes.pop()
            self.undo_stack.append(equation_widget)
            self.left_layout.removeWidget(equation_widget)
            equation_widget.setParent(None)

    def update_equation_numbers(self):
        # Reassigns numbers to all active equation boxes.
        for index, eq_widget in enumerate(self.equation_boxes, start=1):
            number_label = eq_widget.findChild(QLabel)  # Get the number label
            if number_label:
                number_label.setText(str(index))  # Update the number

    def update_equation_label_color(self, equation_widget, color):
        """Updates the color of the number label next to an equation."""
        number_label = equation_widget.findChild(QLabel)
        if number_label:
            number_label.setStyleSheet(f"color: {color}; font-weight: bold; font-family: Helvetica;")

    def update_graph(self):
        # Redraws all equations currently in the list.
        self.graph_canvas.ax.clear()
        self.graph_canvas.plot_default_graph()  # Reset Grid

        for _, m, b, color in self.equations:
            self.graph_canvas.plot_equation(m, b, color)

        self.graph_canvas.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

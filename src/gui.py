import sys
import os
import re
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QFrame,
                             QHBoxLayout, QVBoxLayout, QLabel, QSizePolicy, QToolButton,
                             QLineEdit, QPushButton, QMessageBox, QStackedWidget)
from PyQt5.QtGui import QFont, QFontDatabase, QIcon
from PyQt5.QtCore import Qt, QSize

from graphing import GraphCanvas
from calculations import parse_equation
from settings import SettingsPanel
from maths import MathsPanel
from pick_equation import Pick_Equation_Panel


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

        # --- MENU SECTION (Equation Entry Panel) ---
        self.equation_panel = QWidget()
        self.equation_panel.setStyleSheet("background-color: #f3f3f3;")
        self.left_layout = QVBoxLayout(self.equation_panel)
        self.left_layout.setContentsMargins(0, 10, 0, 0)
        self.left_layout.setSpacing(15)

        # Title
        title_label = QLabel("Graphing Calculator", self)
        title_label.setStyleSheet("color: #595959; font-weight: bold; font-size: 32px; font-family: Righteous")

        # Menu Bar
        toolbar = self.setup_toolbar()

        # Add New Equation Button (+)
        self.add_button = QPushButton("+")
        self.add_button.setFixedSize(40, 40)
        self.add_button.setStyleSheet("border-radius: 20px; background-color: #f3f3f3; font-size: 20px;")
        self.add_button.clicked.connect(self.add_equation_box)

        self.left_layout.addWidget(title_label, 0)
        self.left_layout.addWidget(toolbar, 0)
        self.left_layout.addWidget(self.add_button, 0, Qt.AlignCenter)
        self.left_layout.addStretch(1)
        self.add_equation_box()

        # --- SETTINGS PANEL ---
        self.settings_panel = SettingsPanel(self)

        # --- MATHS PANEL ---
        self.maths_panel = MathsPanel(self)

        # --- PICK EQUATION PANEL ---
        self.pick_equation_panel = Pick_Equation_Panel(self)

        # --- LEFT SECTION (STACKED WIDGET) ---
        self.left_section = QStackedWidget()  # Allows switching between panels
        self.left_section.addWidget(self.equation_panel)  # Index 0 → Equation Panel
        self.left_section.addWidget(self.settings_panel)  # Index 1 → Settings Panel
        self.left_section.addWidget(self.maths_panel)  # Index 2 → Maths Panel
        self.left_section.addWidget(self.pick_equation_panel)  # Index 3 → Choose Equation Panel

        # --- GRAPH SECTION ---
        self.graph_section = QWidget()
        self.graph_layout = QVBoxLayout(self.graph_section)
        self.graph_layout.setContentsMargins(0, 0, 0, 0)

        self.graph_container = QWidget(self.graph_section)
        self.graph_container_layout = QVBoxLayout(self.graph_container)
        self.graph_container_layout.setContentsMargins(0, 0, 0, 0)

        self.graph_canvas = GraphCanvas(self, main_window=self)
        self.graph_canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.graph_container_layout.addWidget(self.graph_canvas, 1)

        # --- ZOOM PANEL (Overlay) ---
        self.zoom_panel = QWidget(self.graph_container)
        self.zoom_panel.setFixedSize(100, 25)
        self.zoom_panel.setStyleSheet("background-color: #d9d9d9; border-radius: 10px; opacity: 0.8;")

        # Create layout for zoom controls
        zoom_layout = QHBoxLayout(self.zoom_panel)
        zoom_layout.setContentsMargins(5, 5, 5, 5)
        zoom_layout.setSpacing(8)

        # Create 100% Zoom Text Button
        self.zoom_label = QLabel("100%", self.zoom_panel)
        self.zoom_label.setStyleSheet("font-size: 12px; font-family: Calibri; color: #818181;")
        zoom_layout.addWidget(self.zoom_label, 1)

        # Create Zoom In Button (+)
        self.zoom_in_button = QToolButton(self.zoom_panel)
        self.zoom_in_button.setIcon(QIcon(os.path.join(ICON_PATH, "grey_plus.png")))
        self.zoom_in_button.setIconSize(QSize(14, 14))
        self.zoom_in_button.setStyleSheet("border: none;")
        zoom_layout.addWidget(self.zoom_in_button, 1)

        # Create Zoom Out Button (-)
        self.zoom_out_button = QToolButton(self.zoom_panel)
        self.zoom_out_button.setIcon(QIcon(os.path.join(ICON_PATH, "grey_minus.png")))
        self.zoom_out_button.setIconSize(QSize(14, 14))
        self.zoom_out_button.setStyleSheet("border: none;")
        zoom_layout.addWidget(self.zoom_out_button, 1)

        self.zoom_panel.setLayout(zoom_layout)

        # Position zoom panel in the bottom-right corner
        self.zoom_panel.move(
            self.graph_container.width() - self.zoom_panel.width(),
            self.graph_container.height() - self.zoom_panel.height()
        )

        # Ensure zoom panel moves dynamically on resize
        def update_zoom_panel_position(event):
            self.zoom_panel.move(
                max(self.graph_container.width() - self.zoom_panel.width(), 0),
                max(self.graph_container.height() - self.zoom_panel.height(), 0)
            )

        self.graph_container.resizeEvent = update_zoom_panel_position

        self.zoom_panel.raise_()

        self.graph_layout.addWidget(self.graph_container, 1)
        self.graph_section.setLayout(self.graph_layout)

        # Adding sections to window
        main_layout.addWidget(self.left_section, 1)  # Left Side (Switchable)
        main_layout.addWidget(self.graph_section, 5)  # Right Side (Graph)

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
        # Creates a new equation input box and updates the UI.

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

        # Eye button
        eye_button = QToolButton()
        eye_button.setIcon(QIcon(os.path.join(ICON_PATH, "grey_open_eye.png")))
        eye_button.setIconSize(QSize(20, 20))
        eye_button.setStyleSheet("border: none;")

        eye_button.clicked.connect(lambda: self.toggle_visibility(equation_widget, eye_button))

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
        # Processes the input equation, updates tracking, and redraws the graph.
        equation_text = equation_input.text().strip()

        match = re.match(r"^([a-zA-Z])=", equation_text)

        if not match:
            equation_text = "y=" + equation_text

        equation_input.setText(equation_text)

        parsed_equation = parse_equation(equation_text)
        if parsed_equation is None:
            QMessageBox.warning(self, "Invalid Equation",
                                "Please enter a valid linear or quadratic equation (e.g., 'y = 2x^2 + 3x + 5').")
            return

        equation_type, coefficients, dep_var, indep_var = parsed_equation

        for i, (widget, _, _, color, visible, _) in enumerate(self.equations):
            if widget == equation_widget:
                self.equations[i] = (equation_widget, equation_type, coefficients, color, visible, indep_var)
                self.update_equation_label_color(equation_widget, color)
                self.update_graph()
                return

        color = self.graph_canvas.plot_equation(equation_type, coefficients, indep_var)
        self.equations.append((equation_widget, equation_type, coefficients, color, True, indep_var))
        self.update_equation_label_color(equation_widget, color)

    def on_settings_clicked(self):
        if self.left_section.currentIndex() == 0:
            self.left_section.setCurrentIndex(1)  # Show Settings Panel
        else:
            self.left_section.setCurrentIndex(0)  # Show Equation Panel

    def on_maths_clicked(self):
        if self.left_section.currentIndex() != 2:
            self.left_section.setCurrentIndex(2)
        else:
            self.left_section.setCurrentIndex(0)

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
        # Redo (Restore last undone equation, ensuring it is visible with correct icon).
        if self.undo_stack:
            equation_widget, m, b, color, visible, indep_var = self.undo_stack.pop()
            self.equation_boxes.append(equation_widget)
            self.left_layout.insertWidget(self.left_layout.count() - 2, equation_widget)

            self.equations.append((equation_widget, m, b, color, True, indep_var))

            self.graph_canvas.plot_equation(m, b, indep_var, color)

            eye_button = equation_widget.findChild(QToolButton)
            if eye_button:
                eye_button.setIcon(QIcon(os.path.join(ICON_PATH, "grey_open_eye.png")))

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
        # Updates the color of the number label next to an equation.
        number_label = equation_widget.findChild(QLabel)
        if number_label:
            number_label.setStyleSheet(f"color: {color}; font-weight: bold; font-family: Helvetica;")

    def update_graph(self):
        # Redraws all equations currently visible in the list.
        self.graph_canvas.ax.clear()
        self.graph_canvas.plot_default_graph()  # Reset Grid

        for _, equation_type, coefficients, color, visible, indep_var in self.equations:
            if visible:
                self.graph_canvas.plot_equation(equation_type, coefficients, indep_var, color)

        self.graph_canvas.draw()

    def toggle_visibility(self, equation_widget, eye_button):
        # Toggles the visibility of the equation on the graph.
        for i, (widget, equation_type, coefficients, color, visible, indep_var) in enumerate(self.equations):
            if widget == equation_widget:
                new_visibility = not visible
                self.equations[i] = (widget, equation_type, coefficients, color, new_visibility, indep_var)
                icon_path = "grey_open_eye.png" if new_visibility else "grey_closed_eye.png"
                eye_button.setIcon(QIcon(os.path.join(ICON_PATH, icon_path)))

                self.update_graph()
                return

    def get_all_equations(self):
        # Returns a list of all entered equations from the equation panel.
        equations = []

        for eq_widget in self.equation_boxes:
            equation_input = eq_widget.findChild(QLineEdit)
            if equation_input:
                equations.append(equation_input.text())

        return equations


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

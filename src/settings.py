import os
from PyQt5.QtWidgets import (QWidget, QFrame,
                             QHBoxLayout, QVBoxLayout, QLabel, QSizePolicy, QToolButton,
                             QLineEdit, QMessageBox, QPushButton)
from PyQt5.QtGui import QFont, QIcon, QDoubleValidator
from PyQt5.QtCore import Qt, QSize

ICON_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets", "icons"))


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

        # Settings Title
        settings_text = QLabel("SETTINGS", self)
        settings_text.setStyleSheet("color: #595959; font-weight: bold; font-size: 20px; font-family: Calibri")
        container_layout.addWidget(settings_text, 0, Qt.AlignCenter)

        # Gridline Toggle
        gridlines_widget = self.gridlines()
        container_layout.addWidget(gridlines_widget, 0, Qt.AlignCenter)

        # Axis Numbers Toggle
        axis_numbers_widget = self.axis_numbers()
        container_layout.addWidget(axis_numbers_widget, 0, Qt.AlignCenter)

        # Update X-Axis
        x_axis_widget = self.update_x_axis()
        container_layout.addWidget(x_axis_widget, 0, Qt.AlignCenter)

        # Update X-Axis Step
        x_step_widget = self.update_x_axis_step()
        container_layout.addWidget(x_step_widget, 0, Qt.AlignCenter)

        # Update Y-Axis
        y_axis_widget = self.update_y_axis()
        container_layout.addWidget(y_axis_widget, 0, Qt.AlignCenter)

        # Update Y-Axis Step
        y_step_widget = self.update_y_axis_step()
        container_layout.addWidget(y_step_widget, 0, Qt.AlignCenter)

        # Degrees/Radians Toggle Button
        self.unit_mode = "radians"

        self.unit_button = QPushButton("Convert to Degrees")
        self.unit_button.setStyleSheet(
            "padding: 10px; font-size: 16px; background-color: #f3f3f3; border: 2px solid #595959; color: #595959;")
        self.unit_button.clicked.connect(self.toggle_unit_mode)
        container_layout.addWidget(self.unit_button, 0, Qt.AlignCenter)

        # Open User Manual
        manual_button = QPushButton("Open User Manual")
        manual_button.setStyleSheet(
            "padding: 10px; font-size: 16px; background-color: #ddd; border: none; color: #595959;")
        manual_button.clicked.connect(self.open_manual)
        container_layout.addWidget(manual_button, 0, Qt.AlignCenter)

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

    def gridlines(self):

        gridlines_widget = QWidget()
        gridlines_layout = QHBoxLayout(gridlines_widget)
        gridlines_layout.setContentsMargins(0, 0, 0, 0)
        gridlines_layout.setSpacing(5)

        # Eye button (store reference for toggling)
        self.grid_eye_button = QToolButton()
        self.grid_eye_button.setIcon(QIcon(os.path.join(ICON_PATH, "grey_open_eye.png")))
        self.grid_eye_button.setIconSize(QSize(20, 20))
        self.grid_eye_button.setStyleSheet("border: none;")
        self.grid_eye_button.clicked.connect(self.toggle_grid)

        # Text
        gridline_text = QLabel("Show/Hide Grid", self)
        gridline_text.setFont(QFont("Calibri", 14))
        gridline_text.setStyleSheet("color: #595959;")

        gridlines_layout.addWidget(self.grid_eye_button)
        gridlines_layout.addWidget(gridline_text)

        return gridlines_widget

    def toggle_grid(self):
        # Toggles grid visibility and updates icon.
        self.main_window.graph_canvas.toggle_grid()

        if self.main_window.graph_canvas.grid_enabled:
            self.grid_eye_button.setIcon(QIcon(os.path.join(ICON_PATH, "grey_open_eye.png")))
        else:
            self.grid_eye_button.setIcon(QIcon(os.path.join(ICON_PATH, "grey_closed_eye.png")))

    def axis_numbers(self):

        axis_numbers_widget = QWidget()
        axis_numbers_layout = QHBoxLayout(axis_numbers_widget)
        axis_numbers_layout.setContentsMargins(0, 0, 0, 0)
        axis_numbers_layout.setSpacing(5)

        # Eye button (store reference for toggling)
        self.axis_eye_button = QToolButton()
        self.axis_eye_button.setIcon(QIcon(os.path.join(ICON_PATH, "grey_open_eye.png")))
        self.axis_eye_button.setIconSize(QSize(20, 20))
        self.axis_eye_button.setStyleSheet("border: none;")
        self.axis_eye_button.clicked.connect(self.toggle_axis_numbers)

        # Text
        axis_numbers_text = QLabel("Show/Hide Axis Numbers", self)
        axis_numbers_text.setFont(QFont("Calibri", 14))
        axis_numbers_text.setStyleSheet("color: #595959;")

        axis_numbers_layout.addWidget(self.axis_eye_button)
        axis_numbers_layout.addWidget(axis_numbers_text)

        return axis_numbers_widget

    def toggle_axis_numbers(self):
        # Toggles axis numbers and updates icon."
        self.main_window.graph_canvas.toggle_axis_numbers()

        if self.main_window.graph_canvas.axis_numbers_enabled:
            self.axis_eye_button.setIcon(QIcon(os.path.join(ICON_PATH, "grey_open_eye.png")))
        else:
            self.axis_eye_button.setIcon(QIcon(os.path.join(ICON_PATH, "grey_closed_eye.png")))

    def update_x_axis(self):
        # Creates X-Axis range input fields and applies changes to the graph when modified.
        x_axis_widget = QWidget()
        x_axis_layout = QHBoxLayout(x_axis_widget)
        x_axis_layout.setContentsMargins(0, 0, 0, 0)
        x_axis_layout.setSpacing(5)

        validator = QDoubleValidator()

        # X Min Input
        self.x_min_input = QLineEdit()
        self.x_min_input.setPlaceholderText("-10")
        self.x_min_input.setFont(QFont("Calibri", 14))
        self.x_min_input.setStyleSheet("color: #595959; background-color: white; border: 1px solid #ccc; padding: 5px;")
        self.x_min_input.setFixedWidth(50)
        self.x_min_input.setValidator(validator)
        self.x_min_input.returnPressed.connect(self.apply_x_axis_range)

        # Range Label
        x_range_text = QLabel("≤    x    ≤", self)
        x_range_text.setFont(QFont("Calibri", 14))
        x_range_text.setStyleSheet("color: #595959;")

        # X Max Input
        self.x_max_input = QLineEdit()
        self.x_max_input.setPlaceholderText("10")
        self.x_max_input.setFont(QFont("Calibri", 14))
        self.x_max_input.setStyleSheet("color: #595959; background-color: white; border: 1px solid #ccc; padding: 5px;")
        self.x_max_input.setFixedWidth(50)
        self.x_max_input.setValidator(validator)
        self.x_max_input.returnPressed.connect(self.apply_x_axis_range)

        x_axis_layout.addWidget(self.x_min_input)
        x_axis_layout.addWidget(x_range_text)
        x_axis_layout.addWidget(self.x_max_input)

        return x_axis_widget

    def apply_x_axis_range(self):
        # Applies user-defined X-axis range to the graph.
        min_value = self.x_min_input.text().strip()
        max_value = self.x_max_input.text().strip()

        try:
            min_value = float(min_value) if min_value else -10
            max_value = float(max_value) if max_value else 10

            if min_value >= max_value:
                QMessageBox.warning(self, "Invalid Range", "Minimum X must be less than Maximum X.")
                return

            self.main_window.update_x_axis_zoom(min_value, max_value)

        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Please enter valid numbers for the X-axis range.")

    def update_y_axis(self):
        # Creates Y-Axis range input fields and applies changes to the graph when modified.
        y_axis_widget = QWidget()
        y_axis_layout = QHBoxLayout(y_axis_widget)
        y_axis_layout.setContentsMargins(0, 0, 0, 0)
        y_axis_layout.setSpacing(5)

        validator = QDoubleValidator()

        # Y Min Input
        self.y_min_input = QLineEdit()
        self.y_min_input.setPlaceholderText("-10")
        self.y_min_input.setFont(QFont("Calibri", 14))
        self.y_min_input.setStyleSheet("color: #595959; background-color: white; border: 1px solid #ccc; padding: 5px;")
        self.y_min_input.setFixedWidth(50)
        self.y_min_input.setValidator(validator)
        self.y_min_input.returnPressed.connect(self.apply_y_axis_range)

        # Range Label
        y_range_text = QLabel("≤    y    ≤", self)
        y_range_text.setFont(QFont("Calibri", 14))
        y_range_text.setStyleSheet("color: #595959;")

        # Y Max Input
        self.y_max_input = QLineEdit()
        self.y_max_input.setPlaceholderText("10")
        self.y_max_input.setFont(QFont("Calibri", 14))
        self.y_max_input.setStyleSheet("color: #595959; background-color: white; border: 1px solid #ccc; padding: 5px;")
        self.y_max_input.setFixedWidth(50)
        self.y_max_input.setValidator(validator)
        self.y_max_input.returnPressed.connect(self.apply_y_axis_range)

        y_axis_layout.addWidget(self.y_min_input)
        y_axis_layout.addWidget(y_range_text)
        y_axis_layout.addWidget(self.y_max_input)

        return y_axis_widget

    def apply_y_axis_range(self):
        # Applies user-defined Y-axis range to the graph.
        min_value = self.y_min_input.text().strip()
        max_value = self.y_max_input.text().strip()

        try:
            min_value = float(min_value) if min_value else -10
            max_value = float(max_value) if max_value else 10

            if min_value >= max_value:
                QMessageBox.warning(self, "Invalid Range", "Minimum Y must be less than Maximum Y.")
                return

            self.main_window.update_y_axis_zoom(min_value, max_value)

        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Please enter valid numbers for the Y-axis range.")

    def update_x_axis_step(self):

        x_step_widget = QWidget()
        x_step_layout = QHBoxLayout(x_step_widget)
        x_step_layout.setContentsMargins(0, 0, 0, 0)
        x_step_layout.setSpacing(5)

        validator = QDoubleValidator()

        self.x_step_input = QLineEdit()
        self.x_step_input.setFont(QFont("Calibri", 14))
        self.x_step_input.setStyleSheet("color: #595959; background-color: white; border: 1px solid #ccc; padding: 5px;")
        self.x_step_input.setFixedWidth(50)
        self.x_step_input.setValidator(validator)
        self.x_step_input.returnPressed.connect(self.apply_x_step)

        x_step_text = QLabel("Enter X-Axis Step", self)
        x_step_text.setFont(QFont("Calibri", 14))
        x_step_text.setStyleSheet("color: #595959;")

        x_step_layout.addWidget(self.x_step_input)
        x_step_layout.addWidget(x_step_text)

        return x_step_widget

    def update_y_axis_step(self):

        y_step_widget = QWidget()
        y_step_layout = QHBoxLayout(y_step_widget)
        y_step_layout.setContentsMargins(0, 0, 0, 0)
        y_step_layout.setSpacing(5)

        validator = QDoubleValidator()

        self.y_step_input = QLineEdit()
        self.y_step_input.setFont(QFont("Calibri", 14))
        self.y_step_input.setStyleSheet("color: #595959; background-color: white; border: 1px solid #ccc; padding: 5px;")
        self.y_step_input.setFixedWidth(50)
        self.y_step_input.setValidator(validator)
        self.y_step_input.returnPressed.connect(self.apply_y_step)

        y_step_text = QLabel("Enter Y-Axis Step", self)
        y_step_text.setFont(QFont("Calibri", 14))
        y_step_text.setStyleSheet("color: #595959;")

        y_step_layout.addWidget(self.y_step_input)
        y_step_layout.addWidget(y_step_text)

        return y_step_widget

    def apply_x_step(self):
        step = self.x_step_input.text().strip()
        try:
            step = float(step)
            if step <= 0:
                raise ValueError
            self.main_window.graph_canvas.x_step = step
            self.main_window.graph_canvas.plot_default_graph()
        except ValueError:
            QMessageBox.warning(self, "Invalid Step", "Please enter a positive number for the X-axis step.")

    def apply_y_step(self):
        step = self.y_step_input.text().strip()
        try:
            step = float(step)
            if step <= 0:
                raise ValueError
            self.main_window.graph_canvas.y_step = step
            self.main_window.graph_canvas.plot_default_graph()
        except ValueError:
            QMessageBox.warning(self, "Invalid Step", "Please enter a positive number for the Y-axis step.")

    def toggle_unit_mode(self):
        if self.unit_mode == "radians":
            self.unit_mode = "degrees"
            self.unit_button.setText("Convert to Radians")
            self.main_window.graph_canvas.unit_mode = "degrees"
        else:
            self.unit_mode = "radians"
            self.unit_button.setText("Convert to Degrees")
            self.main_window.graph_canvas.unit_mode = "radians"

        self.main_window.graph_canvas.plot_default_graph()

    def open_manual(self):
        self.main_window.left_section.setCurrentIndex(self.main_window.manual_index)





import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QFrame,
                             QHBoxLayout, QVBoxLayout, QLabel, QSizePolicy, QToolButton)
from PyQt5.QtGui import QFont, QFontDatabase, QIcon
from PyQt5.QtCore import Qt, QSize

# Define constants for paths
FONT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets", "fonts", "Righteous-Regular.ttf"))
ICON_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets", "icons"))

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
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
        left_section.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        left_layout = QVBoxLayout(left_section)

        # Title
        title_label = QLabel("Graphing Calculator", self)
        title_label.setAlignment(Qt.AlignTop)
        title_label.setStyleSheet("color: #595959;")
        title_label.setFont(app_font)

        # Menu Bar
        toolbar = self.setup_toolbar()  # Call setup function

        left_layout.addWidget(title_label, 0)
        left_layout.addWidget(toolbar, 0)
        left_layout.addStretch(1)

        # --- GRAPH SECTION ---
        right_section = QWidget()
        right_section.setStyleSheet("background-color: white;")
        right_section.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Adding sections to window
        main_layout.addWidget(left_section, 1)
        main_layout.addWidget(right_section, 3)

    def setup_toolbar(self):
        # Creates the toolbar with buttons
        toolbar = QFrame()
        toolbar.setStyleSheet("background-color: #d9d9d9; border: none;")
        toolbar.setFixedHeight(50)
        toolbar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        toolbar_layout = QHBoxLayout(toolbar)
        toolbar_layout.setContentsMargins(20, 5, 20, 5)
        toolbar_layout.setSpacing(20)

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

    def on_settings_clicked(self):
        print("Settings button clicked!")

    def on_maths_clicked(self):
        print("Grid button clicked!")

    def on_undo_clicked(self):
        print("Undo button clicked!")

    def on_redo_clicked(self):
        print("Redo button clicked!")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

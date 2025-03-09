import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget,
                             QHBoxLayout, QVBoxLayout, QLabel, QSizePolicy)
from PyQt5.QtGui import QFont, QFontDatabase
from PyQt5.QtCore import Qt

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
        font_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets", "fonts", "Righteous-Regular.ttf"))
        ids = QFontDatabase.addApplicationFont(font_path)
        if ids < 0: print("Error adding font")
        families = QFontDatabase.applicationFontFamilies(ids)

        # --- MENU SECTION ---
        left_section = QWidget()
        left_section.setStyleSheet("background-color: #f3f3f3;")
        left_section.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        left_layout = QVBoxLayout(left_section)

        title_label = QLabel("Graphing Calculator", self)
        title_label.setAlignment(Qt.AlignTop)
        title_label.setStyleSheet("color: #595959;")
        title_label.setFont(QFont(families[0], 30))

        left_layout.addWidget(title_label)
        left_section.setLayout(left_layout)

        # --- GRAPH SECTION ---
        right_section = QWidget()
        right_section.setStyleSheet("background-color: white;")
        right_section.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Adding sections to window
        main_layout.addWidget(left_section, 1)
        main_layout.addWidget(right_section, 3)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

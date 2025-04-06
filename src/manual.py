from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea, QSizePolicy
from PyQt5.QtCore import Qt

class ManualPanel(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Back button
        back_button = QLabel("Back")
        back_button.setStyleSheet("color: #595959; background-color: #d9d9d9; padding: 8px 20px; font-size: 14px; font-family: Calibri;")
        back_button.setFixedHeight(40)
        back_button.setMinimumWidth(250)
        back_button.setAlignment(Qt.AlignCenter)
        back_button.setCursor(Qt.PointingHandCursor)
        back_button.mousePressEvent = self.go_back_to_equations
        layout.addWidget(back_button, 0, Qt.AlignTop | Qt.AlignLeft)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.NoFrame)
        scroll.viewport().setStyleSheet("background-color: #f3f3f3;")

        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setSpacing(20)

        manual_sections = [
            ("Linear Equations", "Format: y = mx + b\nExample: y = 2x + 3"),
            ("Quadratic Equations", "Format: y = ax^2 + bx + c\nExample: y = x^2 - 4x + 7"),
            ("Cubic Equations", "Format: y = ax^3 + bx^2 + cx + d\nExample: y = x^3 - x"),
            ("Quartic Equations", "Format: y = ax^4 + bx^3 + cx^2 + dx + e\nExample: y = x^4 + 2x^2 - 1"),
            ("Reciprocal Equations", "Format: y = a / x^n\nExamples: y = 1/x, y = 3/x^2"),
            ("Exponential Equations", "Format: y = a^x\nExamples: y = 2^x, y = e^x"),
            ("Logarithmic Equations", "Format: y = logx (base 10), y = lnx (natural log), y = log[base]x\nExamples: y = logx, y = lnx, y = log[2]x"),
            ("Trigonometric Equations", "Format: y = sinx, cosx, or tanx\nExamples: y = sinx, y = cosx, y = tanx"),
            ("Inverse Trigonometric Equations" , "Format: y = arcsinx, arccosx, arctanx\nExamples: y = arcsinx, y = arctanx"),
            ("Advanced Operations – Area Under Graphs",
             "After selecting 'Find Area Under Graphs', you may tick one or more equations to include.\n"
             "You can optionally enter lower and upper x-limits for each. If these are left blank, the area will be calculated between the graph’s x-intercepts where possible.\n"
             "If the graph cannot be integrated or lacks valid bounds, it will be skipped.\n"
             "Results are shown as simplified fractions (if possible), along with a decimal approximation.")
        ]

        for title, content in manual_sections:
            title_label = QLabel(title)
            title_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #595959;")
            body_label = QLabel(content)
            body_label.setStyleSheet("font-size: 15px; color: #444;")
            body_label.setWordWrap(True)

            container_layout.addWidget(title_label)
            container_layout.addWidget(body_label)

        scroll.setWidget(container)
        layout.addWidget(scroll)

        wrapper = QWidget(self)
        wrapper.setStyleSheet("background-color: #f3f3f3;")
        wrapper_layout = QVBoxLayout(wrapper)
        wrapper_layout.setContentsMargins(0, 0, 0, 0)
        wrapper_layout.setSpacing(0)
        wrapper_layout.addLayout(layout)

        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)
        outer_layout.setSpacing(0)
        outer_layout.addWidget(wrapper)

        self.setLayout(outer_layout)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def go_back_to_equations(self, event):
        self.main_window.left_section.setCurrentIndex(0)
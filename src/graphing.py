from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import numpy as np
import random


class GraphCanvas(FigureCanvas):
    def __init__(self, parent, main_window):
       # Graphing canvas that dynamically fetches equations from the main window."""
        if main_window is None:
            raise ValueError("main_window reference is required")

        fig, self.ax = plt.subplots(figsize=(10, 8), dpi=100)
        fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
        super().__init__(fig)
        self.setParent(parent)

        self.main_window = main_window

        self.x_min, self.x_max = -10, 10
        self.y_min, self.y_max = -10, 10
        self.grid_enabled = True
        self.axis_numbers_enabled = True

        self.plot_default_graph()

    def plot_default_graph(self):
        # Plots the grid and axes while keeping existing equations intact.
        self.ax.clear()
        self.ax.set_xlim(self.x_min, self.x_max)
        self.ax.set_ylim(self.y_min, self.y_max)

        self.ax.axhline(0, color='grey', linewidth=1)
        self.ax.axvline(0, color='grey', linewidth=1)

        for spine in self.ax.spines.values():
            spine.set_visible(False)

        self.ax.set_xticks(np.arange(self.x_min, self.x_max + 1, 1))
        self.ax.set_yticks(np.arange(self.y_min, self.y_max + 1, 1))

        if self.grid_enabled:
            self.ax.grid(True, linestyle="--", color="grey", alpha=0.6)

        self.ax.set_xticklabels([])
        self.ax.set_yticklabels([])

        if self.axis_numbers_enabled:
            for x in range(int(self.x_min), int(self.x_max) + 1):
                if x != 0:
                    self.ax.annotate(str(x), (x, -0.5), fontsize=7, ha='center', va='top', color='grey')
            for y in range(int(self.y_min), int(self.y_max) + 1):
                if y != 0:
                    self.ax.annotate(str(y), (-0.5, y), fontsize=7, ha='right', va='center', color='grey')

        self.redraw_equations()
        self.draw()

    def plot_equation(self, equation_type, coefficients, indep_var, color=None):
        # Plots a linear or quadratic equation with a specified color.
        if color is None:
            color = "#{:06x}".format(random.randint(0, 0xFFFFFF))

        x_values = np.linspace(float(self.x_min), float(self.x_max), 400)

        if equation_type == "linear":
            m, b = coefficients
            y_values = m * x_values + b
            equation_label = f"{indep_var} = {m}x + {b}"

        elif equation_type == "quadratic":
            a, b, c = coefficients
            y_values = a * (x_values ** 2) + b * x_values + c
            equation_label = f"{indep_var} = {a}x² + {b}x + {c}"

        else:
            raise ValueError("Unsupported equation type")

        self.ax.plot(x_values, y_values, color=color, label=equation_label)
        self.draw()
        return color

    def toggle_grid(self):
        # Toggles grid visibility while keeping equations intact.
        self.grid_enabled = not self.grid_enabled
        self.plot_default_graph()

    def toggle_axis_numbers(self):
        # Toggles axis numbers visibility while keeping equations intact.
        self.axis_numbers_enabled = not self.axis_numbers_enabled
        self.plot_default_graph()

    def update_x_axis(self, min_x, max_x):
        # Updates the X-axis range dynamically while keeping equations.
        self.x_min = min_x
        self.x_max = max_x
        self.plot_default_graph()

    def update_y_axis(self, min_y, max_y):
        # Updates the Y-axis range dynamically while keeping equations.
        self.y_min = min_y
        self.y_max = max_y
        self.plot_default_graph()

    def redraw_equations(self):
        # Replots only the visible equations from MainWindow.
        for equation_data in self.main_window.equations:
            equation_widget, equation_type, coefficients, color, visible, indep_var = equation_data
            if visible:
                self.plot_equation(equation_type, coefficients, indep_var, color)

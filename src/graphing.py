from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import numpy as np
import random

class GraphCanvas(FigureCanvas):
    def __init__(self, parent=None):
        fig, self.ax = plt.subplots(figsize=(10, 8), dpi=100)
        fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
        super().__init__(fig)
        self.setParent(parent)

        # Default X-Axis
        self.x_min = -10.2
        self.x_max = 10.2

        #Default Y-Axis
        self.y_min = -10.2
        self.y_max = 10.2

        self.grid_enabled = True
        self.axis_numbers_enabled = True
        self.equations = []  # Store equations
        self.plot_default_graph()


    def plot_default_graph(self):
        # Plots a 4-quadrant grid.
        self.ax.clear()
        self.ax.set_xlim(self.x_min, self.x_max)
        self.ax.set_ylim(self.y_min, self.y_max)

        self.ax.axhline(0, color='grey', linewidth=1)  # X-axis
        self.ax.axvline(0, color='grey', linewidth=1)  # Y-axis

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

        self.draw()

    def plot_equation(self, m, b, color=None):
        # Plots a linear equation y = mx + b with a specified color.
        x = np.linspace(self.x_min, self.x_max, 400)
        y = m * x + b

        if color is None:
            import random
            color = "#{:06x}".format(random.randint(0, 0xFFFFFF))

        self.ax.plot(x, y, color=color)

        for i, (_, m_old, b_old, _) in enumerate(self.equations):
            if m_old == m and b_old == b:
                self.equations[i] = (None, m, b, color)
                break
        else:
            self.equations.append((None, m, b, color))

        self.draw()
        return color

    def toggle_grid(self):
        # Toggles grid visibility.
        self.grid_enabled = not self.grid_enabled
        self.refresh_graph()

    def toggle_axis_numbers(self):
        #  Toggles axis numbers
        self.axis_numbers_enabled = not self.axis_numbers_enabled
        self.refresh_graph()

    def update_x_axis(self, min_x, max_x):
        # Updates the X-axis range dynamically.
        self.x_min = min_x
        self.x_max = max_x
        self.refresh_graph()

    def update_y_axis(self, min_y, max_y):
        # Updates the X-axis range dynamically.
        self.y_min = min_y
        self.y_max = max_y
        self.refresh_graph()

    def refresh_graph(self):
            # Redraws the graph while preserving plotted equations.
            self.ax.clear()
            self.plot_default_graph()

            for _, m, b, color in self.equations:
                x_values = np.linspace(self.x_min, self.x_max, 400)
                y_values = m * x_values + b
                self.ax.plot(x_values, y_values, color=color)

            self.draw()
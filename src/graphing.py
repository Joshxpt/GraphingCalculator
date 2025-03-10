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

        self.equations = []  # Store equations
        self.plot_default_graph()

    def plot_default_graph(self):
        # Plots a 4-quadrant grid.
        self.ax.clear()
        self.ax.set_xlim(-10.5, 10.5)
        self.ax.set_ylim(-10.5, 10.5)

        self.ax.axhline(0, color='grey', linewidth=1)  # X-axis
        self.ax.axvline(0, color='grey', linewidth=1)  # Y-axis

        for spine in self.ax.spines.values():
            spine.set_visible(False)

        self.ax.set_xticks(np.arange(-10, 11, 1))
        self.ax.set_yticks(np.arange(-10, 11, 1))
        self.ax.grid(True, linestyle="--", color="grey", alpha=0.6)

        self.ax.set_xticklabels([])
        self.ax.set_yticklabels([])

        for x in range(-10, 11):
            if x != 0:
                self.ax.annotate(str(x), (x, -0.5), fontsize=7, ha='center', va='top', color='grey')
        for y in range(-10, 11):
            if y != 0:
                self.ax.annotate(str(y), (-0.5, y), fontsize=7, ha='right', va='center', color='grey')

        self.draw()

    def plot_equation(self, m, b, color=None):
        # Plots a linear equation y = mx + b with a specified color.
        x = np.linspace(-10, 10, 400)
        y = m * x + b

        if color is None:
            import random
            color = "#{:06x}".format(random.randint(0, 0xFFFFFF))

        self.ax.plot(x, y, label=f"y = {m}x + {b}", color=color)
        self.ax.legend(loc="upper left", fontsize=8)
        self.draw()

        return color

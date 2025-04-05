from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import numpy as np
import sympy as sp
import random


class GraphCanvas(FigureCanvas):
    def __init__(self, parent, main_window):
       # Graphing canvas that dynamically fetches equations from the main window."""
        if main_window is None:
            raise ValueError("main_window reference is required")

        fig, self.ax = plt.subplots(figsize=(10, 8), dpi=100)
        fig.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)
        super().__init__(fig)
        self.setParent(parent)

        self.main_window = main_window

        self.x_min, self.x_max = -10, 10
        self.y_min, self.y_max = -10, 10

        self.x_step = 1
        self.y_step = 1

        self.grid_enabled = True
        self.axis_numbers_enabled = True

        self.unit_mode = "radians"

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

        self.ax.set_frame_on(False)
        self.ax.patch.set_visible(False)

        xticks = np.arange(self.x_min, self.x_max + self.x_step, self.x_step)
        yticks = np.arange(self.y_min, self.y_max + self.y_step, self.y_step)

        # Prevent borders
        if len(xticks) > 1:
            xticks = xticks[1:]
        if len(yticks) > 1:
            yticks = yticks[:-1]

        self.ax.set_xticks(xticks)
        self.ax.set_yticks(yticks)


        self.ax.tick_params(axis='both', direction='in', length=0)

        if self.grid_enabled:
            self.ax.grid(True, linestyle="--", color="grey", alpha=0.6)

        self.ax.set_xticklabels([])
        self.ax.set_yticklabels([])

        if self.axis_numbers_enabled:
            x_offset = (self.y_max - self.y_min) * 0.02
            y_offset = (self.x_max - self.x_min) * 0.02

            for x in np.arange(self.x_min, self.x_max + self.x_step, self.x_step):
                if x != 0:
                    self.ax.annotate(
                        str(int(x)) if x.is_integer() else f"{x:.2f}",
                        (x, 0 - x_offset),
                        fontsize=7,
                        ha='center',
                        va='top',
                        color='grey'
                    )

            for y in np.arange(self.y_min, self.y_max + self.y_step, self.y_step):
                if y != 0:
                    self.ax.annotate(
                        str(int(y)) if y.is_integer() else f"{y:.2f}",
                        (0 - y_offset, y),
                        fontsize=7,
                        ha='right',
                        va='center',
                        color='grey'
                    )

        self.redraw_equations()
        self.draw()

    def plot_equation(self, equation_type, coefficients, indep_var, color=None):
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

        elif equation_type == "cubic":
            a, b, c, d = coefficients
            y_values = a * (x_values ** 3) + b * (x_values ** 2) + c * x_values + d
            equation_label = f"{indep_var} = {a}x³ + {b}x² + {c}x + {d}"

        elif equation_type == "quartic":
            a, b, c, d, e = coefficients
            y_values = a * (x_values ** 4) + b * (x_values ** 3) + c * (x_values ** 2) + d * x_values + e
            equation_label = f"{indep_var} = {a}x⁴ + {b}x³ + {c}x² + {d}x + {e}"

        elif equation_type == "reciprocal":
            numerator, exponent = coefficients
            x_values = x_values[x_values != 0]
            y_values = numerator / (x_values ** exponent)
            equation_label = f"{indep_var} = {numerator}/{indep_var}^{exponent}"

        elif equation_type == "exponential":
            (base,) = coefficients
            if base == "e":
                y_values = np.exp(x_values)
                equation_label = f"{indep_var} = e^{indep_var}"
            else:
                y_values = np.power(float(base), x_values)
                equation_label = f"{indep_var} = {base}^{indep_var}"

        elif equation_type == "logarithmic":
            (base,) = coefficients
            x_values = np.linspace(0.01, self.x_max, 400)  # Avoid log(0)
            if base == "e":
                y_values = np.log(x_values)
                equation_label = f"{indep_var} = ln({indep_var})"
            else:
                y_values = np.log(x_values) / np.log(float(base))
                equation_label = f"{indep_var} = log[{base}]({indep_var})"

        elif equation_type == "trigonometric":
            (func,) = coefficients
            x_vals = np.deg2rad(x_values) if self.unit_mode == "degrees" else x_values
            if func == "sin":
                y_values = np.sin(x_vals)
                equation_label = f"{indep_var} = sin({indep_var})"
            elif func == "cos":
                y_values = np.cos(x_vals)
                equation_label = f"{indep_var} = cos({indep_var})"
            elif func == "tan":
                y_values = np.tan(x_vals)
                y_values[np.abs(y_values) > 20] = np.nan
                equation_label = f"{indep_var} = tan({indep_var})"

        elif equation_type == "inverse_trig":
            (func,) = coefficients
            if func == "arcsin":
                x_values = x_values[(x_values >= -1) & (x_values <= 1)]
                y_values = np.arcsin(x_values)
                equation_label = f"{indep_var} = arcsin({indep_var})"
            elif func == "arccos":
                x_values = x_values[(x_values >= -1) & (x_values <= 1)]
                y_values = np.arccos(x_values)
                equation_label = f"{indep_var} = arccos({indep_var})"
            elif func == "arctan":
                y_values = np.arctan(x_values)
                equation_label = f"{indep_var} = arctan({indep_var})"
        elif equation_type == "symbolic":
            expr = coefficients
            x_sym = sp.Symbol(indep_var)

            try:
                is_trig = any(expr.has(getattr(sp, f)) for f in ["sin", "cos", "tan"])

                # Apply degrees mode if necessary
                if is_trig and self.unit_mode == "degrees":
                    x_values_eval = np.deg2rad(x_values)
                else:
                    x_values_eval = x_values

                f = sp.lambdify(x_sym, expr, modules=["numpy", "sympy"])
                y_values = f(x_values_eval)
                y_values = np.where(np.isfinite(y_values), y_values, np.nan)

            except Exception:
                y_values = np.full_like(x_values, np.nan)

            equation_label = sp.latex(expr)
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

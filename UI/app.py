import sys
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QLineEdit,
    QPushButton,
    QLabel
)
import sys
import os
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
from sympy import symbols, solve

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Logic.string_to_sym import string_to_sympy
from Logic.calculations import calculate_initial_velocity, calculate_velocity_at_1s
from sympy.plotting import plot

class Plot(QWidget):
    def __init__(self):
        super().__init__()
        self.t = symbols('t')
        
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

        self.plot = self.figure.add_subplot(111)
        self.plot.grid()

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.canvas)
        self.setLayout(self.layout)

    def update_plot(self, equation_sympy):
        self.plot.clear()
        self.plot.grid()
        
        # Convert symbolic expression to numerical function
        t_values = np.linspace(float(solve(equation_sympy, self.t)[0]), 
                             float(solve(equation_sympy, self.t)[1]), 
                             1000)
        y_values = [float(equation_sympy.subs(self.t, t_val)) for t_val in t_values]
        
        self.plot.plot(t_values, y_values)
        self.canvas.draw()

class AppWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tiro Parabólico")
        self.setGeometry(100, 100, 800, 600)

        # ── Central widget + layout ────────────────────────────────────────
        container = QWidget()
        main_layout = QHBoxLayout()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # ── Plot layout ──────────────────────────────────────────────────
        self.plot_layout = QVBoxLayout()

        self.equation_label = QLabel("Ecuación:")
        self.plot_layout.addWidget(self.equation_label)

        # self.equation_layout = QVBoxLayout()
        self.equation_input = QLineEdit()
        self.equation_input.setPlaceholderText("Ingrese la ecuación (e.g. 10t + 5t^2)")

        self.plot_button = QPushButton("Graficar")

        self.plot_layout.addWidget(self.equation_input)
        self.plot_layout.addWidget(self.plot_button)

        # Initialize the plot widget
        self.plot_widget = Plot()
        self.plot_layout.addWidget(self.plot_widget)

        main_layout.addLayout(self.plot_layout)

        # ── Results layout ─────────────────────────────────────────────────
        results_layout = QGridLayout()

        self.initial_velocity_label = QLabel("Velocidad Inicial:")
        self.velocity_at_1s_label = QLabel("Velocidad a 1s:")
        self.max_velocity_label = QLabel("Velocidad Máxima:")

        self.initial_velocity_result = QLabel("")
        self.velocity_at_1s_result = QLabel("")
        self.max_velocity_result = QLabel("")

        results_layout.addWidget(self.initial_velocity_label, 0, 0)
        results_layout.addWidget(self.initial_velocity_result, 0, 1)

        results_layout.addWidget(self.velocity_at_1s_label, 1, 0)
        results_layout.addWidget(self.velocity_at_1s_result, 1, 1)

        results_layout.addWidget(self.max_velocity_label, 2, 0)
        results_layout.addWidget(self.max_velocity_result, 2, 1)

        main_layout.addLayout(results_layout)

        self.plot_button.clicked.connect(self.plot_equation)

    def plot_equation(self):
        equation_str = self.equation_input.text().strip()
        equation_sympy = string_to_sympy(equation_str)

        initial_velocity = calculate_initial_velocity(equation_sympy)
        velocity_at_1s = calculate_velocity_at_1s(equation_sympy)

        self.initial_velocity_result.setText("{0:.2f}".format(initial_velocity)+" m/s")
        self.velocity_at_1s_result.setText("{0:.2f}".format(velocity_at_1s)+" m/s")
        self.max_velocity_result.setText("{0:.2f}".format(initial_velocity)+" m/s")

        # Update the existing plot widget
        self.plot_widget.update_plot(equation_sympy)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AppWindow()
    window.show()
    sys.exit(app.exec())

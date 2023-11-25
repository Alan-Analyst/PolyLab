import tkinter as tk
import sympy as sp
import matplotlib.pyplot as plt
import numpy as np


def perform_action():
    # Get the equation string from the entry box
    equation_str = entry_equation.get()

    try:
        # Convert the string to a SymPy expression
        equation_sym = sp.sympify(equation_str)

        # Make 'x' a symbolic variable
        x = sp.symbols('x')

        # Create a lambdify function to convert the equation to a Python function
        equation_func = sp.lambdify(x, equation_sym, modules='numpy')

        # Generate x values for plotting
        x_vals = np.linspace(-10, 10, 500)  # Adjust the range and number of points as needed

        # Compute y values using the equation function
        y_vals = equation_func(x_vals)

        # Plot the graph
        plt.figure(figsize=(8, 6))
        plt.plot(x_vals, y_vals, label=f"y = {equation_str}")
        plt.xlabel('x-axis')
        plt.ylabel('y-axis')
        plt.title('Graph of the Equation')
        plt.legend()
        plt.grid(True)
        plt.show()

    except sp.SympifyError:
        label_result.config(text="Invalid equation format!")


# Create the main window
root = tk.Tk()
root.title("Graph of Symbolic Equation")

# Entry box to input the equation
entry_equation = tk.Entry(root)
entry_equation.pack()

# Button to perform action
button = tk.Button(root, text="Plot Graph", command=perform_action)
button.pack()

# Label to display the result
label_result = tk.Label(root, text="")
label_result.pack()

# Run the tkinter main loop
root.mainloop()


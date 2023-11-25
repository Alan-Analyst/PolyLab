import matplotlib.pyplot as plt
import numpy as np
import sympy as sp
import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
import darkdetect
from buttons import Button
from setting_btn import SettingWindow
from matplotlib.animation import FuncAnimation
from settings import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
try:
    from ctypes import windll, byref, sizeof, c_int
except:
    pass

#############
# functions #
############

# def derivative():
#     # Define the variable
#     x = sp.symbols('x')
#
#     # Define the function
#     y = func_int.get()
#
#     # Calculate the derivative of the function with respect to x
#     f_prime = sp.diff(y, x)
#
#     print(f"The derivative of f(x) = {y} is f'(x) = {f_prime}")



###################
# window settings #
###################


class App(ctk.CTk):
    def __init__(self, is_dark):
        super().__init__(fg_color=(WHITE, BLACK))
        self.title('PolyLab')
        self.iconbitmap('images/icon.ico')
        self.resizable(False, False)
        display_width = self.winfo_screenwidth()
        display_height = self.winfo_screenheight()
        left = int(display_width / 2 - APP_SIZE[0] / 2)
        top = int(display_height / 2 - APP_SIZE[1] / 2)
        self.geometry(f'{APP_SIZE[0]}x{APP_SIZE[1]}+{left}+{top}')
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        ctk.set_appearance_mode(f'{"dark" if is_dark else "light"}')
        self.title_bar_color(is_dark)

        self.frame = ctk.CTkFrame(self, fg_color='transparent')
        self.frame.grid(row=0, column=0, sticky='news')
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)

        self.plot = Plot(self.frame)

        self.mainloop()

    def title_bar_color(self, is_dark):
        try:
            HWND = windll.user32.GetParent(self.winfo_id())
            DWMWA_ATTRIBUTE = 35
            COLOR = TITLE_BAR_HEX_COLORS['dark'] if is_dark else TITLE_BAR_HEX_COLORS['light']
            windll.dwmapi.DwmSetWindowAttribute(HWND, DWMWA_ATTRIBUTE, byref(c_int(COLOR)), sizeof(c_int))
        except:
            pass


class Plot:
    def __init__(self, parent):
        super().__init__()
        self.root_frame = parent

        self.frame_widget = ctk.CTkFrame(self.root_frame, corner_radius=0, fg_color='transparent')
        self.frame_widget.grid(row=0, column=0, sticky='NSEW')
        self.frame_widget.columnconfigure([0, 1, 2, 3], weight=1, uniform='a')
        self.frame_widget.rowconfigure(list(range(MAIN_ROWS)), weight=1, uniform='a')

        main_font = ctk.CTkFont(family=FONT, size=NORMAL_FONT_SIZE)
        self.func = ctk.CTkEntry(self.frame_widget,
                                 placeholder_text='function in term of x', placeholder_text_color='black',
                                 font=main_font,
                                 height=50, corner_radius=0, border_width=3, fg_color='#7d8c76', border_color='white',
                                 text_color='black')
        self.func.grid(row=0, column=0, sticky='news', columnspan=4, pady=(30, 0), rowspan=2)

        self.data = SettingWindow(self)
        self.setting_img = ctk.CTkImage(light_image=Image.open('images/setting.png'), size=(20, 20))
        self.setting_btn = ctk.CTkButton(self.frame_widget, text='',
                                         command=self.on_click, height=30, width=30,
                                         image=self.setting_img, fg_color='transparent',
                                         corner_radius=0, hover_color='#686868')
        self.setting_btn.place(x=0, y=0)

        # Buttons
        Button(parent=self.frame_widget, text='Plot', func=self.plot, col=0, row=2)
        Button(parent=self.frame_widget, text='Plot Derivative', func=self.plot_derivative, col=1, row=2)
        Button(parent=self.frame_widget, text='Find roots', func=self.find_roots, col=2, row=2)
        Button(parent=self.frame_widget, text='Mark roots', func=self.mark_roots, col=3, row=2)


        self.combobox_dim = ctk.CTkComboBox(self.frame_widget, values=["2D", "3D", "Complex", "Parametric"],
                                            width=100, command=self.update_text_box, fg_color='black',
                                            button_color='black', border_color='black',
                                            dropdown_fg_color='black', height=30, corner_radius=0,
                                            button_hover_color='#686868')
        self.combobox_dim.set("2D")
        self.combobox_dim.place(x=300, y=0)

        self.combobox_plot_type = ctk.CTkComboBox(self.frame_widget, values=["Plot", "Scatter", "Surface",
                                                                            "Polar"],
                                            width=100, fg_color='black',
                                            button_color='black', border_color='black',
                                            dropdown_fg_color='black', height=30, corner_radius=0,
                                            button_hover_color='#686868')
        self.combobox_plot_type.set("Plot")
        self.combobox_plot_type.place(x=200, y=0)

        self.real_roots = list()
        self.imaginary_roots = list()

    def update_text_box(self, choice):
        if choice == '2D':
            self.func.configure(placeholder_text='function in term of x')
        elif choice == '3D':
            self.func.configure(placeholder_text='function in term of x and y')
        elif choice == 'Complex':
            self.func.configure(placeholder_text='Complex function in term of x and y')
        else:
            self.func.configure(placeholder_text='Parametric equation')

    def on_click(self):
        self.data.open_secondary_window()

    def plot(self):
        if self.data.check_var_grid.get() == 'True':
            grid = True
        else:
            grid = False

        if self.data.check_var_x.get() == 'True':
            plt.axhline(0, color='black', linewidth=0.5)  # Horizontal line at y=0
        else:
            pass
        if self.data.check_var_y.get() == 'True':
            plt.axvline(0, color='black', linewidth=0.5)  # Vertical line at x=0
        else:
            pass

        # Generate x values for plotting
        x_vals = np.linspace(self.data.x_a_var.get(), self.data.x_b_var.get(),
                            self.data.step_x_var.get())  # Adjust the range and number of points as needed
        y_vals = np.linspace(self.data.y_a_var.get(),
                                  self.data.y_b_var.get(),
                                  self.data.step_y_var.get())  # Adjust the range and number of points as needed

        x_lim = self.data.x_a_var.get(), self.data.x_b_var.get()
        y_lim = self.data.y_a_var.get(), self.data.y_b_var.get()


        if self.combobox_dim.get() == '2D':
            self.plot_2d(grid, x_vals, x_lim, y_lim)
        elif self.combobox_dim.get() == '3D':
            self.plot_3d(grid, x_vals, y_vals)

        elif self.combobox_dim.get() == 'Parametric':
            self.plot_parametric()
        else:
            self.plot_complex()

    def plot_2d(self, grid, x_vals, x_lim, y_lim):
        try:
            y = self.func.get()
            x = sp.symbols('x')

            # Create a lambdify function to convert the equation to a Python function
            equation_func = sp.lambdify(x, y, modules='numpy')

            # Compute y values using the equation function
            y_vals = equation_func(x_vals)

            if self.combobox_plot_type.get() == 'Plot':
                plt.plot(x_vals, y_vals)
            else:
                plt.scatter(x_vals, y_vals)
            plt.xlim(x_lim)
            plt.ylim(y_lim)
            plt.title('Graph of the Function ' + self.func.get())
            plt.xlabel('x')
            plt.ylabel('f(x)')
            plt.grid(grid)
            plt.show()
        except:
            messagebox.showerror("Error", f'Expression {self.func.get()} is not defined.')

        ###########
        # 3D plot #
        ###########
    def plot_3d(self, grid, x_vals, y_vals):
        try:
            z = self.func.get()

            x, y = sp.symbols('x y')

            # Convert the user input into a sympy expression
            expr_xy = sp.sympify(z)

            z_expr = expr_xy

            z_func = sp.lambdify((x, y), z_expr, modules='numpy')

            x, y = np.meshgrid(x_vals, y_vals)

            # Calculate z values using the function
            z = z_func(x, y)

            fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

            # Create 3D scatter plot
            if self.combobox_plot_type.get() == 'Scatter':
                ax.scatter(x, y, z)
            else:
                ax.plot_surface(x, y, z, cmap='viridis')


            # Set labels and title
            ax.set_xlabel('X-axis')
            ax.set_ylabel('Y-axis')
            ax.set_zlabel('Z-axis')
            ax.set_title('3D Surface Plot')
            ax.grid(grid)
            plt.show()
        except:
            messagebox.showerror("Error", f'Expression {self.func.get()} is not defined.')


    def plot_complex(self):
        pass

    def plot_parametric(self):
        # Get the parametric equations from the entry box
        parametric_equation = self.func.get()

        # Split the input equation into x(t) and y(t) parts
        x_eqn, y_eqn = parametric_equation.split(',')

        # Define the parameter and convert entered strings to sympy expressions
        t = sp.symbols('t')
        x_expr = sp.sympify(x_eqn)
        y_expr = sp.sympify(y_eqn)

        # Generate parameter values (t)
        t_values = np.linspace(0, 2 * np.pi, 1000)  # Adjust the range as needed

        # Evaluate x and y expressions for each t value
        x_values = np.array([x_expr.subs(t, val) for val in t_values], dtype=float)
        y_values = np.array([y_expr.subs(t, val) for val in t_values], dtype=float)

        # Plot the parametric curve
        plt.figure(figsize=(6, 6))  # Set figure size
        plt.plot(x_values, y_values, label='Parametric Curve')
        plt.title('Parametric Curve')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.legend()
        plt.grid(True)
        plt.axis('equal')  # Set aspect ratio to equal for better visualization
        plt.show()

    def find_roots(self):
        # Get the polynomial equation with the variable from the entry box
        polynomial_eq = self.func.get()

        # Define the variable symbol
        x = sp.symbols('x')

        try:
            # Create a polynomial object using SymPy's Poly
            poly = sp.Poly(polynomial_eq, x)

            # Extract coefficients from the polynomial
            coefficients = poly.all_coeffs()

            # Find the roots of the polynomial equation
            roots = np.roots(coefficients)
            # Separate real and imaginary roots
            self.real_roots = roots[np.isreal(roots)].real  # Get real parts of real roots
            self.imaginary_roots = roots[np.imag(roots) != 0].imag  # Get imaginary parts of imaginary roots

            # Display the roots in a messagebox
            if len(roots) > 0:
                roots_str = ", ".join([f"{root:.4f}" for root in roots])
                tk.messagebox.showinfo("Roots", f"The roots are: {roots_str}")
            else:
                tk.messagebox.showinfo("No Roots", "No roots found for the given polynomial equation.")
        except Exception as e:
            tk.messagebox.showerror("Error", f"Error in parsing polynomial equation: {e}")


    def mark_roots(self):

        # Plot real roots with circles ('o')
        plt.scatter(self.real_roots, np.zeros_like(self.real_roots), marker='o', color='blue', label='Real Roots')

        # Plot imaginary roots with crosses ('x')
        plt.scatter(np.zeros_like(self.imaginary_roots), self.imaginary_roots, marker='x', color='red', label='Imaginary Roots')

        plt.xlabel('Real')
        plt.ylabel('Imaginary')
        plt.title('Roots on Complex Plane')
        plt.legend()
        plt.grid(True)
        plt.show()

    def plot_derivative(self):
        # Define the variable
        x = sp.symbols('x')

        # Define the function
        y = self.func.get()

        # Calculate the derivative of the function with respect to x
        f_prime = sp.diff(y, x)

        print(f"The derivative of f(x) = {y} is f'(x) = {f_prime}")

        # Create a lambdify function to convert the equation to a Python function
        equation_func = sp.lambdify(x, f_prime, modules='numpy')

        # Compute y values using the equation function
        y_vals = equation_func(self.x_vals)
        plt.plot(self.x_vals, y_vals)

        plt.title(f'Graph of the Function {f_prime}')
        plt.xlabel('x')
        plt.ylabel("f'(x)")

        plt.axhline(0, color='black', linewidth=0.5)  # Horizontal line at y=0
        plt.axvline(0, color='black', linewidth=0.5)  # Vertical line at x=0
        print('here')

        plt.show()



if __name__ == '__main__':
    app = App(darkdetect.isDark())

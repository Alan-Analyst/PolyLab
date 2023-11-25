import customtkinter as ctk


class SettingWindow:
    def __init__(self, root):
        self.root = root
        self.secondary_window_open = False
        self.secondary_window = None
        self.x_a_var = ctk.DoubleVar(value=-5)
        self.x_b_var = ctk.DoubleVar(value=5)
        self.step_x_var = ctk.IntVar(value=100)

        self.y_a_var = ctk.DoubleVar(value=-5)
        self.y_b_var = ctk.DoubleVar(value=5)
        self.step_y_var = ctk.IntVar(value=100)
        self.check_var_grid = ctk.StringVar(value='True')
        self.check_var_x = ctk.StringVar(value='True')
        self.check_var_y = ctk.StringVar(value='True')

    def open_secondary_window(self):

        if not self.secondary_window_open:  # Check if the secondary window is not already open
            self.secondary_window_open = True  # Set the flag to indicate the window is open
            self.secondary_window = ctk.CTkToplevel()
            self.secondary_window.iconbitmap('images/empty.ico')
            self.secondary_window.title('Setting')
            self.secondary_window.geometry('300x400+200+200')
            self.secondary_window.resizable(False, False)
            self.secondary_window.rowconfigure(0, weight=1)
            self.secondary_window.columnconfigure(0, weight=1)

            def on_close():
                self.secondary_window_open = False  # Set the flag to indicate the window is closed
                self.secondary_window.destroy()

            self.secondary_window.protocol('WM_DELETE_WINDOW', on_close)  # Handle window closing
            frame = ctk.CTkFrame(self.secondary_window, fg_color='transparent')
            frame.grid(row=0, column=0, sticky='news', pady=10, padx=10)
            frame.columnconfigure([0, 1, 2, 3, 4], weight=1, uniform='a')

            # x range
            x_a_ent = ctk.CTkEntry(frame, width=50, font=('Verdana', 16), border_width=1, corner_radius=0,
                                   textvariable=self.x_a_var)
            x_a_ent.grid(row=1, column=0, sticky='E')
            x_lbl = ctk.CTkLabel(frame, text='≤ x ≤', font=('Verdana', 16))
            x_lbl.grid(row=1, column=1, sticky='EW')
            x_b_ent = ctk.CTkEntry(frame, width=50, font=('Verdana', 16), border_width=1, corner_radius=0,
                                   textvariable=self.x_b_var)
            x_b_ent.grid(row=1, column=2, sticky='W')
            step_lbl = ctk.CTkLabel(frame, text='Step:', font=('Verdana', 16))
            step_lbl.grid(row=1, column=3, sticky='E', padx=(10, 0))
            step_x_ent = ctk.CTkEntry(frame, width=50, font=('Verdana', 16), border_width=1, corner_radius=0,
                                      textvariable=self.step_x_var)
            step_x_ent.grid(row=1, column=4, sticky='W')

            # y range
            y_a_ent = ctk.CTkEntry(frame, width=50, font=('Verdana', 16), border_width=1, corner_radius=0,
                                   textvariable=self.y_a_var)
            y_a_ent.grid(row=2, column=0, sticky='E')
            b_lbl = ctk.CTkLabel(frame, text='≤ y ≤', font=('Verdana', 16))
            b_lbl.grid(row=2, column=1, sticky='EW')
            y_b_ent = ctk.CTkEntry(frame, width=50, font=('Verdana', 16), border_width=1, corner_radius=0,
                                   textvariable=self.y_b_var)
            y_b_ent.grid(row=2, column=2, sticky='W')
            step_lbl = ctk.CTkLabel(frame, text='Step:', font=('Verdana', 16))
            step_lbl.grid(row=2, column=3, sticky='E', padx=(10, 0))
            step_y_ent = ctk.CTkEntry(frame, width=50, font=('Verdana', 16), border_width=1, corner_radius=0,
                                      textvariable=self.step_y_var)
            step_y_ent.grid(row=2, column=4, sticky='W')

            checkbox_x = ctk.CTkCheckBox(frame, text="X",
                                       variable=self.check_var_x, onvalue="True", offvalue="False", corner_radius=0, width=50)
            checkbox_x.grid(row=3, column=0, sticky='E', pady=10)

            checkbox_y = ctk.CTkCheckBox(frame, text="Y",
                                       variable=self.check_var_y, onvalue="True", offvalue="False", corner_radius=0, width=50)
            checkbox_y.grid(row=3, column=1, sticky='E')
            checkbox_grid = ctk.CTkCheckBox(frame, text="Grid",
                                       variable=self.check_var_grid, onvalue="True", offvalue="False", corner_radius=0, width=50)
            checkbox_grid.grid(row=3, column=2, sticky='W')

        else:
            if self.secondary_window:
                self.secondary_window.lift()  # Bring the existing window to the front



###############################################################################
# option_budgets.py
# 
# Created: 10/19/22
# Creator: Ethan de Leon
# Purposes:
#   - Displays the options for budgets
#   - Option to delete purchase orders
#   - Option to see package assigned
###############################################################################

import tkinter as tk
from tkinter import *
from Backend.database_get import *

from GUI.window_option import *

class BudgetOptionsWindow(OptionWindow):
    def __init__(self, master, **kw):
        super().__init__(master, bg='cyan4', width=400,height=200, **kw)
        self.data = None

    def configure(self):
        button_width = 15
        self.button_frame = tk.Frame(self.frame, bg=self.frame.cget('background'))
        
        self.packages_button = tk.Button(self.button_frame, 
            width=button_width, font=FONT, text='SEE PACKAGES')

        self.delete_button = tk.Button(self.button_frame, bg='red', fg='white',
            width=button_width, font=FONT, text='DELETE PURCHASE ORDER')
        
        self.button_frame.pack(expand=1)

        self.packages_button.grid(row=0, column=0)
        self.delete_button.grid(row=1, column=0)

        return super().configure()

    def display_data(self, data):
        self.data = data
        self.titlelabel.configure(text=self.data[1])
        self.show_window()
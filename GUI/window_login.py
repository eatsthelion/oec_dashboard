
import tkinter as tk
from tkinter import END, messagebox
from Backend.assets import ICON
from GUI.GUI_Mains import FONT
from GUI.window_main import PopupWindow
from Backend.database import DB_connect, EMPLOYEEDB
from Backend.usertoken import UserToken

class LoginWindow(PopupWindow):
    def __init__(self, master, **kw) -> None:
        super().__init__(master, width=400, height=300, bg="#7f007f", **kw)

        master.title('Log into OEC')
        self.hide_back_button()
        self.hide_cancel_button()

        self.entryframe = tk.Frame(self.frame, bg=self.bg)

        self.username_label = tk.Label(self.entryframe, fg='white', bg='#7f007f',
             font=FONT, text='USERNAME:')
        self.password_label = tk.Label(self.entryframe, fg='white', bg='#7f007f',
             font=FONT, text='PASSWORD:')

        self.username_entry = tk.Entry(self.entryframe, font=FONT)
        self.password_entry = tk.Entry(self.entryframe, font=FONT, show='★')

        self.enter_button   = tk.Button(self.entryframe, text='ENTER', font=FONT, 
            command=self.login)

        self.username_label.grid(row=0,column=0, padx = 5, pady=5, sticky=tk.W)
        self.password_label.grid(row=1,column=0, padx = 5, pady=5, sticky=tk.W)
        self.username_entry.grid(row=0,column=1, padx = 5, pady=5)
        self.password_entry.grid(row=1,column=1, padx = 5, pady=5)
        self.enter_button  .grid(row=2,column=0, padx = 5, pady=5, columnspan=2,
            sticky=tk.EW)

        self.frame.pack(fill=tk.BOTH, expand=1)
        self.entryframe.pack(expand=1)

        # Sets up program icon
        self.master.iconbitmap(ICON)

        self.master.geometry('+{}+{}'.format(
            int((self.master.winfo_screenwidth()-self.width)/2),
            int((self.master.winfo_screenheight()-self.height)/2)))

        self.master.bind_all("<Return>", self.login)
        self.username_entry.focus_set()
        

    def login(self, event=None):
        username = self.username_entry.get()
        password = self.password_entry.get()

        user = DB_connect(f'SELECT password FROM users WHERE username = "{username}"',
            database=EMPLOYEEDB)
        
        if len(user)==0: 
            messagebox.showerror('Invalid Login', 'The username or password is incorrect.')
            self.password_entry.delete(0,END)
            return False
        if password != user[0][0]:
            messagebox.showerror('Invalid Login', 'The username or password is incorrect.')
            self.password_entry.delete(0,END)
            return False

        self.parent.user = UserToken(username)

        self.master.unbind_all("<Return>")

        print('Login Successful')
        self.frame.pack_forget()
        self.parent.full_program()

        
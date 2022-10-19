import os
import tkinter as tk
from tkinter import *
from datetime import datetime

from Backend.database import  DB_connect

import GUI.fonts
from GUI.GUI_Mains import FONT
from GUI.main_window import PopupWindow

from Backend.database import PROJECTDB, DB_connect, DB_clean_str


class InsertProjectCommentGUI(PopupWindow):
    def __init__(self, master,parent=None, configure=...) -> None:
        self.master = master
        super().__init__(master, bg='cyan4', configure=self.initial)
        self.parent = parent
        self.width = 500
        self.height=350
        self.data = None

    def initial(self):
        self.titlelabel.configure(text='NEW COMMENT')
        self.entryframe = tk.Frame(self.frame, bg=self.frame.cget('background'))
        self.entryframe.pack(expand=1)
        
        self.textbox = tk.Text(self.entryframe, font=FONT, width=50, height=8)
        self.textbox.pack(expand=1, padx=5)

        enterbutton = tk.Button(self.entryframe, font=FONT, text='ADD COMMENT',
            command=self.enter_comment)

        enterbutton.pack(pady=5)

    def enter_comment(self):
        new_comment = DB_clean_str(self.textbox.get("1.0", END))
        if new_comment == '':
            return False
        tt = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        DB_connect(f"""
            INSERT INTO project_status_log VALUES
            ('{self.data[0]}', '{new_comment}', 'COMMENT', '{tt}', '{tt}',
            '{os.getlogin().upper()}')
            """, database = PROJECTDB)
        self.cancel_window()
        self.parent.searchwindow.resultwindow.refresh_results()
        self.parent.get_latest_comment()
        self.parent.get_latest_status()

    def show_window(self):
        self.textbox.delete('1.0', END)
        return super().show_window()
import tkinter as tk
from tkinter import *
from tkinter import messagebox, filedialog

from Backend.database import DB_clean_str

from GUI.GUI_Mains import FONT
from GUI.widgets.highlight import enter_leave_stylechange


class MyFrame(tk.Frame):
    def __init__(self, master, bg=None, **kw) -> None:
        if bg == None:
            bg = master.cget('background')
        super().__init__(master, bg=bg, **kw)
        return

class MyLabel(tk.Label):
    def __init__(self, master, bg=None, font=FONT, **kw) -> None:
        if bg == None:
            bg = master.cget('background')
        super().__init__(master, font=font, bg=bg, **kw)
        return

class MyLabelFrame(tk.LabelFrame):
    def __init__(self, master, bg=None, font=FONT, **kw) -> None:
        if bg == None:
            bg = master.cget('background')
        super().__init__(master, font=font, bg=bg, **kw)
        return

class MyButton(tk.Button):
    def __init__(self, master, font=FONT, enterstyle='underline', **kw) -> None:
        super().__init__(master, font=font, cursor='hand2', relief = 'flat',**kw)
        enter_leave_stylechange(self, enter=enterstyle)
        return

class MyText(tk.Text):
    def __init__(self, master, font=FONT, **kw) -> None:
        super().__init__(master, font=font, wrap='word', **kw)
        return

    def get(self, stindx='1.0', endindx=END) -> str:
        return DB_clean_str(super().get(stindx, endindx))

    def delete(self, stindx='1.0', endindx=END) -> None:
        return super().delete(stindx, endindx)

    def insert(self, chars: str, index='1.0') -> None:
        return super().insert(index, str(chars))

class MyEntry(tk.Entry):
    def __init__(self, master, font=FONT, value:str=None, **kw) -> None:
        self.strvar = tk.StringVar()
        if value!=None:
            self.strvar.set(value)
        super().__init__(master, textvariable=self.strvar, font=font, **kw)
        return

    def get(self) -> str:
        return DB_clean_str(super().get())

    def delete(self, stindx=0, endindx=END) -> None:
        return super().delete(stindx,endindx)

    def insert(self, string: str, index=0) -> None:
        return super().insert(index, string)

    def set(self, value:str) -> None:
        self.strvar.set(value)
        return

class MyOptionMenu(tk.OptionMenu):
    def __init__(self, master, values, font=FONT, **kw) -> None:
        self.values = values
        self.strvar = tk.StringVar(value=self.values[0])
        super().__init__(master, self.strvar , *values, **kw)
        self.config(indicatoron=0, cursor='hand2', bg='white',
            font=font, relief='flat')
        self.menu = master.nametowidget(self.menuname)
        self.menu.config(font=FONT)
        return

    def get(self) -> str:
        return DB_clean_str(self.strvar.get())

    def set(self, value:str) -> None:
        self.strvar.set(value)
        return

    def delete(self) -> None:
        self.strvar.set(self.values[0])
        return

class MyCanvas(tk.Canvas):
    def __init__(self, master, bg=None, highlightthickness=0, **kw) -> None:
        if bg == None:
            bg = master.cget('background')
        super().__init__(master, bg=bg, highlightthickness=highlightthickness,
            **kw)
        return

class MyScrollbar(tk.Scrollbar):
    def __init__(self, master, **kw) -> None:
        super().__init__(master, **kw)
import tkinter as tk
from tkinter import *

from GUI.widgets.basics import *
from GUI.widgets.highlight import rowhighlight
from GUI.main_window import PopupWindow

class Terminal(MyFrame):
    def __init__(self, master, font=FONT, dimensions=(60,6), 
        scroll_bar=False, **kw) -> None:
        self.shadow_frame = MyFrame(master, bg='black')
        super().__init__(master, **kw)
        
        self.terminal = MyText(self, state=DISABLED, width=dimensions[0], 
            height=dimensions[1], font=font)
        
        if scroll_bar:
            scrollbar = MyScrollbar(self, orient='vertical')
            self.terminal.configure(yscrollcommand=scrollbar.set)
            scrollbar.config(command=self.terminal.yview)
            scrollbar.pack(side='right', fill='y', padx=(0,5), pady=10)
            self.terminal.pack(padx=(10,0), pady=10, anchor=N)
        else:
            self.terminal.pack(padx=10, pady=10, anchor=N)

    def print_terminal(self, text):
        self.terminal.configure(state=NORMAL)
        self.terminal.delete()
        self.terminal.insert(text)
        self.terminal.configure(state=DISABLED)
        self.master.update()
    
    def hide_terminal(self):
        self.place_forget()
        self.shadow_frame.place_forget()
        self.terminal.configure(state=NORMAL)
        self.terminal.delete()
        self.terminal.configure(state=DISABLED)
        self.terminal.grab_release()

    def show_terminal(self):
        self.place(relx=.5, rely=.5, height=150, width=400, anchor=CENTER)
        self.shadow_frame.place(relx=.505, rely=.51, height=150, width=400, 
            anchor=CENTER)
        self.terminal.grab_set()
        pass

class TerminalWindow(PopupWindow):
    def __init__(self, master, width=600, height=300, bg='gray60', 
        scroll_bar = True, font = (FONT[0], 18),**kw) -> None:
        super().__init__(master, width=width, height=height, bg=bg, **kw)
        self.data = None
        self.origin_widget = None
        self.terminal = Terminal(self.frame, bg=self.bg, dimensions=(60,10),
            font = font, scroll_bar=scroll_bar)
        self.terminal.pack(padx=10,pady=10)
        
    def cancel_window(self):
        rowhighlight(None, self.origin_widget, 'white', 'white')
        return super().cancel_window()
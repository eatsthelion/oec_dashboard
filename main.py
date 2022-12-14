import tkinter as tk
from tkinter import *

import sys
sys.dont_write_bytecode = True

class MainProgram(object):
    def __init__(self, root):
        # Initializes program settings
        from GUI.window_login import LoginWindow
        self.root = root
        self.user = None
        self.parent=None
        self.children = []
        self.current_program = LoginWindow(self.root, parent=self)
        
    def full_program(self):
        self.width = 1280
        self.height = 700
        self.bg = "#7f007f"
        self.font = ('helvetica', 20, 'bold')
        self.root.title('OEC Dashboard')
        self.root.resizable(1,1)
        self.root.minsize(self.width, self.height)
        self.root.geometry('+{}+{}'.format(
            int((self.root.winfo_screenwidth()-self.width)/2),
            int((self.root.winfo_screenheight()-self.height)/2)))

        # Fullscreen button binding  
        self.fullscreen = False
        self.root.bind("<F11>", self.fullscreen_command)

        # Initializes main program frame
        self.mainframe = tk.Frame(self.root, bg=self.bg)
        self.mainframe.pack(fill=BOTH, expand=1)

        # Initializes Loading Screen
        self.l_frame = tk.Frame(self.mainframe, bg=self.bg)
        self.l_frame.place(x=0, y=0, relwidth=1, relheight=1, anchor=NW)
        self.load_text = tk.Label(self.l_frame, fg='white', bg=self.bg, 
            font = self.font, text='LOADING\nDASHBOARD', width = 20)
        self.star_txt_left = tk.Label(self.l_frame, fg='white', bg=self.bg, 
            font = self.font, text='')
        self.star_txt_right = tk.Label(self.l_frame, fg='white', bg=self.bg, 
            font = self.font, text='')
        self.star_txt_left .pack(side=LEFT, expand=1,anchor=E)
        self.load_text.pack(side=LEFT,anchor=CENTER, padx=30)
        self.star_txt_right.pack(side=LEFT, expand=1,anchor=W)
        self.root.update()
        self.load_text.configure(text='LOADING\nASSETS')
        self.star_txt_right.configure(text='★')
        self.star_txt_left.configure(text='★')
        self.root.update()

        # Loads Program Assets
        from GUI.GUI_Mains import FONT, FONTBOLD
        
        self.font = FONT
        self.load_text.configure(font=FONTBOLD, text = 'LOADING\nFILES')
        self.star_txt_right.configure(text='★ ★ ★')
        self.star_txt_left.configure(text='★ ★ ★')
        self.star_txt_right.configure(font=FONTBOLD)
        self.star_txt_left .configure(font=FONTBOLD)
        self.root.update()

        self.load_text.configure(text = 'LOADING\nFILES')
        self.root.update()

        # Destroys the previous loaded program
        if self.current_program != None:
            self.current_program.frame.destroy()
            del self.current_program
        self.load_text.configure(text = "LOADING\nOEC DASHBOARD")
        self.star_txt_right.configure(text='★ ★ ★ ★ ★')
        self.star_txt_left.configure(text='★ ★ ★ ★ ★')
        self.root.update()

        from GUI.window_home import HomeWindow
        self.current_program = HomeWindow(self.mainframe, parent=self)
        self.root.title("OEC Dashboard")

        # Changes windows to display
        self.current_program.show_full_window()
        self.l_frame.place_forget()
    
    def fullscreen_command(self, event):
        if self.fullscreen == False:
            self.root.attributes('-fullscreen',True)
            self.fullscreen = True
        else: 
            self.root.attributes('-fullscreen',False)
            self.fullscreen = False

    def raise_loading_screen(self, load_text:str = 'LOADING'):
        self.l_frame.tkraise(aboveThis=None)
        self.l_frame.place(x=0, y=0, relwidth=1, relheight=1, anchor=NW)
        self.load_text.configure(text=load_text)
        self.star_txt_right.configure(text='★ ★ ★ ★ ★')
        self.star_txt_left.configure(text='★ ★ ★ ★ ★')
        self.root.update()

    def lower_loading_screen(self):
        self.l_frame.place_forget()
        self.root.update()

def main() -> None:
    root = tk.Tk()
    root.resizable(0,0)
    root.configure(bg="#7f007f")
    root.title("OEC Dashboard")
    load_label = tk.Label(root, font=('montserrat', 16,'bold'), 
        text="LOADING",bg="#7f007f", fg='white')

    root.geometry('360x130+{}+{}'.format(
            int((root.winfo_screenwidth()-400)/2),
            int((root.winfo_screenheight()-300)/2)))
    load_label.place(relx=.5, rely=.5, anchor=CENTER)
    root.update()
    MainProgram(root)
    load_label.place_forget()
    tk.mainloop()

if __name__=='__main__':
    main()
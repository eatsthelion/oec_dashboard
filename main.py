import tkinter as tk
from tkinter import *

from GUI.login_window import LoginWindow

START = 'OEC Project Catalog'
PROGRAMS = ['Switch Programs', 'OEC Taskboard', 'OEC Project Catalog', 
    'OEC Schedule', 'OEC Budget Catalog', 'OEC Material Database', 
    'OEC Staff', ]

class MainProgram(object):
    def __init__(self):
        # Initializes program settings
        self.root = tk.Tk()
        self.root.resizable(0,0)
        self.user = None
        self.parent=None
        self.children = []
        self.current_program = LoginWindow(self.root, parent=self)
        
        tk.mainloop()

    def full_program(self):
        self.width = 1280
        self.height = 720
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
        import GUI.fonts
        from GUI.GUI_Mains import FONT, FONTBOLD
        
        self.font = FONT
        self.load_text.configure(font=FONTBOLD, text = 'LOADING\nFILES')
        self.star_txt_right.configure(text='★ ★ ★')
        self.star_txt_left.configure(text='★ ★ ★')
        self.star_txt_right.configure(font=FONTBOLD)
        self.star_txt_left .configure(font=FONTBOLD)
        self.root.update()

        self.switch_catalog(START)

    def switch_catalog(self, program_name):
        self.load_text.configure(text = 'LOADING\nFILES')
        self.root.update()
        if program_name == 'OEC Project Catalog':
            from Backend.database_get import get_project_info
            from GUI.catalogs.catalog_projects import ProjectCatalog
            db_function = get_project_info
            catalog = ProjectCatalog
        elif program_name == 'OEC Material Database':
            from Backend.database_get import get_material_info
            from GUI.catalogs.catalog_materials import MaterialDatabase
            db_function = get_material_info
            catalog = MaterialDatabase
        elif program_name == 'OEC Schedule':
            from Backend.database_get import get_oec_date_catalog
            from GUI.catalogs.catalog_project_dates import ProjectDates
            db_function = get_oec_date_catalog
            catalog = ProjectDates
        elif program_name == 'OEC Budget Catalog':
            from Backend.database_get import get_budget_catalog
            from GUI.catalogs.catalog_budgets import BudgetCatalog
            db_function = get_budget_catalog
            catalog = BudgetCatalog
        elif program_name == 'OEC Staff':
            from Backend.database_get import get_active_employees
            from GUI.catalogs.catalog_users import EmployeeDatabase
            db_function = get_active_employees
            catalog = EmployeeDatabase
        elif program_name == 'OEC Taskboard':
            from Backend.database_get import get_taskboard
            from GUI.catalogs.catalog_taskboard import Taskboard
            db_function = lambda: get_taskboard(self.user.user_id)
            catalog = Taskboard
        elif program_name == 'Excel Comparison':
            from other_programs.excel_file_comparison import ExcelComparer
            db_function = None
            catalog = BudgetCatalog
        # Raises the Loading Screen
        self.l_frame.tkraise(aboveThis=None)
        self.l_frame.place(x=0, y=0, relwidth=1, relheight=1, anchor=NW)

        # Destroys the previous loaded program
        if self.current_program != None:
            self.current_program.frame.destroy()
            del self.current_program
        self.load_text.configure(text = "LOADING\n{}"
            .format(program_name.upper()))
        self.star_txt_right.configure(text='★ ★ ★ ★ ★')
        self.star_txt_left.configure(text='★ ★ ★ ★ ★')
        self.root.update()
        
        self.current_program = catalog(self.mainframe, parent=self)
        self.current_program.display_data(None, lambda: db_function())
        self.root.title(self.current_program.program_title)

        # Changes windows to display
        from GUI.widgets.basics import MyOptionMenu
        self.current_program.show_full_window()
        self.l_frame.place_forget()

        self.programOptions = MyOptionMenu(self.current_program.frame, PROGRAMS,
            command=self.menu_command)
        
        self.programOptions.place(x=0, y=0, anchor=NW)

    def menu_command(self, event):
        program = self.programOptions.get()
        if program == 'Switch Programs':
            return
        self.switch_catalog(program)
    
    def fullscreen_command(self, event):
        if self.fullscreen == False:
            self.root.attributes('-fullscreen',True)
            self.fullscreen = True
        else: 
            self.root.attributes('-fullscreen',False)
            self.fullscreen = False

    

if __name__=='__main__':
    MainProgram()
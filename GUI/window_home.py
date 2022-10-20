from GUI.window_main import *
from GUI.widgets.textscroller import TextScroller
from Backend.database_get import *

class HomeWindow(PopupWindow):
    def __init__(self, master: tk, **kw) -> None:
        super().__init__(master, **kw)
        self.menubar = None
        self.hide_back_button()
        self.hide_cancel_button()
        self.titlelabel.configure(font = ("montserrat extrabold",24,'bold'), 
            text="★ OEC DASHBOARD ★", bg='white',
            height=2)
        self.titlelabel.place_forget()
        self.titlelabel.pack(fill='x')

    def configure(self):
        self.text_scroller = TextScroller(self.frame, height = 50, 
            user = self.user.first_name)
        self.button_frame = MyFrame(self.frame)
        bwidth = 20
        self.project_catalog_button = MyButton(self.button_frame, width=bwidth,
            font=(FONT[0],18), text='Project Catalog', command = lambda:
                self.switch_windows('project catalog'))
        self.material_database_button = MyButton(self.button_frame, width=bwidth,
            font=(FONT[0],18), text='Materials Database',command = lambda: 
                self.switch_windows('mat db'))
        self.taskboard_button = MyButton(self.button_frame, width=bwidth,
            font=(FONT[0],18), text='Taskboard', command = lambda:
                self.switch_windows('taskboard'))
        self.staff_button = MyButton(self.button_frame, width=bwidth,
            font=(FONT[0],18), text='Staff', command = lambda:
                self.switch_windows('staff'))

        self.project_catalog_button.grid(row=0, column=0, padx=5, pady=5, 
            sticky=EW)
        self.taskboard_button.grid(row=0, column=1, padx=5, pady=5, sticky=EW)
        self.material_database_button.grid(row=1, column=0, padx=5, pady=5, 
            sticky=EW)
        self.staff_button.grid(row=1, column=1, padx=5, pady=5, sticky=EW)
        self.text_scroller.pack(fill='x')
        self.button_frame.pack(padx=5, pady=5, expand=1)
        
        super().configure()
        self.text_scroller.start()
        self.scroller_binds()

    def scroller_binds(self):
        self.mainprogram.root.bind("<space>", self.text_scroller.pause)
        self.mainprogram.root.bind("<KeyPress-Right>", self.text_scroller.fastforward)
        self.mainprogram.root.bind("<KeyRelease-Right>", self.text_scroller.normal_speed)

    def switch_windows(self, program_name):
        """Switches displays to a new program"""
        # Imports all the programs 
        from Programs.catalog_projects import ProjectCatalog
        from Programs.catalog_materials import MaterialDatabase
        from Programs.catalog_project_dates import ProjectDates
        from Programs.catalog_budgets import BudgetCatalog
        from Programs.catalog_users import EmployeeDatabase
        from Programs.catalog_taskboard import Taskboard
        from Misc.excel_file_comparison import ExcelComparer

        self.mainprogram.raise_loading_screen()
        self.text_scroller.stop()
        self.mainprogram.root.unbind("<space>")
        self.mainprogram.root.unbind("<KeyPress-Right>")
        self.mainprogram.root.unbind("<KeyRelease-Right>")

        # removes existing programs
        for child in self.mainprogram.children:
            if child == self:
                continue
            try: 
                child.go_back()
            except:
                pass

        # determines the next program to be displayed
        if program_name == 'project catalog':
            db_function = get_project_info
            catalog = ProjectCatalog
        elif program_name == 'mat db':
            db_function = get_material_info
            catalog = MaterialDatabase
        elif program_name == 'OEC Schedule':
            from Backend.database_get import get_oec_date_catalog
            db_function = get_oec_date_catalog
            catalog = ProjectDates
        elif program_name == 'OEC Budget Catalog':
            from Backend.database_get import get_budget_catalog
            db_function = get_budget_catalog
            catalog = BudgetCatalog
        elif program_name == 'staff':
            from Backend.database_get import get_active_employees
            db_function = get_active_employees
            catalog = EmployeeDatabase
        elif program_name == 'taskboard':
            from Backend.database_get import get_taskboard
            db_function = lambda: get_taskboard(self.user.user_id)
            catalog = Taskboard
        elif program_name == 'Excel Comparison':
            db_function = None
            catalog = ExcelComparer
        
        # Creates the next program
        current_program = catalog(self.master, parent=self.mainprogram)
        current_program.display_data(None, lambda: db_function())
        self.add_menubar(current_program)
        current_program.show_full_window()
        current_program.back_direction=self.show_full_window
        self.cancel_window()

        self.mainprogram.lower_loading_screen()

    def add_menubar(self, program:object) -> None:
        """Adds a menubar to the window
        program: The window that is displayed. Additional menu options can be added
        with the program object's "self.additional_menu_options" function
        """
        self.menubar = Menu(self.parent.root, tearoff=False)
        self.parent.root.config(menu=self.menubar)
        catalog_menu = Menu(self.menubar, tearoff=False)
        catalog_menu.add_command(label = 'Home',
            command = self.go_back_home)
        catalog_menu.add_command(label='Project Catalog',
            command = lambda: self.switch_windows('project catalog'))
        catalog_menu.add_command(label='Taskboard',
            command = lambda: self.switch_windows('taskboard'))
        catalog_menu.add_command(label='Material Database',
            command = lambda: self.switch_windows('mat db'))
        program.additional_menu_options(self.menubar)

        self.menubar.add_cascade(label='Navigation', menu=catalog_menu)

    def show_full_window(self) -> None:
        """Removes the menubar and returns to home window"""
        if self.menubar != None:
            self.menubar.destroy()
        self.mainprogram.lower_loading_screen()
        return super().show_full_window()

    def go_back_home(self) -> None:
        """Removes all open programs and returns to the home menu"""
        self.mainprogram.raise_loading_screen()
        for child in self.mainprogram.children:
            if child == self:
                continue
            try: 
                child.go_back()
            except:
                pass
        self.text_scroller.start()
        self.scroller_binds()
        self.show_full_window()

if __name__ == '__main__':
    from GUI.test_gui import TestGUI
    test = TestGUI(HomeWindow)
from GUI.window_main import *

from Backend.database_get import *
from Programs.catalog_projects import ProjectCatalog
from Programs.catalog_materials import MaterialDatabase

class HomeWindow(PopupWindow):
    def __init__(self, master: tk, **kw) -> None:
        super().__init__(master, **kw)
        self.menubar = None
        self.hide_back_button()
        self.hide_cancel_button()

    def configure(self):
        self.button_frame = MyFrame(self.frame)
        bwidth = 20
        self.project_catalog_button = MyButton(self.button_frame, width=bwidth,
            text='Project Catalog', command = lambda:
                self.switch_windows('project catalog'))
        self.material_database_button = MyButton(self.button_frame, width=bwidth,
            text='Materials Database',command = lambda: 
                self.switch_windows('mat db'))
        self.taskboard_button = MyButton(self.button_frame, width=bwidth,
            text='Taskboard', command = lambda:
                self.switch_windows('taskboard'))
        self.staff_button = MyButton(self.button_frame, width=bwidth,
            text='Staff', command = lambda:
                self.switch_windows('staff'))

        self.project_catalog_button.grid(row=0, column=0, padx=5, pady=5, 
            sticky=EW)
        self.taskboard_button.grid(row=0, column=1, padx=5, pady=5, sticky=EW)
        self.material_database_button.grid(row=1, column=0, padx=5, pady=5, 
            sticky=EW)
        self.staff_button.grid(row=1, column=1, padx=5, pady=5, sticky=EW)
        self.button_frame.pack(padx=5, pady=5, expand=1)
        return super().configure()

    def switch_windows(self, program_name):
        self.mainprogram.raise_loading_screen()
        for child in self.mainprogram.children:
            if child == self:
                continue
            try: 
                child.go_back()
            except:
                pass
    
        if program_name == 'project catalog':
            db_function = get_project_info
            catalog = ProjectCatalog
        elif program_name == 'mat db':
            db_function = get_material_info
            catalog = MaterialDatabase
        elif program_name == 'OEC Schedule':
            from Backend.database_get import get_oec_date_catalog
            from Programs.catalog_project_dates import ProjectDates
            db_function = get_oec_date_catalog
            catalog = ProjectDates
        elif program_name == 'OEC Budget Catalog':
            from Backend.database_get import get_budget_catalog
            from Programs.catalog_budgets import BudgetCatalog
            db_function = get_budget_catalog
            catalog = BudgetCatalog
        elif program_name == 'staff':
            from Backend.database_get import get_active_employees
            from Programs.catalog_users import EmployeeDatabase
            db_function = get_active_employees
            catalog = EmployeeDatabase
        elif program_name == 'taskboard':
            from Backend.database_get import get_taskboard
            from Programs.catalog_taskboard import Taskboard
            db_function = lambda: get_taskboard(self.user.user_id)
            catalog = Taskboard
        elif program_name == 'Excel Comparison':
            from Misc.excel_file_comparison import ExcelComparer
            db_function = None
            catalog = BudgetCatalog
        # Raises the Loading Screen
        current_program = catalog(self.master, parent=self.mainprogram)
        current_program.display_data(None, lambda: db_function())
        self.add_menubar(current_program)
        current_program.show_full_window()
        current_program.back_direction=self.show_full_window
        self.cancel_window()
        self.mainprogram.lower_loading_screen()

    def add_menubar(self, program):
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

    def show_full_window(self):
        if self.menubar != None:
            self.menubar.destroy()
        return super().show_full_window()

    def go_back_home(self):
        print(self.mainprogram.children)
        for child in self.mainprogram.children:
            if child == self:
                continue
            try: 
                child.go_back()
            except:
                pass
        self.show_full_window()

if __name__ == '__main__':
    from GUI.test_gui import TestGUI
    test = TestGUI(HomeWindow)
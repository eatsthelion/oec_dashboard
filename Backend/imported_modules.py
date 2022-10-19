
class importer(object):
    def __init__(self, terminal) -> None:
        self.terminal= terminal
        pass

    def start(self):
        
        self.update_terminal('OS')
        import os
        self.update_terminal('EXCEL\nFUNCTIONALITY')
        from Backend.exports import export_init
        import openpyxl
        from openpyxl.utils import get_column_letter
        from openpyxl.styles import PatternFill, Border, Side, Alignment, \
            Protection, Font
        import pandas as pd
        from datetime import datetime
        
        self.update_terminal('DATABASE\nCONNECTIONS')

        self.update_terminal('FILING SYSTEM')
        from Backend.filesystem import FileSystem
        from Backend.path_analyzer import PathAnalyzer
        self.update_terminal('GUI')
        
        self.update_terminal('PROJECTS')
        self.update_terminal
        self.update_terminal('CONTACTS')
        self.update_terminal('TASK ASSIGNMENTS')


        del self

    def update_terminal(self, update):
        self.terminal.configure(text= 'IMPORTING\n'+update)
        self.terminal.update()

from GUI.widgets.new_search_window import SearchWindow
from GUI.GUI_Mains import *

import GUI.fonts
from GUI.widgets.terminal import *

from GUI.project_catalog.option_windows.project_options  import ProjectOptionsWindow
from GUI.project_catalog.project_budgets        import ProjectBudgetsGUI
from GUI.project_catalog.project_status_log     import ProjectStatusGUI
from GUI.project_catalog.project_schedule       import ProjectScheduleGUI
from GUI.project_catalog.project_assignments    import ProjectAssignmentsGUI
from GUI.project_catalog.project_documents      import ProjectDocumentsGUI
from GUI.project_catalog.project_packages       import ProjectPackagesGUI
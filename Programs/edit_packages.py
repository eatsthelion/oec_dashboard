###############################################################################
# edit_packages.py
# 
# Created: 8/02/22
# Creator: Ethan de Leon
# Purposes: 
#   - GUI for both inserting and modifying packages
###############################################################################

PROGRAMTITLE = 'Package Edits'
import os
from datetime import datetime
from Backend.database import  DBTIME,  PACKAGEDB, USERTIME, DB_connect
from Backend.filesystem import FileSystem
from Backend.database_send import project_edit_entry, project_input_entry

from GUI.window_edit import *

class EditPackagesGUI(EditWindow):
    def __init__(self, master, **kw) -> None:
        super().__init__(master, bg='cyan4',width=600,height=400, 
        program_title = PROGRAMTITLE, **kw)
        self.data = None
        self.project_id = None
        self.event_id = ''

    def configure(self):
        ew = 25
        self.entryframe = MyFrame(self.frame, bg=self.bg)
        self.name_entry = MyEntry(self.entryframe, width=ew)
        self.desc_entry = MyText(self.entryframe, width=ew, height=3)
        self.type_entry = MyEntry(self.entryframe, width=ew)
        self.forecast_entry = DateEntry(self.entryframe)
        self.actual_entry = DateEntry(self.entryframe)

        self.datapairs = [
            ("Package Name*:",self.name_entry,'name'),
            ("Description:", self.desc_entry,'description'), 
            ("Package Type*:", self.type_entry,'type'),
            ("Forecast Submittal Date:", self.forecast_entry,
                'forecast_date'),
            ("Actual Submittal Date", self.actual_entry, 
                'submittal_date'),
        ]

        for row, datapair in enumerate(self.datapairs):
            label = MyLabel(self.entryframe, text=datapair[0])
            label.grid(row=row, column=0, padx=5, pady=(5,0), sticky=W)
            datapair[1].grid(row=row, column = 1, padx=5, pady=(5,0), sticky=EW)
        
        self.entryframe.pack(expand=1, pady=(0,5), padx=5)

        self.enterbutton = MyButton(self.frame, command=self.enter_command)
        self.enterbutton.pack(fill='x', padx=5, pady=5)
        return super().configure()

    def enter_command(self) -> None:
        name = self.name_entry.get()
        desc = self.desc_entry.get()
        p_type = self.type_entry.get().upper()
        fore = self.forecast_entry.get()
        actl = self.actual_entry.get()

        if self.context == 'insert':
            # Checks if there isn't a package of the same name in the project
            same_package = DB_connect(f"""
                SELECT rowid
                FROM packages
                WHERE project_id = {self.project_id} and name = '{name}'""",
                database = PACKAGEDB)
            if len(same_package)>0:
                messagebox.showerror("Same Named Package",
                    "A package of the same name already exists for this project.")
                return False

            status_updates = f"Package {name} was created.\n" + \
                f"{name} has the package type of {p_type}\n"

            if desc!='':
                status_updates+=f"{name} has the description of '{desc}'\n"
            if fore!='':
                fd = fore.strftime(USERTIME)
                fore = fore.strftime(DBTIME)
                status_updates+=f"{name} has a forecast date on {fd}\n"
            if actl!='':
                ad = actl.strftime(USERTIME)
                actl = actl.strftime(DBTIME)
                status_updates+=f"{name} has a actual date on {ad}\n"

            sql_str = f"""'{self.project_id}','{self.event_id}','','1','{name}',
                '{desc}','{p_type}','{fore}','{actl}'"""
            
            project_input_entry(self.project_id, 'packages', PACKAGEDB, sql_str,
                status_updates, 'NEW PACKAGE', user = self.user)

            rid = DB_connect("SELECT MAX(rowid) FROM packages", 
                database = PACKAGEDB)[0][0]
            os.mkdir(FileSystem.get_package_folder(rid))
            self.parent.searchwindow.refresh_page()

        elif self.context == 'modify':
            # Validates if the new name already exists in the project or not
            if name!= self.data[1]:
                same_package = DB_connect(f"""
                    SELECT rowid
                    FROM packages
                    WHERE project_id = {self.project_id} and name = '{name}'""",
                    database = PACKAGEDB)
                if len(same_package)>0:
                    messagebox.showerror("Same Named Package",
                        "A package of the same name already exists for this project.")
                    return False
            datapairs = [
                (name, 'name', 'name'),
                (desc, 'description', 'description'),
                (p_type, 'package type', 'type')
            ]

            datelist = [
                (self.data[7], self.forecast_entry,  'proposal submittal', 
                    'proposed_date'),
                (self.data[8], self.actual_entry,  'contract submittal',
                    'contract_date')
            ]

            past_path = FileSystem.get_package_folder(self.data[0])
            project_edit_entry(self.project_id, self.data[0], 'packages', 
                PACKAGEDB, name, 'PACKAGE EDIT', self.data, self.data_dict,
                datapairs, datelist, 
                user=self.user)
            os.rename(past_path, FileSystem.get_package_folder(self.data[0]))
            self.parent.searchwindow.refresh_page()

        self.cancel_window()
        
        return

    def display_data(self, project_id:int, data:tuple=None, 
        event_id:int='') -> None:

        self.name_entry.delete()
        self.desc_entry.delete()
        self.type_entry.delete()
        self.forecast_entry.delete()
        self.actual_entry.delete()

        self.data = data
        self.project_id = project_id
        self.event_id = event_id

        if data==None:
            self.context = "insert"
            self.titlelabel.configure(text='NEW PACKAGE')
            self.enterbutton.configure(text='ADD PACKAGE')
            
            self.show_window() 
            return
        
        self.context = "modify"
        self.titlelabel.configure(text='EDIT PACKAGE')
        self.enterbutton.configure(text='SAVE CHANGES')
        
        self.name_entry.insert(self.get_data('name'))
        self.desc_entry.insert(self.get_data('description'))
        self.type_entry.insert(self.get_data('type'))

        try:            
            self.forecast_entry.insert(datetime.strptime(self.get_data('forecast_date'), DBTIME))
        except:
            pass
        try:
            self.actual_entry.insert(datetime.strptime(self.get_data('submittal_date'), DBTIME))
        except:
            pass
        
        self.show_window()
        return


    
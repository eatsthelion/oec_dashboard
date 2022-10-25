PROGRAMTITLE = 'Project Edits'
import os
from datetime import datetime

from Backend.database import  DB_connect, PROJECTDB
from Backend.database_send import project_edit_entry, project_input_entry
from Backend.filesystem import FileSystem

from GUI.window_edit import *

class EditProjectGUI(EditWindow):
    def __init__(self, master, **kw) -> None:
        super().__init__(master, bg='mediumorchid1', 
        program_title = PROGRAMTITLE, **kw)
        self.data = None

    def configure(self):
        self.canvas_show()
        self.canvas_window.h_scroll_hide()
        self.entryframe = MyFrame(self.canvasframe, bg=self.bg)
        self.entryframe.pack(expand=1, pady=5)
        
        self.folder_frame = MyLabelFrame(self.entryframe,
            text='Update via Report File')
        self.folder_entry = MyEntry(self.folder_frame, state=DISABLED,
            disabledbackground='white')
        self.folder_label = MyLabel(self.folder_frame, text='Report File:')
        self.folder_btton = MyButton(self.folder_frame,text='SELECT')
        self.update_btton = MyButton(self.folder_frame,text='UPDATE')

        self.folder_label.grid(row=0,column=0, sticky=NSEW, padx=(5,0))
        self.folder_entry.grid(row=0,column=1, padx=(5,0), sticky=NS)
        self.folder_btton.grid(row=0,column=2, padx=5)
        self.update_btton.grid(row=1,column=0, pady=5, padx=5, columnspan=3,
            sticky=EW)

        self.active_statuses = ['ACTIVE', 'COMPLETED', 'ON HOLD', 'CANCELLED']
        self.active_status_label = MyLabel(self.entryframe, text='Active Status:')
        self.active_status_options = MyOptionMenu(self.entryframe, 
            self.active_statuses)

        self.oec_entry_label = MyLabel(self.entryframe, text='OEC No*:')
        self.progress_label = MyLabel(self.entryframe, text='Progress(%):')
        self.phase_label = MyLabel(self.entryframe, text='Phase:')
        self.stage_label = MyLabel(self.entryframe, text='Stage:')
        self.title_entry_label = MyLabel(self.entryframe, text='Project Title*:')
        self.client_label = MyLabel(self.entryframe, text='Client*:')
        self.active_label = MyLabel(self.entryframe, text='Active Status:')
        self.client_job_label = MyLabel(self.entryframe, text='Client Job #:')
        self.location_label = MyLabel(self.entryframe, text='Location*:')
        self.project_type_label = MyLabel(self.entryframe, text='Project Type:')

        ew=25
        self.oec_entry = MyEntry(self.entryframe, width=ew)
        self.progress_entry = MyEntry(self.entryframe, width=ew)
        self.phase_entry = MyEntry(self.entryframe, width=ew)
        self.stage_entry = MyEntry(self.entryframe, width=ew)
        self.title_entry = MyEntry(self.entryframe, width=ew)
        self.client_entry = MyEntry(self.entryframe, width=ew)
        self.client_job_entry = MyEntry(self.entryframe,  width=ew)
        self.location_entry = MyEntry(self.entryframe, width=ew)
        self.project_type_entry = MyEntry(self.entryframe)
        
        self.enterbutton = MyButton(self.frame, command=self.enter_command)
        self.enterbutton.pack(pady=10, fill='x', padx=10)
        self.canvas_window.v_scroll_pack()
        
        super().configure()
    
    def widget_placement(self):
        widget_pairings = [
            (self.oec_entry_label, self.oec_entry),
            (self.title_entry_label, self.title_entry),
            (self.client_job_label, self.client_job_entry),
            (self.active_label, self.active_status_options),
            (self.progress_label, self.progress_entry),
            (self.stage_label, self.stage_entry),
            (self.phase_label, self.phase_entry),
            (self.client_label, self.client_entry),
            (self.location_label, self.location_entry),
            (self.project_type_label, self.project_type_entry)
        ]

        skipwidgets = [(self.active_label, self.active_status_options),
            (self.progress_label, self.progress_entry),
            (self.stage_label, self.stage_entry),
            (self.phase_label, self.phase_entry),]

        for row, pair in enumerate(widget_pairings):
            if (self.context =='insert') and (pair in skipwidgets):
                continue
            pair[0].grid(row = row + 1, column = 0, padx =(35, 5), sticky = W)
            pair[1].grid(row = row + 1, column = 1, padx =(5, 10), pady=5, 
                sticky = EW)

    def enter_command(self):
        oec_number =      self.oec_entry.get()
        title =           self.title_entry.get()
        client_job =      self.client_job_entry.get()
        client =          self.client_entry.get()
        project_type =    self.project_type_entry.get()
        location =        self.location_entry.get()
        progress =        self.progress_entry.get()
        phase =           self.phase_entry.get()
        stage =           self.stage_entry.get()
        active_status =   self.active_status_options.get()

        try:
            progress = float(progress)/100
        except:
            if self.context == 'insert':
                progress = 0
            elif self.context == 'modify':
                progress = self.data[11]

        for req in [oec_number, title, client, location]:
            if req == '': 
                messagebox.showerror("Required Field Empty",
                "Please fill out all required fields before submitting. " + \
                "Please try again.")
                return False

        if self.context == 'insert':
            new_row = DB_connect('SELECT MAX(rowid) FROM project_info', 
            database=PROJECTDB)
            rowid = int(new_row[0][0])+1 

            todaytext = datetime.today().strftime('%Y-%m-%d %H:%M:%S')

            status_log = f"Project {oec_number} was created.\n" + \
                f"The project is located at {location}.\n" + \
                f"The Client of this project is {client}."
            
            sql_str = f"""'{oec_number}', '{client_job}', '{client}', 
                'ACTIVE', '{title}', '{location}', '', '{project_type}',
                '',   '',  '0', ''"""

            project_input_entry(rowid, 'project_info', PROJECTDB,sql_str,
            status_log, 'PROJECT CREATION', user = self.user)

            os.mkdir(FileSystem.get_project_folder(rowid))   

            self.parent.searchwindow.refresh_results()         

        elif self.context == 'modify':
            datasets = [
                (oec_number, 'OEC No', 'oec_job'),
                (title, 'title', 'project_name'),
                (client,  'client', 'client'),
                (client_job, 'client job number', 'client_job'),
                (active_status,  'active status', 'active_status'),
                (location,  'location', 'location'),
                (project_type, 'project type', 'project_type'),
                (phase, 'phase', 'current_phase'),
                (stage, 'stage', 'current_stage'),
                (progress, 'progress percent', 'current_percent_complete'),
            ]

            past_path = FileSystem.get_project_folder(self.data[0])

            project_edit_entry(self.data[0], self.data[0], 'project_info',
            PROJECTDB, f"Project {oec_number}", 'PROJECT INFO EDIT',
            self.data, self.data_dict, datasets, user=self.user)

            os.rename(past_path, FileSystem.get_project_folder(self.data[0]))
            self.parent.searchwindow.refresh_page()
        self.cancel_window()
        
    def display_data(self, data = None):
        self.data = data
        self.oec_entry          .delete()
        self.title_entry        .delete()
        self.client_entry       .delete()
        self.client_job_entry   .delete()
        self.location_entry     .delete()
        self.project_type_entry .delete()
        self.progress_entry     .delete()
        self.phase_entry        .delete()
        self.stage_entry        .delete()

        if data == None:
            self.context = 'insert'
            self.oec_entry.insert(datetime.today().strftime('%y-XXXX'))
            self.enterbutton.configure(text="START PROJECT")
            self.titlelabel.configure(text='START A NEW PROJECT')
            self.height=360
            self.folder_frame.grid_remove()

        else: 
            self.context = 'modify'
            self.folder_frame.grid(row=0,column=0,columnspan=2, pady=5, 
                padx=(35,0))
            self.enterbutton.configure(text='UPDATE PROJECT')
            titletext = f"UPDATE {self.data[1]}"
            if len(titletext)>20:
                titletext = titletext[:20]+'...'
            self.titlelabel.configure(text=titletext)
            self.active_status_options.set(self.data[4])

            self.oec_entry               .insert(self.get_data('oec_job'))
            self.client_job_entry        .insert(self.get_data('client_job'))
            self.client_entry            .insert(self.get_data('client'))
            self.title_entry             .insert(self.get_data('project_name'))
            self.location_entry          .insert(self.get_data('location'))
            self.project_type_entry      .insert(self.get_data('project_type'))
            self.phase_entry             .insert(self.get_data('current_phase'))
            self.stage_entry             .insert(self.get_data('current_stage'))
            try:
                self.progress_entry.insert(f'{(100*self.get_data("current_percent_complete")):.1f}') 
            except TypeError:
                pass
            self.height = 500
            self.canvas_window.v_scroll_pack()
        
        self.widget_placement()
        self.show_window()

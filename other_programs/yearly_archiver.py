#############################################################################################
# yearly_archiver.py
# 
# created: 9/02/22
# creator: Ethan de Leon
# Required Installs: pandas
#############################################################################################

# region Imports
import os
import time 
import shutil
import tkinter as tk
import pandas as pd
from datetime import datetime
from tkinter import CENTER, END, messagebox

from Backend.database import DB_connect, PROJECTDB
from Backend.path_analyzer import PathAnalyzer
from GUI.GUI_Mains import FONT
from GUI.main_window import ProgramWindow

# endregion
# region MACROS

PROGRAMTITLE = 'OEC YEARLY ARCHIVER'
FOLDER = r"G:/"
OECMAIN = r'O:\1-project'
ENTRYLIMIT = 1000
UPDATELIMIT = 10000
# endregion

class AutoArchiverGUI(ProgramWindow):
    def __init__(self) -> None:
        super().__init__(configure=self.configure)
    
    def configure(self):
        self.settings()
        self.widgets()
        self.root.update()
        self.root.minsize(self.root.winfo_width()+200,self.root.winfo_height())
        self.root.maxsize(self.root.winfo_width()+200,self.root.winfo_height())
        self.root.resizable(0,0)
        self.root.update()
        self.root.geometry('+{}+{}'.format(int((self.root.winfo_screenwidth()-self.root.winfo_width())/2),
            int((self.root.winfo_screenheight()-self.root.winfo_height())/2)))

    def settings(self):
        self.root.title(PROGRAMTITLE)

    def widgets(self):
        titleframe = tk.Frame(self.mainframe,bg='white')
        titlelabel = tk.Label(titleframe, font = ("montserrat extrabold",16,'bold'), 
            text="★ "+PROGRAMTITLE.upper()+" ★", bg=titleframe.cget('background'),
            height=2)
        body_frame = tk.Frame(self.mainframe, bg=self.mainframe.cget('background'))
        terminal_frame = tk.Frame(body_frame, bg=self.mainframe.cget('background'))
        terminal_label = tk.Text(terminal_frame, font = FONT, 
            height=6, width=50)
        self.program = AutoArchiver(FOLDER, output_terminal=terminal_label, window=self.root)
        self.start_button = tk.Button(body_frame, text = 'Start Archiving', command=self.start_archiving)

        terminal_label.insert('1.0', 'This process takes about 70 minutes.')

        titleframe.pack(fill='x', ipadx=10)
        titlelabel.pack()
        body_frame.pack(fill='both')
        terminal_frame.pack(fill='x', pady=10, anchor=CENTER)
        terminal_label.pack()
        self.start_button.pack(pady=10, anchor=CENTER)

    def start_archiving(self):
        self.start_button.configure(bg='gray90', text='Archiving...', command=None)
        self.start_button.pack_forget()
        self.root.update()
        try: self.program.yearly_archiver(self.program.folder)
        except: 
            messagebox.showerror('Error', "An Error has occured. Please Try Again") 
            exit()
        self.start_button.configure(bg='white', text='Start Archiving', command = self.start_archiving)
        self.start_button.pack(pady=10, anchor=CENTER)

class AutoArchiver():
    sqlinsert = "INSERT INTO documents VALUES "
    sql_value = """(
            '{}', '{}', '{}', '{}', '{}',
            '{}', '{}', '{}', '{}', '{}',
            '{}', '{}', '{}', '{}', '{}',
            '{}', '{}', '{}', '{}', '{}',
            '{}', '{}', '{}'), """
    def __init__(self, startfolder = None, output_terminal = None, window=None) -> None:
        self.folder = startfolder
        self.output_terminal = output_terminal
        self.window = window
     
    def auto_filer_yearly_archiver(self, folder):
        element_list = os.listdir(folder)
        self.folder_count += 1

        terminal_text = 'Analyzing {}'.format(folder.replace('/','\\'))
        if self.output_terminal==None: print(terminal_text)
        else: 
            self.output_terminal.delete('1.0', END)
            self.output_terminal.insert('1.0',terminal_text)
            self.window.update()

        for elem in element_list:
            # Lets user know where we are in the print
            element = os.path.join(folder, elem)

            if os.path.isdir(element): self.auto_filer_yearly_archiver(element)
            if not os.path.isfile(element): continue
            
            file_query, create_date = self.file_analyzer(element)
            file_year = datetime.strftime(datetime.strptime(create_date,'%Y-%m-%d %H:%M:%S'), "%Y")

            #prevents duplicate entries
            if element in self.yearly_database_dict[file_year]['existing_files']: continue

            database = self.yearly_database_dict[file_year]['database']
            self.yearly_database_dict[file_year]['entry_array'] += file_query
            self.yearly_database_dict[file_year]['entry_count'] += 1

            if self.yearly_database_dict[file_year]['entry_count']<ENTRYLIMIT: continue

            self.yearly_database_dict[file_year]['entry_array']=self.yearly_database_dict[file_year]['entry_array'].strip(', ')
            terminal_text = 'Archiving {} documents into {} ({})'.format(self.yearly_database_dict[file_year]['entry_count'],os.path.basename(database), element)
            if self.output_terminal==None: print(terminal_text)
            else: 
                self.output_terminal.delete('1.0', END)
                self.output_terminal.insert('1.0',terminal_text)
                self.window.update()

            DB_connect(self.yearly_database_dict[file_year]['entry_array'],database=database)

            self.yearly_database_dict[file_year]['entry_array'] = "INSERT INTO documents VALUES "
            self.yearly_database_dict[file_year]['entry_count'] = 0

    def file_analyzer(self, file):
        todaytext = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        file_address = (file.replace('/','\\')).replace("'", "''")
        file_name = (os.path.basename(file)).replace("'", "''")
        _, file_type = os.path.splitext(file)
        file_type = file_type.lstrip('.').upper()

        try:    last_modified = datetime.fromtimestamp(os.path.getmtime(file)).strftime( '%Y-%m-%d %H:%M:%S')
        except: last_modified = todaytext.strftime('%Y-%m-%d %H:%M:%S')
        try:    created_date = datetime.fromtimestamp(os.path.getctime(file)).strftime('%Y-%m-%d %H:%M:%S')
        except: created_date = todaytext.strftime('%Y-%m-%d %H:%M:%S')

        try: file_size = os.path.getsize(file_address)
        except: file_size = 1
        
        new_query = self.sql_value.format(
        file_address,                                   #file_address                      
        file_name,                                      #file_name                  
        file_type,                                      #file_type         
        file_size,                                      #file_size
        PathAnalyzer.findDwgNumPath(file_name),         #dwg_num                  
        '',                                             #title                              
        PathAnalyzer.findRevPath(file_name),            #revision        
        PathAnalyzer.findSheetPath(file_name),          #sheets            
        '',                                             #department              
        '',                                             #remarks                                
        '',                                             #client                             
        PathAnalyzer.findJobOrderPath(file_address),    #client_job                              
        '',                                             #oec_job  
        '',                                             #purchase_order
        PathAnalyzer.findSubstationPath(file_address),  #location  
        todaytext,                                      #upload_date  
        '',                                             #file owner
        created_date,                                   #create_date  
        last_modified,                                  #modify_date
        '',                                             #last_accessed_by  
        '',                                             #package_id  
        '',                                             #project_id
        ''                                              #package_index
        )
        return new_query, created_date

    def yearly_database_initialize(self): 
        docpath = r"G:\Yearly_Archive\oec_documents.db"
        database_str = os.path.splitext(docpath)
        self.yearly_database_dict = {}
        for year in range(1986, int(datetime.today().strftime("%Y"))+1):
            cur_database = database_str[0]+'_{}'.format(year)+database_str[1]
            if not os.path.exists(cur_database): shutil.copy(docpath, cur_database)
            self.yearly_database_dict[str(year)] = {'database':cur_database, 'entry_array':"INSERT INTO documents VALUES ", 'existing_files':[], 'entry_count':0}
            files_from_database = DB_connect("SELECT file_address FROM documents", database = cur_database)
            for file in files_from_database: self.yearly_database_dict[str(year)]['existing_files'].append(file[0])

        self.folder_count = 0

    def yearly_archiver(self, folder):
        start_time = time.time()
        self.yearly_database_initialize()
        self.auto_filer_yearly_archiver(folder)

        for year in self.yearly_database_dict:
            if self.yearly_database_dict[year]['entry_count'] == 0: continue
            terminal_text = 'Archiving {} documents to {}'.format(self.yearly_database_dict[year]['entry_count'],os.path.basename(self.yearly_database_dict[year]['database']))
            if self.output_terminal==None: print(terminal_text)
            else: 
                self.output_terminal.delete('1.0', END)
                self.output_terminal.insert('1.0',terminal_text)
            self.yearly_database_dict[year]['entry_array']=self.yearly_database_dict[year]['entry_array'].strip(', ')
            DB_connect(self.yearly_database_dict[year]['entry_array'], database=self.yearly_database_dict[year]['database'])
        
        minutes = int((time.time() - start_time)/60)
        seconds = int((time.time() - start_time)-(minutes*60))
        doc_count , byte_count = self.yearly_doc_count()
        
        terminal_text = 'Analysis Complete!\n\n' \
            +"Execution Time: {} Min. {} Sec.\n".format(minutes, seconds) \
            +"Number of Folders Encountered: {}\n".format(self.folder_count) \
            +"Total File Count: {} files\n".format(doc_count)\
            +"Total Byte Count: {} Gigabytes\n".format(byte_count)

        if self.output_terminal==None: print(terminal_text)
        else: 
            self.output_terminal.delete('1.0', END)
            self.output_terminal.insert('1.0',terminal_text)
            self.window.update()

    def yearly_doc_count(self, namecount = False):
        self.yearly_database_initialize()
        document_count = 0
        byte_count = 0
        for year in self.yearly_database_dict:
            entry = DB_connect("SELECT count(*), SUM(file_size)/1000000000 FROM documents", database=self.yearly_database_dict[year]['database'])[0]
            document_count += entry[0]
            try: byte_count += entry[1]
            except: pass
                

        print("Total File Count: {} files".format(document_count))
        print("Total Byte Count: {} Gigabytes".format(byte_count))
        if namecount:
            named_files = 0
            numbered_files = 0
            for year in self.yearly_database_dict:
                entry  = DB_connect("SELECT count(*) FROM documents WHERE (title IS NOT NULL)AND(title is not '')", database=self.yearly_database_dict[year]['database'])[0]
                entry1 = DB_connect("SELECT count(*) FROM documents WHERE (dwg_num IS NOT NULL)AND(dwg_num is not '')AND(file_type = 'PDF' OR 'DGN')", database=self.yearly_database_dict[year]['database'])[0]
                try: named_files += entry[0]
                except: pass
                try: numbered_files += entry1[0]
                except: pass
            print("Numbered Files Count: {} files".format(numbered_files))
            print("Titled Files Count: {} files".format(named_files))
            print("{:.1f}% of files are titled in our system".format(float(named_files)/float(numbered_files)*100))
        return document_count, byte_count

    def update_doc_titles(self):
        self.yearly_database_initialize()
        self.updater_list = []
        self.search_for_progress_folder(OECMAIN)

        print('Applying updates to {} documents'.format(len(self.updater_list)))
        for year in self.yearly_database_dict:
            if len(self.yearly_database_dict[year]['existing_files'])==0: continue
            print("Updating documents on", self.yearly_database_dict[year]['database'])
            DB_connect(self.updater_list, database=self.yearly_database_dict[year]['database'])
        self.updater_list = []

    def update_doc_projects(self):
        self.yearly_database_initialize()
        self.updater_list = []

        projects = DB_connect("SELECT rowid, oec_job, client_job FROM project_info WHERE (client_job IS NOT NULL)AND(client_job is not '')", database=r'E:\.shortcut-targets-by-id\1kwHnoQenHJiBDLz907c6OevuJ6Oa-CGn\Databases\oec_projects.db')
        for project in projects: 
            self.updater_list.append(
                "UPDATE documents SET project_id = '{}', oec_job='{}' WHERE client_job = '{}'".format(
                    project[0],project[1],project[2]))
        for year in self.yearly_database_dict: 
            if len(self.yearly_database_dict[year]['existing_files'])==0: continue
            print("Updating documents on", self.yearly_database_dict[year]['database'])
            DB_connect(self.updater_list, database=self.yearly_database_dict[year]['database'])
        
    def search_for_progress_folder(self, folder):
        elems = os.listdir(folder)
        if "DWGPROG" in os.path.basename(folder).upper(): print('Analyzing', folder)
        for elem in elems:
            file = os.path.join(folder, elem)
            if os.path.isdir(file): 
                self.search_for_progress_folder(file)
                continue
            if "DWGPROG" not in os.path.basename(folder).upper(): continue
            
            if 'xls' not in elem.lower(): continue
            
            if not self.analyze_drawing_list(file): continue
            
            if len(self.updater_list)<UPDATELIMIT: continue
            print('Applying updates to {} documents'.format(len(self.updater_list)))
            for year in self.yearly_database_dict: 
                if len(self.yearly_database_dict[year]['existing_files'])==0: continue
                print("Updating documents on", self.yearly_database_dict[year]['database'])
                DB_connect(self.updater_list, database=self.yearly_database_dict[year]['database'])
            self.updater_list = []

    def analyze_drawing_list(self, file):
        try: 
            document_data = pd.read_excel(file, dtype=str)
        except: 
            print('Could not read, file may be corrupted:', file)
            return False
        print('Reading', file)

        # Finds the Drawing Number and Title Columns
        dwgcol = None
        titlecol = None
        for column in range(len(document_data.columns)):
            if 'DWG' in str(document_data.columns[column]).upper():
                dwgcol = column
            elif 'DRAWING' in str(document_data.columns[column]).upper():
                dwgcol = column
            elif 'TITLE' in str(document_data.columns[column]).upper():
                titlecol = column
            if (dwgcol!=None) and (titlecol!=None): break

        if (dwgcol==None) or (titlecol==None):
            for row in range(len(document_data.index)):
                for col in range(len(document_data.columns)):
                    if 'DWG' in str(document_data.iloc[row,col]).upper():
                        dwgcol = col
                    elif 'DRAWING' in str(document_data.iloc[row,col]).upper():
                        dwgcol = col
                    elif 'TITLE' in str(document_data.iloc[row,col]).upper():
                        titlecol = col
                if dwgcol and titlecol: break

        if (dwgcol==None):
            print("File does not contain a Drawing Number Column:", file)
            return False
        elif (titlecol==None): 
            print("File does not contain a Title Column:", file)
            return False 

        for row in range(1,len(document_data.index)):
            try: 
                if not PathAnalyzer.is_int(document_data.iloc[row,1]): continue
                title = str(document_data.iloc[row,titlecol]).replace("'","''").strip()
                dwg_num = str(document_data.iloc[row,dwgcol]).replace('.0','').strip()
                self.updater_list.append("UPDATE documents SET title = '{}' WHERE dwg_num = '{}'".format(title, dwg_num))
            except: continue
         
        return True

if __name__ == '__main__':
    program = AutoArchiver()
    program.yearly_doc_count(namecount=True)
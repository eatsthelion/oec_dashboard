PROGRAMTITLE = 'Document Edits'
import os
import shutil
from tkinter import messagebox, filedialog

from Backend.filesystem import FileSystem
from Backend.path_analyzer import PathAnalyzer
from Backend.database_send import project_edit_entry, project_input_entry
from Backend.database import  DOCDB, EMPTYLIST, DB_connect
from Backend.database_get import get_package_name, get_project_from_package

from GUI.widgets.basics import *
from GUI.widgets.terminal import Terminal
from GUI.project_catalog.edit_windows.edit_window import EditWindow

class EditDocumentGUI(EditWindow):
    def __init__(self, master, **kw) -> None:
        super().__init__(master, bg='royalblue3', width=500, height=500, 
        programt_title = PROGRAMTITLE, **kw)
        self.data = None
        self.file = None
        self.package_id = None

    def configure(self):
        self.canvas_window.v_scroll_pack()
        
        ew = 25

        # File Selection Widgets
        self.multifileframe = MyLabelFrame(self.canvasframe, text='UPLOAD MULTIPLE FILES')
        self.singlefileframe = MyLabelFrame(self.canvasframe, text='UPLOAD 1 FILE')
        self.entryframe = MyFrame(self.singlefileframe, bg=self.bg)
        self.fileframe = MyLabelFrame(self.singlefileframe, text='FILE SELECTION')
        self.file_button = MyButton(self.fileframe, text="SELECT FILE",
            command = self.select_file)
        self.files_button = MyButton(self.multifileframe, text='SELECT MANY FILES',
            command=self.upload_many_files) 
        self.filename_entry = MyEntry(self.fileframe, width=ew, state=DISABLED, 
            disabledforeground='black', disabledbackground='goldenrod2')
        filelabel = MyLabel(self.fileframe, text='Filename:')

        filelabel.grid(row=0,column=0, padx=(5,0), pady=5)
        self.filename_entry.grid(row=0,column=1, padx=(5,0), pady=5, sticky=NS)
        self.file_button.grid(row=0,column=2, padx=5, pady=5)
        self.files_button.pack(fill='x', expand=1, pady=5, padx=5)

        # Data Entry Widgets
        self.title_entry = MyText(self.entryframe, width=ew, height=3)
        self.desc_entry = MyText(self.entryframe, width=ew, height=3)

        self.drawingno_entry = MyEntry(self.entryframe, width=ew)
        self.rev_entry = MyEntry(self.entryframe, width=ew)
        self.sheet_entry = MyEntry(self.entryframe, width=ew)
        self.purpose_entry = MyEntry(self.entryframe, width=ew)
        self.progress_entry = MyEntry(self.entryframe, width=ew)

        self.datapairs = [
            ("Title*:",self.title_entry),
            ("Description:", self.desc_entry), 
            ("Drawing No:", self.drawingno_entry),
            ("Revision:", self.rev_entry),
            ("Sheet:", self.sheet_entry),
            ("Purpose:", self.purpose_entry),
            ('Progress:', self.progress_entry)
        ]

        for row, datapair in enumerate(self.datapairs):
            label = MyLabel(self.entryframe, text=datapair[0])
            label.grid(row=row, column = 0, padx=5, pady=(5,0), sticky=W)
            datapair[1].grid(row=row, column = 1, padx=5, pady=(5,0), sticky=EW)

        self.enterbutton = MyButton(self.canvasframe, command=self.enter_command)
        self.terminal = Terminal(self.frame) 
        
        return super().configure()

    def widget_placements(self):
        if self.context == 'insert':
            self.multifileframe.pack(pady=(0,5), expand=1, padx=5, fill='x')
        self.singlefileframe.pack(pady=(0,5), expand=1, padx=5, fill='x')
        
        self.fileframe.pack(pady=(0,5))
        self.entryframe.pack(expand=1, pady=(0,5), padx=5)
        self.enterbutton.pack(fill='x', padx=5, pady=5)

    def enter_command(self):
        filename   = self.filename_entry.get()
        title      = self.title_entry      .get()
        desc       = self.desc_entry       .get()
        drawingno  = self.drawingno_entry  .get()         
        rev        = self.rev_entry        .get()
        sheet      = self.sheet_entry      .get() 
        purpose    = self.purpose_entry    .get()   
        progress   = self.progress_entry   .get() 

        if filename != "":
            filetype = os.path.splitext(filename)[1].upper()
        else:
            filetype = ''

        # Error Handling
        for req in [title]:
            if req == '':
                messagebox.showerror("Required Field Empty",
                "Please fill out all required fields before submitting. " + \
                "Please try again.")
                return False

        if self.context == 'insert':
            # Error if there is a document with the same title in the same package
            if not self.filename_check(filename):
                return False
            if not self.insert_document(filename, filetype, title, desc, 
                drawingno, rev, sheet, purpose, progress):
                return False
            self.parent.searchwindow.refresh_results()
        else:
            # Checks if there is a document with the same title that exists within
            # the same package
            if title != self.data[4]:
                same_title = DB_connect(f"""
                    SELECT rowid
                    FROM documents
                    WHERE package_id = {self.package_id} and title = '{title}'""",
                    database = DOCDB)
                if len(same_title)>0:
                    messagebox.showerror("Same Titled Document",
                        "A document of the same title already exists in this package.")
                    return False
            # endregion

            status_updates = ''
            name = f"Package {get_package_name(self.package_id)}'s {self.data[2]}"
            
            # region Re-files document depending on edits made
            if (filename != self.data[2]) or (self.file != None):
                if filename != self.data[2]:
                    # Error Handling
                    same_filename = DB_connect(f"""
                        SELECT rowid
                        FROM documents
                        WHERE package_id = {self.package_id} and filename = '{filename}'
                        """,
                        database = DOCDB)
                    if len(same_filename)>0:
                        messagebox.showerror("Existing File",
                            "This file already exists in this package.")
                        return False

                package_folder = FileSystem.get_package_folder(self.package_id)
                old_path = FileSystem.get_project_document(self.data[0])
                new_path = os.path.join(package_folder, filename)
                
                # Old document does not exist
                if not old_path:
                    shutil.copy(self.file, new_path)
                # Renames or Removes old document 
                elif self.file == None:
                    # Removes old document
                    if filename in EMPTYLIST:
                        os.remove(old_path)
                    # Renames old document
                    else:
                        os.rename(old_path, new_path)
                # Replaces old document with new document
                else:
                    status_updates += f"\n\n{name}'s was replaced with {filename}."
                    shutil.copy(self.file, new_path)
            # endregion

            datapairs = [
                (self.data[2], filename, 'filename', 'filename'), 
                (self.data[3], filetype, 'proposed amount', 'file_type'),
                (self.data[4], title, 'title', 'title'),
                (self.data[5], drawingno, 'drawing no', 'drawing_num'),
                (self.data[6], rev, 'REV', 'revision'),
                (self.data[7], sheet, 'SH', 'sheet'),
                (self.data[8], desc, 'description', 'description'),
                (self.data[9], purpose, 'purpose', 'doc_purpose'),
                (self.data[10], progress, 'progress', 'progress'),
            ]

            project_edit_entry(get_project_from_package(self.package_id), 
                self.data[0], 'documents', datapairs, name, "DOCUMENT EDIT",
                datapairs, user=self.user)
            self.parent.searchwindow.refresh_page()

        self.cancel_window()

    def filename_check(self, filename):
        if filename != "":
            same_filename = DB_connect(f"""
                SELECT rowid
                FROM documents
                WHERE package_id = {self.package_id} and filename = '{filename}'
                """,
                database = DOCDB)
            if len(same_filename)>0:
                messagebox.showerror("Existing File",
                    f"The file {filename} already exists in this package.")
                return False
        return True

    def insert_document(self, filename,filetype, title, desc, drawingno, rev,
        sheet, purpose, progress, copies = False):
        #same_title = DB_connect(f"""
        #    SELECT rowid
        #    FROM documents
        #    WHERE package_id = {self.package_id} and title = '{title}'""",
        #    database = DOCDB)
        #if len(same_title)>0:
        #    messagebox.showerror("Same Titled Document",
        #        "A document of the same title already exists in this package.")
        #    return False

        # Error if there is a document with the same filename in the package
        

        try: 
            index = int(DB_connect(f"""
                SELECT MAX(package_index) 
                FROM documents 
                WHERE package_id = '{self.package_id}'""",
                database = DOCDB)[0][0]) + 1
        except TypeError:
            index = 1

        # Uploads file or folder to the Filing System
        if self.file not in EMPTYLIST:
            filename = os.path.basename(self.file)
            pathname = FileSystem.get_package_folder(self.package_id)
            copysink = os.path.join(pathname, filename)
            if os.path.exists(copysink):
                os.remove(copysink)
            if os.path.isdir(self.file):
                shutil.copytree(self.file, copysink)
            elif os.path.isfile(self.file):
                shutil.copy(self.file, os.path.join(copysink))

        sql_str = f"""'{self.package_id}', '{index}', '{filename}', 
            '{filetype}', '{title}', '{drawingno}', '{rev}', '{sheet}', 
            '{desc}', '{purpose}', '{progress}', '{self.user.user_id}', ''"""
        status_updates = f"Document {title} was created in Package {self.package_id}."

        project_input_entry(get_project_from_package(self.package_id), 
            'documents', DOCDB, sql_str, status_updates, 'NEW DOCUMENT',
            user=self.user)

    def analyze_document_info(self,filename, replace=False):
        drawingno = PathAnalyzer.findDwgNumPath(filename)
        rev = PathAnalyzer.findRevPath(filename)
        sheet = PathAnalyzer.findSheetPath(filename)

        if replace:
            self.drawingno_entry.delete()
            self.rev_entry.delete()
            self.sheet_entry.delete()
            self.drawingno_entry.insert(drawingno)
            self.rev_entry.insert(rev)
            self.sheet_entry.insert(sheet)
        
        return (drawingno, rev, sheet)
    
    def apply_document_list():
        pass

    def select_file(self):
        file = filedialog.askopenfilename(title = 'Select a file')
        if not file:
            return
        self.file = file
        self.filename_entry.configure(state=NORMAL)
        self.filename_entry.delete()
        self.filename_entry.insert(os.path.basename(self.file))
        self.filename_entry.configure(state=DISABLED)
        self.analyze_document_info(file)

    def upload_many_files(self):
        filelist = filedialog.askopenfilenames(title='Select files')
        if not filelist:
            return

        # Checks each file to see if there are no duplicates in the given list
        # of files
        for file in filelist:
            if not self.filename_check(os.path.basename(file)):
                return False

        for file in filelist:
            self.file = file
            filename = os.path.basename(file)
            filetype = os.path.split(file)[1]
            docdata = self.analyze_document_info(filename)

            self.insert_document(filename=filename,filetype=filetype,title='',
            drawingno=docdata[0], rev=docdata[1], sheet=docdata[2], purpose='',
            progress=0)

        self.parent.searchwindow.refresh_results()

    def display_data(self, package_id, data = None):
        self.filename_entry.configure(state=NORMAL)
        self.filename_entry.delete()
        self.filename_entry.configure(state=DISABLED)

        self.title_entry.delete('1.0',END)
        self.desc_entry.delete('1.0',END)
        self.drawingno_entry.delete()
        self.rev_entry.delete()
        self.sheet_entry.delete()
        self.purpose_entry.delete()
        self.progress_entry.delete()

        self.data = data
        self.package_id = package_id
        self.file = None

        if data != None:
            self.context = 'modify'
            self.singlefileframe.configure(text="")
            self.titlelabel.configure(text="MODIFY DOCUMENT")
            self.file_button.configure(text='REPLACE')
            self.enterbutton.configure(text="SAVE CHANGES")

            self.filename_entry.configure(state=NORMAL)
            self.filename_entry.insert(self.data[2])
            if self.data[2] in EMPTYLIST:
                self.filename_entry.configure(state=DISABLED)
                self.file_button.configure(text='SELECT')
            self.files_button.grid_remove()

            self.title_entry.insert(self.data[4])
            self.desc_entry.insert(self.data[8])
            self.drawingno_entry.insert(self.data[5])
            self.rev_entry.insert(self.data[6])
            self.sheet_entry.insert(self.data[7])
            self.purpose_entry.insert(self.data[8])
            self.progress_entry.insert(self.data[9])
        else: 
            self.context = 'insert'
            self.singlefileframe.configure(text="UPLOAD 1 FILE")
            self.titlelabel.configure(text="NEW DOCUMENT")
            self.enterbutton.configure(text="UPLOAD DOCUMENT")
            self.file_button.configure(text='SELECT')
            self.files_button.grid()
        self.widget_placements()
        self.show_window()
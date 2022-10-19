import tkinter as tk
from tkinter import messagebox
from tkinter import *
from Backend.database import  ITEMCATALOG, DB_connect

import GUI.fonts
from GUI.widgets.highlight import enter_leave_stylechange
from GUI.GUI_Mains import FONT, FONTBOLD, OECCOLOR
from GUI.main_window import PopupWindow

ENTRYWIDTH = 50

COLUMNTITLES = ['Project Title', 'Client', 'Client Job #','Location', 'Project Engineer', 
    'Outdoor Designers', 'Indoor Designers', 'Project Type', 'CWA Type']

class UpdateMaterialGUI(PopupWindow):
    def __init__(self, master, parent=None, configure=...) -> None:
        self.master = master
        super().__init__(master, bg='cyan4', configure=self.initial)
        self.parent=parent

    def initial(self):
        self.data=None

        self.titlelabel.configure(text='UPDATE ITEM')
        self.widgetdict = {}
        self.entryframe = tk.Frame(self.canvasframe, bg=self.canvasframe.cget('background'))
        self.entryframe.pack(anchor=CENTER)
        
        item_label          = tk.Label(self.entryframe, font=FONT, bg=self.frame.cget('background'), text='Item Name*:')
        code_label          = tk.Label(self.entryframe, font=FONT, bg=self.frame.cget('background'), text='Code:')
        desc_label          = tk.Label(self.entryframe, font=FONT, bg=self.frame.cget('background'), text='Description:')
        type_label          = tk.Label(self.entryframe, font=FONT, bg=self.frame.cget('background'), text='Type:')
        ref_label           = tk.Label(self.entryframe, font=FONT, bg=self.frame.cget('background'), text='Reference:')
        other_label         = tk.Label(self.entryframe, font=FONT, bg=self.frame.cget('background'), text='Other Data:')

        item_label          .grid(row=self.row_counter(reset=True), column=0, padx=10, sticky=NW)
        code_label          .grid(row=self.row_counter(), column=0, padx=10, sticky=NW)
        desc_label          .grid(row=self.row_counter(), column=0, padx=10, sticky=NW)
        type_label          .grid(row=self.row_counter(), column=0, padx=10, sticky=NW)
        ref_label           .grid(row=self.row_counter(), column=0, padx=10, sticky=NW)
        other_label         .grid(row=self.row_counter(), column=0, padx=10, sticky=NW)

        self.item_strvar             = tk.StringVar()
        self.code_strvar             = tk.StringVar()
        self.type_strvar             = tk.StringVar()
        self.ref_strvar              = tk.StringVar()
        self.other_strvar             = tk.StringVar()

        self.item_entry             = tk.Entry(self.entryframe, textvariable = self.item_strvar            , font=FONT, width =ENTRYWIDTH)
        self.code_entry             = tk.Entry(self.entryframe, textvariable = self.code_strvar            , font=FONT, width =ENTRYWIDTH)
        self.desc_entry             = tk.Text (self.entryframe, font=FONT, width =ENTRYWIDTH, height = 5)
        self.type_entry             = tk.Entry(self.entryframe, textvariable = self.type_strvar            , font=FONT, width =ENTRYWIDTH)
        self.ref_entry              = tk.Entry(self.entryframe, textvariable = self.ref_strvar            , font=FONT, width =ENTRYWIDTH)
        self.other_entry            = tk.Entry(self.entryframe, textvariable = self.other_strvar            , font=FONT, width =ENTRYWIDTH)
        
        self.item_entry             .grid(row=self.row_counter(reset=True), column=1, padx=10,sticky=NW)
        self.code_entry             .grid(row=self.row_counter(), column=1, padx=10,sticky=NW)
        self.desc_entry             .grid(row=self.row_counter(), column=1, padx=10,sticky=NW, pady=5)
        self.type_entry             .grid(row=self.row_counter(), column=1, padx=10,sticky=NW)
        self.ref_entry              .grid(row=self.row_counter(), column=1, padx=10,sticky=NW)
        self.other_entry            .grid(row=self.row_counter(), column=1, padx=10,sticky=NW)

        self.updatebutton = tk.Button(self.canvasframe, font=FONT, text="UPDATE ITEM", relief='flat', cursor='hand2', command = self.update_material)
        self.updatebutton.pack(pady=10)

    def row_counter(self, reset=False):
        if reset == True: self.row_count = 0
        try: self.row_count +=1
        except: self.row_count = 0
        return self.row_count

    def update_material(self):
        item = self.item_entry .get().replace("'", "''")
        code = self.code_entry .get().replace("'", "''")
        desc = self.desc_entry .get('1.0','end-1c').replace("'", "''")
        typ  = self.type_entry .get().replace("'", "''")
        ref  = self.ref_entry  .get().replace("'", "''")
        other= self.other_entry.get().replace("'", "''")

        required = [code]
        for req in required:
            if req == '': 
                messagebox.showerror("Required Field Empty", 'Please fill out all required fields before submitting. Please try again.')
                return False

        existing_code = DB_connect("SELECT rowid, item FROM item_catalog WHERE code = '{}'".format(code), database=ITEMCATALOG)
        if len(existing_code)>0: 
            if existing_code[0][0] != self.data[0]:
                messagebox.showerror("Existing Code", 'An item with the same code exists in the database. Please try again with a different code.')
                return False
        
        if not DB_connect("""UPDATE item_catalog SET item='{}', code = '{}', description = '{}', type='{}', reference = '{}', other_data = '{}' WHERE rowid = '{}'
            """.format(item, code, desc, typ, ref, other, self.data[0]), 
            database=ITEMCATALOG, debug =True): return False

        self.item_entry .delete(0,END)
        self.code_entry .delete(0,END)
        self.desc_entry .delete('1.0',END)
        self.type_entry .delete(0,END)
        self.ref_entry  .delete(0,END)
        self.other_entry.delete(0,END)

        self.cancel_window()
        self.parent.searchwindow.resultwindow.refresh_results()
        return True

    def display_data(self):
        self.item_entry .delete(0,END)
        self.code_entry .delete(0,END)
        self.desc_entry .delete('1.0',END)
        self.type_entry .delete(0,END)
        self.ref_entry  .delete(0,END)
        self.other_entry.delete(0,END)

        try: self.item_entry .insert(0,self.data[1])        
        except: pass
        try: self.code_entry .insert(0,self.data[2])        
        except: pass
        try: self.desc_entry .insert('1.0',self.data[4])    
        except: pass    
        try: self.type_entry .insert(0,self.data[5])        
        except: pass
        try: self.ref_entry  .insert(0,self.data[6])        
        except: pass
        try: self.other_entry.insert(0,self.data[7])        
        except: pass
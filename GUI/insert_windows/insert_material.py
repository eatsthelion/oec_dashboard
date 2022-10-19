import tkinter as tk
from datetime import datetime
from tkinter import *
from tkinter import messagebox
from Backend.database import  DB_connect

import GUI.fonts
from GUI.widgets.highlight import enter_leave_stylechange
from GUI.GUI_Mains import FONT, FONTBOLD
from GUI.main_window import PopupWindow

from Backend.database import PROJECTDB, DB_connect

TABLE = 'table'
VALUES = "'{}', '{}', '', '{}', '', '{}', '{}', '{}'"

class InsertMaterialGUI(PopupWindow):
    def __init__(self, master,parent=None, configure=...) -> None:
        self.master = master
        super().__init__(master, bg='cyan4', configure=self.initial)
        self.parent = parent

    def initial(self):
        self.titlelabel.configure(text='ADD NEW ITEM')
        self.widgetdict = {}
        self.entryframe = tk.Frame(self.frame, bg=self.canvasframe.cget('background'))
        self.entryframe.pack(anchor=CENTER, fill=BOTH, expand=1)

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
        self.desc_strvar             = tk.StringVar()
        self.type_strvar             = tk.StringVar()
        self.ref_entry               = tk.StringVar()
        self.other_entry             = tk.StringVar()

        self.item_entry             = tk.Entry(self.entryframe, textvariable = self.item_strvar            , font=FONT)
        self.code_entry             = tk.Entry(self.entryframe, textvariable = self.code_strvar            , font=FONT)
        self.desc_entry             = tk.Entry(self.entryframe, textvariable = self.item_strvar            , font=FONT)
        self.type_entry             = tk.Entry(self.entryframe, textvariable = self.item_strvar            , font=FONT)
        self.ref_entry              = tk.Entry(self.entryframe, textvariable = self.item_strvar            , font=FONT)
        self.other_entry            = tk.Entry(self.entryframe, textvariable = self.item_strvar            , font=FONT)
        
        self.item_entry             .grid(row=self.row_counter(reset=True), column=1, padx=10,sticky=NW)
        self.code_entry             .grid(row=self.row_counter(), column=1, padx=10,sticky=NW)
        self.desc_entry             .grid(row=self.row_counter(), column=1, padx=10,sticky=NW)
        self.type_entry             .grid(row=self.row_counter(), column=1, padx=10,sticky=NW)
        self.ref_entry              .grid(row=self.row_counter(), column=1, padx=10,sticky=NW)
        self.other_entry            .grid(row=self.row_counter(), column=1, padx=10,sticky=NW)

        self.uploadbutton = tk.Button(self.canvasframe, font=FONT, text="ADD ITEM", relief='flat', cursor='hand2', command=self.insert_to_database)
        self.uploadbutton.pack(pady=10)

    def row_counter(self, reset=False):
        if reset == True: self.row_count = 0
        try: self.row_count +=1
        except: self.row_count = 0
        return self.row_count

    def insert_to_database(self):
        item                    = self.item_entry            .get().replace("'", "''")
        code                    = self.code_entry            .get().replace("'", "''")
        desc                    = self.desc_entry            .get().replace("'", "''")
        type                    = self.type_entry            .get().replace("'", "''")
        ref                     = self.ref_entry             .get().replace("'", "''")
        other                   = self.other_entry           .get().replace("'", "''")
              
        required = [item]
        for req in required:
            if req == '': 
                messagebox.showerror("Required Field Empty", 'Please fill out all required fields before submitting. Please try again.')
                return False

        if code == '': 
            new_oec_code = DB_connect("SELECT MAX(code) FROM item_catalog WHERE code LIKE '%OEC%'", database=PROJECTDB)
            new_oec_code = new_oec_code[0][0].split('-')
            today = datetime.today()
            code = 'OEC'+'-'+today.strftime('%y')+'-'+str(int(new_oec_code[2])+1)

        sql_array = []
        sql_array.append( """INSERT INTO {} VALUES ()""".format(
            TABLE, VALUES.format(item, code, desc, type, ref, other)
            ))
        
        
        try: DB_connect(sql_array, database = PROJECTDB, debug=True)
        except: messagebox.showerror('Database is locked!', 'The database is locked, please try again later.')
        self.item_entry .delete(0,END)
        self.code_entry .delete(0,END)
        self.desc_entry .delete(0,END)
        self.type_entry .delete(0,END)
        self.ref_entry  .delete(0,END)
        self.other_entry.delete(0,END)

        self.cancel_window()
        self.parent.searchwindow.resultwindow.refresh_results()


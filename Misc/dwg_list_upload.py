#############################################################################################
# dwg_list_upload.py
# 
# Created: 9/02/22
# Creator: Ethan de Leon
# Purposes:
#   - Upload the contents of the drawing progess list to our archives
# Required Installs: pandas
#############################################################################################

import pandas as pd
from tkinter import filedialog, messagebox

from Backend.path_analyzer import PathAnalyzer
from Backend.database import DOCDB, DB_clean_str, DB_connect
from other_programs.yearly_archiver import AutoArchiver

def apply_dwglist_to_package(table='documents', terminal=None):
    file = filedialog.askopenfilename(title='Select a Drawing List', 
        filetypes=[('Excel','*.xlsx'), ('Excel 97','*.xls')])
    
    if not file:
        return False
    if not messagebox.askyesno('Confirm to Apply',
        'Are you sure you want to apply this file?\n\n' + \
            f'{file}'):
        return False
    try: 
        document_data = pd.read_excel(file, dtype=str)
    except:
        messagebox.showerror("Can Not Read File", "Unable to read file")
        return False
    if terminal == None: 
        print("Reading", file)
    else:
        terminal.print_terminal(f"Reading {file}")

    dwgcol = None
    titlecol = None
    for column in range(len(document_data.columns)):
        if 'DWG' in str(document_data.columns[column]).upper():
            dwgcol = column
        elif 'TITLE' in str(document_data.columns[column]).upper():
            titlecol = column
        if (dwgcol!=None) and (titlecol!=None):
            break

    if (dwgcol==None) or (titlecol==None):
        for row in range(len(document_data.index)):
            for col in range(len(document_data.columns)):
                if 'DWG' in str(document_data.iloc[row,col]).upper():
                    dwgcol = col
                elif 'TITLE' in str(document_data.iloc[row,col]).upper():
                    titlecol = col
            if dwgcol and titlecol: 
                break

    if (dwgcol==None): 
        messagebox.showerror("Required Drawing Column Not Found", 'Drawing Column was not found in this file')
        return False
    elif (titlecol==None): 
        messagebox.showerror("Required Title Column Not Found", 'Title Column was not found in this file')
        return False

    updater_list = []
    for row in range(1,len(document_data.index)):
        try: 
            if not PathAnalyzer.is_int(document_data.iloc[row,1]): continue
            title = DB_clean_str(str(document_data.iloc[row,titlecol]))
            dwg_num = DB_clean_str(str(document_data.iloc[row,dwgcol]))
            updater_list.append(
                f"UPDATE {table} SET title = '{title}' WHERE dwg_num = '{dwg_num}'"
                )
        except: continue
    
    if len(updater_list) == 0: 
        messagebox.showerror("Empty File", 'There were no documents found to be updated.')
        return False
    # Updates Changes to the Archive
    if terminal == None: 
        print("Reading", file)
    else:
        terminal.print_terminal("Connecting to Document Databases...")

    DB_connect(updater_list, database=DOCDB)
    
def upload_dwg_list_content(terminal=None):
    file = filedialog.askopenfilename(title='Select a Drawing List', filetypes=[('Excel','*.xlsx'), ('Excel 97','*.xls')])
    if not file: 
        return False
    if not messagebox.askyesno("Confirm to Upload", "Are you sure you want to upload this file?\n\n{}".format(file)): 
        return False

    try: 
        document_data = pd.read_excel(file, dtype=str)
    except:
        messagebox.showerror("Can Not Read File", "Unable to read file")
        return False

    # Finds the Drawing Number and Title Columns

    if terminal == None: 
        print("Reading", file)
    else:
        terminal.print_terminal("Reading {}".format(file))
    dwgcol = None
    titlecol = None
    for column in range(len(document_data.columns)):
        if 'DWG' in str(document_data.columns[column]).upper():
            dwgcol = column
        elif 'TITLE' in str(document_data.columns[column]).upper():
            titlecol = column
        if (dwgcol!=None) and (titlecol!=None):
            break

    if (dwgcol==None) or (titlecol==None):
        for row in range(len(document_data.index)):
            for col in range(len(document_data.columns)):
                if 'DWG' in str(document_data.iloc[row,col]).upper():
                    dwgcol = col
                elif 'TITLE' in str(document_data.iloc[row,col]).upper():
                    titlecol = col
            if dwgcol and titlecol: 
                break

    if (dwgcol==None): 
        messagebox.showerror("Required Drawing Column Not Found", 'Drawing Column was not found in this file')
        return False
    elif (titlecol==None): 
        messagebox.showerror("Required Title Column Not Found", 'Title Column was not found in this file')
        return False
    
    # Creates List of Updates to SQL
    updater_list = []
    for row in range(1,len(document_data.index)):
        try: 
            if not PathAnalyzer.is_int(document_data.iloc[row,1]): continue
            title = str(document_data.iloc[row,titlecol]).replace("'","''").strip()
            dwg_num = str(document_data.iloc[row,dwgcol]).replace('.0','').strip()
            updater_list.append("UPDATE documents SET title = '{}' WHERE dwg_num = '{}'".format(title,dwg_num))
        except: continue
    
    if len(updater_list) == 0: 
        messagebox.showerror("Empty File", 'There were no documents found to be updated.')
        return False
    # Updates Changes to the Archive
    if terminal == None: 
        print("Reading", file)
    else:
        terminal.print_terminal("Connecting to Document Archives...")
    archive = AutoArchiver()
    archive.yearly_database_initialize() 
    
    if terminal == None: 
        print("Reading", file)
    else:
        terminal.print_terminal("Updating Documents...")
    for year in archive.yearly_database_dict: 
        if len(archive.yearly_database_dict[year]['existing_files'])==0: continue
        if terminal == None: 
            print("Updating documents on", archive.yearly_database_dict[year]['database'])
        else:
            terminal.print_terminal("Updating documents on {}".format(archive.yearly_database_dict[year]['database']))
        DB_connect(updater_list, database=archive.yearly_database_dict[year]['database'])
    return True
        

if __name__ == '__main__': 
    upload_dwg_list_content()
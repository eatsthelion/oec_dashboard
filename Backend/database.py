import os
import json
import sqlite3
from datetime import datetime
from tkinter import messagebox

from Backend.locator import LOCATION

DBLOCATION  = os.path.join(LOCATION, 'Databases')
DATABASE    = os.path.join(LOCATION, 'oec.db')
ITEMCATALOG = os.path.join(LOCATION, 'itemcatalog.db')
DOCCATALOG  = os.path.join(LOCATION, 'oec_documents.db')
PROJECTDB  = os.path.join(LOCATION, 'oec_projects.db')
PACKAGEDB = os.path.join(LOCATION, 'project_packages.db')
STATUSDB = os.path.join(LOCATION, 'project_statuses.db')
DOCDB = os.path.join(LOCATION, 'project_documents.db')
EMPLOYEEDB = os.path.join(LOCATION, 'oec_staff.db')

TIME12HR = '%I:%M %p'
TIME24HR = '%H:%M:%S'
DBTIME = '%Y-%m-%d'+' '+TIME24HR
REGTIME = '%m/%d/%y'
USERTIME = REGTIME+" "+TIME12HR
DISPLAYTIME = REGTIME + ' at ' + TIME12HR

EMPTYLIST = ['', None, 'None','none', 'nan', 'Nan', 'NaN']

with open(r".\Assets\database_locations.json", 'r') as f:
    DBDICT = json.load(f)

for database in DBDICT:
    DBDICT[database] = os.path.join(LOCATION, DBDICT[database])

def DB_attach(sql_str:str) -> str:
    for key in DBDICT:
        sql_str = sql_str.replace(key, DBDICT[key])
    return sql_str

def DB_connect2(database, sql_statement, sql_params:dict or tuple = None):
    sql_txt = sql_statement
    sql_statement = DB_attach(sql_statement)
    sql_statement = sql_statement.strip(';').split(';')
    if not sql_statement:
        return False
    conn = sqlite3.connect(database)
    try:
        c = conn.cursor()
        for s in sql_statement:
            c.execute(s,sql_params)
        if "SELECT" == s.upper().split()[0]:
            records = c.fetchall()
            return records
        return True
    except Exception as e:
        messagebox.showerror('Database Locked!',
            'The database is currently locked. Please try again later.' + \
            f'\n\n{e}\n\n{database}\n\n{sql_txt}')
        return False
    finally:
        conn.commit()
        conn.close()

def DB_connect(sql_str:str or list, sql_dict:dict = {}, 
    database:str = DATABASE,  debug:bool=False, 
    attach:str or list = None, detach:str or list = None):

    if (type(sql_str) == str) and (';' in sql_str):
        sql_str = sql_str.split(';')

    if debug: print(database)
    conn = sqlite3.connect(database)

    # Attaches additional databases
    c = conn.cursor()
    if attach != None:
        if type(attach)==list:
            for a in attach:
                c.execute(a)
        else:
            c.execute(attach)
        conn.commit()

    if debug:
        if sql_dict != {}: c.execute(sql_str,sql_dict)
        elif type(sql_str) == list: 
            for stritem in sql_str:
                if stritem == '': continue
                c.execute(stritem)
        else: c.execute(sql_str)
    else:
        try: 
            if sql_dict != {}: c.execute(sql_str,sql_dict)
            elif type(sql_str) == list: 
                for stritem in sql_str:
                    if stritem == '': continue
                    try: c.execute(stritem)
                    except: print('ERROR ON QUERY:', stritem)
            else: c.execute(sql_str)
        except:
            messagebox.showerror('Database Locked!',
            'The database is currently locked. Please try again later.' + \
            f'\n\n{database}\n\n{sql_str}'
            )
            conn.commit()
            conn.close()
            return False
    
    if type(sql_str) == str:
        sql_list = sql_str.split()
        if ('SELECT' in sql_list[0].upper()) or ('PRAGMA'== sql_list[0].upper()):
            records = c.fetchall()
            conn.commit()
            conn.close()
            return records

    if detach != None:
        c.execute(detach)
    
    conn.commit()
    conn.close()    
    return True

def get_DB_columns(table, database):
    conn = sqlite3.connect(database)
    c = conn.cursor()
    c.execute("PRAGMA table_info('{}')".format(table))
    columns = c.fetchall()
    conn.commit()
    conn.close()
    return columns

def DB_dictionary(table, database, columntitles):
    DB_dict = {}
    column_list = get_DB_columns(table, database)
    if len(column_list)!=len(columntitles): raise IndexError
    for col in range(len(column_list)): DB_dict[columntitles[col]] = {'col':column_list[col][1], 'index':column_list[col][0]}
    return DB_dict

def DB_database_find_replace(table, database, find_value, replace_value):
    columnlist = DB_connect("PRAGMA table_info('{}')".format(table), database=database)
    update_list = []
    for column in columnlist:
        update_list.append("UPDATE {} SET {}='{}' WHERE {} = '{}'".format(table, column[1], replace_value, column[1], find_value))
    DB_connect(update_list, database=database)

def DB_column_find_replace(table, column, database, find_value, replace_value):
    DB_connect("UPDATE {} SET {}='{}' WHERE {} = '{}'".format(table, column, replace_value, column, find_value), database=database)

def DB_clean_str(string):
    return string.replace("'","''").strip('\n').strip()

def format_data(data, format_type):
    new_data = str(data)
    if format_type == 'date':
        try:
            new_data = datetime.strptime(data,DBTIME).strftime(USERTIME)
        except:
            pass
    elif format_type == 'hml':
        hml = {1:"LOW", 2:"MEDIUM", 3:'HIGH'}
        try:
            new_data = hml[data]
        except:
            pass 
    elif format_type == 'taskboard':
        if data:
            new_data = 'Posted'
        else:
            new_data = 'Not Posted'
    elif format_type == 'percent':
        try:
            new_data = f"{(100*data):.1f}%"
        except:
            pass
    elif format_type == 'dollar':
        try:
            new_data = f"${data:,.2f}"
        except:
            pass
    return new_data

if __name__ == '__main__':
    DB_database_find_replace('project_info', PROJECTDB, 'nan', '')
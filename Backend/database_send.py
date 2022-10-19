import os
from datetime import date, datetime
from Backend.database import DBTIME, DISPLAYTIME, STATUSDB, DB_clean_str, DB_connect

def send_project_status(project_id:int, statuses:str, status_type:str, 
    user:object=None) -> None:
    """Sends a status update for a project to the project database.
    """
    if user == None:
        modifier = os.getlogin().upper()
    else:
        modifier = user.user_id
    tt = datetime.today().strftime(DBTIME)
    statuses = DB_clean_str(statuses)
    sql_array = f"""INSERT INTO project_status_log VALUES
    ('{project_id}', '{statuses}', '{status_type}', 
    '{tt}', '{tt}', '{modifier}')"""
    DB_connect(sql_array, database=STATUSDB)

def project_input_entry(project_id:int, table:str, database:str, 
    insert_vals:str, status_str:str, status_tag:str, 
    user:object=None) -> None:
    """ Inputs entries in our project database.
    
        project_id: The rowid of the observation in the specified data table
        table: The table of the data observation
        database: The database filepath of the data observation
        status_tag: The status type of the entry edit
        datepairs: a list of tuples that contains observation schedule data
        skippudates: a list of data fields that need to be skipped for status updates
        user: The user token of the current user
        """
    if user==None:
        user_id = os.getlogin().upper()
    else:
        user_id = user.user_id

    tt = datetime.today().strftime(DBTIME)
    sql_insert = f"""INSERT INTO {table} VALUES 
    ({DB_clean_str(insert_vals)}, '{tt}', '{tt}', '{user_id}')"""

    DB_connect(sql_insert, database=database)
    send_project_status(project_id, status_str, status_tag, user=user)
    return

def project_edit_entry(project_id:int, entry_id:int, table:str, database:str,   
    name:str, status_tag:str, datapairs:list, datelist:list=None,
    skipupdates:list=[], date_status_type:str='', user:object=None) -> None:
    """ Updates entries in our project database.
        
        project_id: The rowid of the project the observation is under
        entry_id: The rowid of the observation in the specified data table
        table: The table of the data observation
        database: The database filepath of the data observation
        name: The name of the changed data observation
        status_tag: The status type of the entry edit
        datapairs: a list of tuples the contains observation data
            Datapair format: 
            (0. Old Data, 1. New Entry Data, 2. Status Name, 3. Database Name)
            Datepair format:
            (0. Old Data, 1. New Entry Data, 2. Status Name, 3. Database Name)
        datelist: a list of tuples that contains observation schedule data
        skippudates: a list of data fields that need to be skipped for 
            status updates
        user: The user token of the current user """
    
    updates = ''
    statuses = ''
    for dp in datapairs:
        if dp[0]==dp[1]:
            continue
        updates += f"{dp[3]} = '{dp[1]}', "
        # Data is changed
        if dp[0]!='':
            statuses += f"\n\n{name}'s {dp[2]} updated from {dp[0]} to {dp[1]}."
        # Data is removed
        elif dp[1] == "":
            statuses += f"\n\n{name}'s {dp[2]} was removed.\nRemoved Info:\n{dp[0]}"
        # Data is set
        else:
            statuses += f"\n\n{name}'s {dp[2]} was set to {dp[1]}."

    date_statuses = ''
    if datelist != None:
        for dp in datelist:
            try:
                comp_date = datetime.strptime(dp[0], DBTIME)
            except:
                comp_date = None
            
            outcome = dp[1].compare_dates(comp_date)
            if outcome != None:
                try:
                    date_entry = dp[1].get()
                    podate = date_entry.strftime(DBTIME)
                except:
                    podate = ''
                updates+=f"{dp[3]} = '{podate}', "
            
            if outcome == 'updated':
                date_statuses += f"\n\n{name} updated its {dp[2]} date from " + \
                    comp_date.strftime(DISPLAYTIME) + \
                    date_entry.strftime(" to " + DISPLAYTIME)

            elif outcome == 'set':
                date_statuses += f"\n\n{name} set its {dp[2]} date on " + \
                    date_entry.strftime(DISPLAYTIME)

            elif outcome == 'removed':
                date_statuses += f"\n\n{name} removed its {dp[2]} date on " + \
                    comp_date.strftime(DISPLAYTIME)

    if updates == '':
        return False

    if user==None:
        user_id = os.getlogin().upper()
    else:
        user_id = user.user_id

    tt = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    updates += f"modify_date = '{tt}', "
    updates += f"last_modified_by = '{user_id}' "
    sql_update = f"UPDATE {table} SET {updates.strip(', ')} " + \
        f"WHERE rowid = {entry_id}"

    # Updates the database and project statuses
    DB_connect(sql_update, database=database)
    if (statuses != '') or (date_statuses != ''):
        if date_status_type == '': 
            statuses += date_statuses
            send_project_status(project_id, statuses, status_tag, user=user)
            return
        if statuses != '':
            send_project_status(project_id, statuses, status_tag, user=user)
        if date_statuses != '':
            send_project_status(project_id, date_statuses, status_tag, user=user)

    return
        
from tkinter import messagebox
from datetime import datetime 

from Backend.database import DOCDB, PACKAGEDB, DB_connect, PROJECTDB
from Backend.database_get import get_package_from_document, get_project_from_document, get_project_from_package
from Backend.database_send import send_project_status

def delete_project(data:tuple, user_id:int):
    """Deletes a project from showing up in the Catalog. The data
        still exists within our systems, but it will not appear within
        the application."""
    # Confirmation of project deletion
    if not messagebox.askyesno("Delete Project?", 
        f"Are you sure you want to delete Project {data[1]}?"): 
            return False
    
    # Gathers date of change
    date = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    # Applies changes
    DB_connect([
        f"""UPDATE project_info 
        SET active_status = 'DELETED', 
        oec_job = '{data[1]+'-DELETED'}'
        WHERE rowid = '{data[0]}'""",
        f"""INSERT INTO project_status_log VALUES 
        ('{data[0]}', 'Project {data[1]} was deleted.', 
        'DELETED', '{date}', '{date}', '{user_id}')""" ],
        database=PROJECTDB)

def delete_change_order(data:tuple, project_id:int) -> None:
    """Deletes a change order from showing up in the Catalog. The data
    is permanently deleted from our systems."""
    # Confirmation of project deletion
    if not messagebox.askyesno("Delete Change Order?", 
        f"Are you sure you want to delete Change Order {data[1]}?"): 
        return

    # Applies changes
    DB_connect(
        f"""DELETE FROM change_order_log
        WHERE rowid = '{data[0]}'""",
        database=PROJECTDB)

    send_project_status(project_id, f'CO {data[1]} was deleted.',
        "CHANGE ORDER DELETED")
    return 

def delete_purchase_order(data:str, project_id:int) -> None:
    """Deletes a purchase order in the database. The data
    is permanently deleted from our systems."""
    # Confirmation of purchase order deletion
    if not messagebox.askyesno("Delete Purchase Order?", 
        f"Are you sure you want to delete Purchase Order {data[1]}?"): 
        return

    DB_connect(
        f"""DELETE FROM project_budget
        WHERE rowid = '{data[0]}'""",
        database=PROJECTDB)

    send_project_status(project_id, f'PO {data[1]} was deleted.',
        "PURCHASE ORDER DELETED")

def delete_project_person(person_id, project_id):
    pass

def delete_project_package(package_id, package_name):
    """Deletes a package in the database and filing systems. The data
    is permanently deleted from our systems."""
    if not messagebox.askyesno("Delete Package?", 
        f"Are you sure you want to delete Package {package_name}? " + \
        "All files and documents contained in this package will be deleted as well."): 
        return

    project_id = get_project_from_package(package_id)
    DB_connect(
        f"""DELETE FROM packages
        WHERE rowid = '{package_id}'""",
        database=PACKAGEDB)
    DB_connect(
        f"""DELETE FROM documents
        WHERE package_id = '{package_id}'""",
        database=DOCDB
    )
    send_project_status(project_id, f'Package {package_name} and its contents were deleted.',
        "PACKAGE DELETED")

def delete_project_document(doc_id, filename, table='documents'):
    """Deletes a package in the database and filing systems. The data
    is permanently deleted from our systems."""
    if not messagebox.askyesno("Delete Package?", 
        f"Are you sure you want to delete Package {filename}? " + \
        "All files and documents contained in this package will be deleted as well."): 
        return

    project_id = get_project_from_document(doc_id)
    package_id = get_package_from_document(doc_id)
    package_name = DB_connect(
        f'SELECT name FROM packages WHERE rowid = {package_id}')[0][0]

    DB_connect(
        f"""DELETE FROM {table}
        WHERE rowid = '{doc_id}'""",
        database=DOCDB
    )
    
    send_project_status(project_id, f'{filename} in {package_name} was deleted.',
        "DOCUMENT DELETED")

def delete_schedule_event(event_id):
    pass

def delete_assigned_employee(event_id):
    pass 


from Backend.database_queries import *

def get_sql_dataset(sqlfile, filter='', sort=''):
    return 

# region Project Catalog
def get_project_info(filter: str = '', sort: str = 'ORDER BY rowid DESC') -> list:
    attach = f"ATTACH '{EMPLOYEEDB}' AS staff"
    sql_query = f"""
    {ALLPROJECTS}
    {filter}
    {sort}
    """
    return DB_connect(sql_query, database=PROJECTDB,attach=attach)

def get_my_project_info(user) -> list:
    return get_project_info(
        filter = f"""
    AND {user.user_id} IN 
    (
    SELECT staff.users.rowid
    FROM project_engineers
    LEFT JOIN staff.users
    ON project_engineers.employee_id = staff.users.rowid
    WHERE project_info.rowid = project_engineers.project_id
    )""")

def get_project_data(project_id):
    project_data = get_project_info(filter=f'AND rowid = {project_id}')
    if len(project_data) == 0:
        return []
    else:
        return project_data[0]
    
def get_people_info(project_id) -> list:
    sql_query = PROJECTCONTACTS.format(project_id)
    return DB_connect(sql_query, database=PROJECTDB)

def get_budget_info(project_id) -> list:
    sql_query = PROJECTBUDGET.format(project_id)
    return DB_connect(sql_query, database=PROJECTDB)

def get_schedule_info(filter:str = '', sort:str = '') -> list:
    attach = f"ATTACH '{EMPLOYEEDB}' AS staff"
    sql_query = f"""
    {SCHEDULEINFO}
    {filter}
    {sort}
    """
    return DB_connect(sql_query, database=PROJECTDB, attach=attach)

def get_schedule(project_id:int, sort:str = '') -> list:
    return get_schedule_info(
        filter=f'WHERE project_dates.project_id = {project_id}',
        sort=sort)
    

def get_event_info(task_id) -> tuple:
    task_data = get_schedule_info(
        filter=f'WHERE project_dates.rowid = {task_id}')
    if len(task_data) == 0:
        return []
    else:
        return task_data[0]

def get_status_log(project_id:int, table:str='project_status_log') -> list:
    sql_query = f"""
        SELECT rowid, status_change, status_type, date, 
        modify_date, last_modified_by 
        FROM {table} 
        WHERE project_id = {project_id}
        ORDER BY rowid DESC
        """
    return DB_connect(sql_query, database=STATUSDB)

def get_project_documents(project_id, filter:str = '', sort:str = '') -> list:
    attach = [f"ATTACH '{EMPLOYEEDB}' AS staff",
        f"ATTACH '{PACKAGEDB}' AS packages"]
    sql_query = f"""
    {PROJECTDOCUMENTS.format(project_id)}
    {filter}
    {sort}
    """
    return DB_connect(sql_query, database=DOCDB, attach=attach)

def get_docs_in_package(package_id:int) -> list:
    attach = f"ATTACH '{EMPLOYEEDB}' AS staff"
    sql_query = PACKAGEDOCS.format(package_id)

    return DB_connect(sql_query, database=DOCDB, attach=attach)

def get_all_packages(table='packages',filter:str = '', sort:str = ''):
    attached = f"ATTACH '{PROJECTDB}' AS project;"
    sql_query = f"""
        {PACKAGES.format(table)}
        {filter}
        {sort}
        """
    return DB_connect(sql_query, database=PACKAGEDB, attach=attached)

def get_packages(project_id:int) -> list:
    return get_all_packages(
        filter=f"WHERE p.project_id = {project_id}")

def get_package_info(package_id:int) -> tuple:
    package_data = get_all_packages(
        filter=f'WHERE project_dates.rowid = {package_id}')
    if len(package_data) == 0:
        return []
    else:
        return package_data[0]

def get_change_orders(purchase_order_id:int) -> list:
    sql_query = CHANGEORDERS.format(purchase_order_id)
    return DB_connect(sql_query, database=PROJECTDB)

# endregion

# Materials Database
def get_material_info() -> list:
    sql_query = """
    SELECT rowid, item, code, connected, description, type, reference, 
    other_data 
    FROM item_catalog"""
    return DB_connect(sql_query, database=ITEMCATALOG)

# Budget Catalog
def get_budget_catalog() -> list:
    sql_query = ALLBUDGETS
    return DB_connect(sql_query, database = PROJECTDB)

# OEC Date Schedule
def get_oec_date_catalog() -> list:
    sql_query = """SELECT 
    project_dates.rowid, project_info.oec_job, project_info.project_name, project_info.project_engineer,
    project_dates.event, project_dates.forecast_date, project_dates.actual_date, 
    project_dates.input_date, project_dates.modify_date 
    FROM project_dates 
    LEFT JOIN project_info ON project_dates.project_id = project_info.rowid 
    ORDER BY project_info.oec_job DESC"""
    return DB_connect(sql_query, database = PROJECTDB)

def get_project_from_package(package_id) -> int:
    sql_query = f"""
    SELECT project_id 
    FROM packages
    WHERE rowid = {package_id}"""
    return DB_connect(sql_query, database = PACKAGEDB)[0][0]

def get_package_from_document(doc_id) -> int:
    sql_query = f"""
    SELECT package_id
    FROM documents 
    WHERE rowid = {doc_id}"""
    return DB_connect(sql_query, database=DOCDB)[0][0]

def get_project_from_document(doc_id) -> str:
    package_id = get_package_from_document(doc_id)
    return get_project_from_package(package_id)

def get_package_name(package_id) -> str:
    sql_query = f"""
    SELECT name 
    FROM packages
    WHERE rowid = {package_id}"""
    return DB_connect(sql_query, database = PACKAGEDB)[0][0]

def get_event_packages(event_id) -> list:
    sql_query = f"""SELECT rowid, name, description, type, deletable,
        event_id, access, forecast_date, submittal_date,
        input_date, modify_date, last_modified_by 
        FROM packages
        WHERE event_id = '{event_id}'
        ORDER BY rowid DESC
        """
    return DB_connect(sql_query, database=PACKAGEDB)

def get_active_employees() -> list:
    attach = f"ATTACH '{PROJECTDB}' as projects"
    sql_query = ACTIVEEMPLOYEES
    return DB_connect(sql_query, database=EMPLOYEEDB, attach=attach)

def get_task_applicants(project_task_id:int) -> list:
    attach = f"ATTACH '{EMPLOYEEDB}' AS staff"
    sql_query = f"""
    SELECT
    app.rowid, staff.users.full_name, 
    (   
        SELECT COUNT(*)
		FROM project_task_assignments AS app
        WHERE app.project_person_id = staff.users.rowid
        AND app.assigned = 1
    ) AS assigned_tasks, 
    (   
        (SELECT COUNT(*) 
            FROM project_people
            LEFT JOIN project_info 
            ON project_people.project_id = project_info.rowid
            WHERE project_people.employee_id = staff.users.rowid 
			AND project_info.active_status = 'ACTIVE'
        )+
        (SELECT COUNT(*) 
            FROM project_engineers
			LEFT JOIN project_info ON project_info.rowid = project_engineers.project_id
            WHERE project_engineers.employee_id = staff.users.rowid 
            AND project_info.active_status = 'ACTIVE'
        )
    ) AS assigned_projects
    FROM project_task_assignments AS app
    LEFT JOIN staff.users 
    ON app.project_person_id = staff.users.rowid
    WHERE app.project_task_id = {project_task_id}
    AND app.assigned = 0
    """
    return DB_connect(sql_query, database=PROJECTDB, attach=attach)

def get_taskboard_tasks(filter:str = '', sort:str = ''):
    attach = f"ATTACH '{EMPLOYEEDB}' AS staff"
    sql_query = f"{TASKBOARD}\n{filter}\n{sort}"
    return DB_connect(sql_query, database=PROJECTDB, attach=attach, debug=True)

def get_taskboard(user_id):
    return get_taskboard_tasks(
        filter = f"""AND (
    SELECT COUNT(pa.project_task_id)
    FROM project_task_assignments AS pa
    WHERE pa.project_person_id = {user_id}
    AND pa.project_task_id = pd.rowid
) == 0""" )

def get_my_taskboard(user_id):
    return get_taskboard_tasks(
        filter = f"""AND (
    SELECT COUNT(pa.project_task_id)
    FROM project_task_assignments AS pa
    WHERE pa.project_person_id = {user_id}
    AND pa.project_task_id = pd.rowid
    AND pa.assigned = 1
) > 0""" )

def get_my_applied_tasks(user_id):
    return get_taskboard_tasks(
        filter = f"""
AND (
    SELECT COUNT(pa.project_task_id)
    FROM project_task_assignments AS pa
    WHERE pa.project_person_id = {user_id}
    AND pa.project_task_id = pd.rowid
    AND pa.assigned = 0
) > 0""" )

def get_assigned_staff(task_id):
    attach = f"ATTACH '{PROJECTDB}' as projects"
    sql_query = f"""
    SELECT users.rowid, users.full_name, 
    users.position,
    (SELECT COUNT(*) 
        FROM projects.project_task_assignments
        WHERE projects.project_task_assignments.project_person_id = users.rowid
        AND projects.project_task_assignments.assigned = 1
    ) AS assigned_tasks,
    (
        (SELECT COUNT(*) 
            FROM projects.project_people
            LEFT JOIN projects.project_info 
            ON projects.project_people.project_id = projects.project_info.ROWID
            WHERE projects.project_people.employee_id = users.rowid 
			AND projects.project_info.active_status = 'ACTIVE'
        )+
        (SELECT COUNT(*) 
            FROM projects.project_engineers
			LEFT JOIN projects.project_info ON projects.project_info.rowid = projects.project_engineers.project_id
            WHERE projects.project_engineers.employee_id = users.rowid AND projects.project_info.active_status = 'ACTIVE'
        )
    ) AS assigned_projects
    FROM users
    LEFT JOIN projects.project_task_assignments AS pa
    ON pa.project_person_id = users.rowid
    WHERE (active_status = 'Full' OR active_status = 'Part-Time')
    AND pa.project_task_id = {task_id}"""
    return DB_connect(sql_query, database=EMPLOYEEDB, attach=attach)

if __name__ == '__main__':
    print(get_taskboard(7))
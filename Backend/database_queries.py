
from Backend.database import *

ATTACHSTAFF = f"ATTACH '{EMPLOYEEDB}' AS staff;"
ATTACHPROJECTS = f"ATTACH '{PROJECTDB}' AS projects;"
ATTACHDOCS = f"ATTACH '{DOCDB} AS docs;"
ATTACHPACKAGES = f"ATTACH '{PACKAGEDB}' AS packages;"

ALLPROJECTS = """
    SELECT 
    rowid, oec_job, client_job, client,
    active_status, project_name, location, 
    (
		SELECT group_concat(staff.users.rowid, ',
')
		FROM project_engineers
		LEFT JOIN staff.users
		ON project_engineers.employee_id = staff.users.rowid
		WHERE project_info.rowid = project_engineers.project_id
	)as project_engineers_ids, 
	(
		SELECT group_concat(staff.users.full_name, ',
')
		FROM project_engineers
		LEFT JOIN staff.users
		ON project_engineers.employee_id = staff.users.rowid
		WHERE project_info.rowid = project_engineers.project_id
	)as project_engineers_all
    , 

    project_type,  current_phase,
    current_stage, current_percent_complete, creation_date, modify_date
    FROM project_info 
    WHERE NOT active_status = 'DELETED' 
    """

SCHEDULEINFO = """SELECT 
project_dates.rowid, event, description, event_type, status, 
priority, difficulty,
progress_percent,
(
    SELECT COUNT(*)
    FROM project_task_assignments AS pa
    LEFT JOIN staff.users
    ON pa.project_person_id = staff.users.rowid
    WHERE pa.project_task_id = project_dates.rowid
    AND pa.assigned = 0
) AS applied_staff_ids,
(
    SELECT group_concat(staff.users.full_name, ',
')
    FROM project_task_assignments AS pa
    LEFT JOIN staff.users
    ON pa.project_person_id = staff.users.rowid
    WHERE pa.project_task_id = project_dates.rowid
    AND pa.assigned = 1
) AS assigned_staff_names,
    forecast_date, actual_date, taskboard, input_date, 
modify_date, staff.users.full_name
FROM project_dates
LEFT JOIN staff.users
ON project_dates.last_modified_by = staff.users.rowid
"""

TASKBOARD = """SELECT
pd.rowid, pd.event, pd.description, pd.event_type, pd.priority, 
pd.difficulty, project_info.rowid, project_info.oec_job, 
project_info.project_name,
(
    SELECT group_concat(staff.users.rowid)
    FROM project_engineers
    LEFT JOIN staff.users
    ON project_engineers.employee_id = staff.users.rowid
    WHERE project_info.rowid = project_engineers.project_id
    )as project_engineers_ids, 
(
    SELECT group_concat(staff.users.full_name, ',
')
    FROM project_engineers
    LEFT JOIN staff.users
    ON project_engineers.employee_id = staff.users.rowid
    WHERE project_info.rowid = project_engineers.project_id
)as project_engineers_names,
(
    SELECT group_concat(staff.users.rowid)
    FROM project_task_assignments
    LEFT JOIN staff.users
    ON project_task_assignments.project_person_id = staff.users.rowid
    WHERE project_task_assignments.project_task_id = pd.rowid
    AND project_task_assignments.assigned = 1
)as assigned_ids,
(
    SELECT group_concat(staff.users.full_name, ',
')
    FROM project_task_assignments
    LEFT JOIN staff.users
    ON project_task_assignments.project_person_id = staff.users.rowid
    WHERE project_task_assignments.project_task_id = pd.rowid
    AND project_task_assignments.assigned = 1
)as assigned_names,
(
    SELECT group_concat(staff.users.rowid)
    FROM project_task_assignments
    LEFT JOIN staff.users
    ON project_task_assignments.project_person_id = staff.users.rowid
    WHERE project_task_assignments.project_task_id = pd.rowid
    AND project_task_assignments.assigned = 0
)as applied_ids

FROM project_dates AS pd
LEFT JOIN project_info 
ON pd.project_id = project_info.rowid
WHERE project_info.active_status='ACTIVE' 
AND pd.taskboard = 1"""

PACKAGES="""
SELECT p.rowid, p.name, p.description, p.type, p.deletable,
p.event_id, project.project_dates.event, p.access, p.forecast_date, 
p.submittal_date,
p.input_date, p.modify_date, p.last_modified_by 
FROM {} AS p
LEFT JOIN project.project_dates 
ON p.event_id = project.project_dates.rowid
"""
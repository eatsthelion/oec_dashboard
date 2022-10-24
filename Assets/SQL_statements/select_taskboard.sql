SELECT
pd.rowid, 
pd.event, 
pd.description, 
pd.event_type, 
pd.priority, 
pd.difficulty, 
project_info.rowid, 
project_info.oec_job, 
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
AND pd.taskboard = 1
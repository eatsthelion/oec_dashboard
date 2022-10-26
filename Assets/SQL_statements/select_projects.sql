ATTACH ':EMPLOYEEDB:' AS staff;
SELECT 
rowid, oec_job, client_job, client,
active_status, project_name, location, 
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
)as project_engineers_full_names, 
project_type,  current_phase,
current_stage, current_percent_complete, 
creation_date, modify_date
FROM project_info 
WHERE NOT active_status = 'DELETED'
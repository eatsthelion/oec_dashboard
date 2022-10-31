ATTACH ':EMPLOYEEDB:' AS staff;
SELECT
pe.rowid, staff.users.full_name, 
(   
    SELECT COUNT(*)
    FROM project_task_assignments AS pa
    WHERE pa.project_person_id = staff.users.rowid
    AND pa.assigned = 1
) AS assigned_tasks, 
(   
    SELECT COUNT(*) 
    FROM project_engineers
    LEFT JOIN project_info 
    ON project_info.rowid = project_engineers.project_id
    WHERE project_engineers.employee_id = users.rowid 
    AND project_info.active_status = 'ACTIVE'
) AS assigned_projects
FROM project_engineers AS pe
LEFT JOIN staff.users 
ON pe.employee_id = staff.users.rowid
WHERE pe.project_id = {}
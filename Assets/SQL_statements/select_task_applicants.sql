ATTACH ':EMPLOYEEDB:' AS staff;
SELECT
app.rowid, staff.users.full_name, 
(   
    SELECT COUNT(*)
    FROM project_task_assignments AS app
    WHERE app.project_person_id = staff.users.rowid
    AND app.assigned = 1
) AS assigned_tasks, 
(   
    SELECT COUNT(*) 
    FROM project_engineers
    LEFT JOIN project_info ON project_info.rowid = project_engineers.project_id
    WHERE project_engineers.employee_id = staff.users.rowid 
    AND project_info.active_status = 'ACTIVE'
) AS assigned_projects
FROM project_task_assignments AS app
LEFT JOIN staff.users 
ON app.project_person_id = staff.users.rowid
WHERE app.project_task_id = {}
AND app.assigned = 0
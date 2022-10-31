ATTACH ':PROJECTDB:' AS projects;
SELECT 
users.rowid, 
users.full_name, 
users.position,
(
    SELECT COUNT(*) 
    FROM projects.project_task_assignments
    WHERE projects.project_task_assignments.project_person_id = users.rowid
    AND projects.project_task_assignments.assigned = 1
) AS assigned_tasks,
(
    SELECT COUNT(*) 
    FROM projects.project_engineers
    LEFT JOIN projects.project_info 
    ON projects.project_info.rowid = projects.project_engineers.project_id
    WHERE projects.project_engineers.employee_id = users.rowid 
    AND projects.project_info.active_status = 'ACTIVE'
) AS assigned_projects
FROM users
LEFT JOIN projects.project_task_assignments AS pa
ON pa.project_person_id = users.rowid
WHERE (active_status = 'Full' OR active_status = 'Part-Time')
AND pa.project_task_id = {}
AND pa.assigned = 1
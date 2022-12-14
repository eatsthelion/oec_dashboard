ATTACH ':PROJECTDB:' as projects;
SELECT users.rowid, 
(users.first_name || ' ' ||users.last_name) AS full_name, 
users.position,
(SELECT COUNT(*) 
    FROM projects.project_task_assignments
    LEFT JOIN projects.project_dates
    ON projects.project_dates.rowid = projects.project_task_assignments.project_task_id
    LEFT JOIN projects.project_info
    ON projects.project_info.rowid = projects.project_dates.project_id
    WHERE projects.project_task_assignments.project_person_id = users.rowid
    AND projects.project_task_assignments.assigned = 1
    AND projects.project_info.active_status = 'ACTIVE'
) AS assigned_tasks,
(
    (SELECT COUNT(*) 
        FROM projects.project_engineers
        LEFT JOIN projects.project_info 
        ON projects.project_info.rowid = projects.project_engineers.project_id
        WHERE projects.project_engineers.employee_id = users.rowid 
        AND projects.project_info.active_status = 'ACTIVE'
    )
) AS assigned_projects
FROM users
WHERE active_status = 'Full' OR active_status = 'Part-Time'
ORDER BY full_name
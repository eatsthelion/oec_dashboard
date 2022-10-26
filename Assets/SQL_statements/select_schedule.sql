ATTACH ':EMPLOYEEDB:' AS staff;
SELECT 
project_dates.rowid, 
event, 
description, 
event_type, 
status, 
progress_percent, 
priority, 
difficulty, 
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
forecast_date, 
actual_date, 
taskboard, 
input_date, 
modify_date, 
staff.users.full_name  
FROM project_dates
LEFT JOIN staff.users
ON project_dates.last_modified_by = staff.users.rowid
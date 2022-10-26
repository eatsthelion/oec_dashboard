ATTACH ':EMPLOYEEDB:' AS staff;
SELECT 
t.rowid, 
t.status_change, 
t.status_type, 
date, 
t.modify_date, 
staff.users.full_name
FROM {} AS t
LEFT JOIN staff.users 
ON t.last_modified_by = staff.users.rowid
WHERE t.project_id = {}
ORDER BY t.rowid DESC
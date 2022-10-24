SELECT 
rowid, name, role, clearance, org, email, phone,
creation_date, modify_date 
FROM project_people
WHERE project_id = '{}'
ORDER BY rowid DESC
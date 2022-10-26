SELECT 
rowid, name, role, org, email, phone,
creation_date, modify_date 
FROM project_people
WHERE project_id = '{}'
ORDER BY rowid DESC
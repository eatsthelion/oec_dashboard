SELECT rowid, 
status_change, 
status_type, 
date, 
modify_date, 
last_modified_by 
FROM {table} 
WHERE project_id = {project_id}
ORDER BY rowid DESC
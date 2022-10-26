ATTACH ':EMPLOYEEDB:' AS staff;
SELECT 
documents.rowid, 
package_index, 
filename, 
file_type, 
title, 
drawing_num, 
revision, 
sheet, 
description, 
doc_purpose, 
progress, 
a.full_name AS author_name,
checked_out_by,
c.full_name AS checked_out_name,
input_date, 
modify_date, 
staff.users.full_name
FROM documents
LEFT JOIN staff.users
ON last_modified_by = staff.users.rowid
LEFT JOIN staff.users AS c
ON checked_out_by = c.rowid
LEFT JOIN staff.users AS a
ON author = a.rowid
WHERE package_id = {}
ORDER BY package_index ASC
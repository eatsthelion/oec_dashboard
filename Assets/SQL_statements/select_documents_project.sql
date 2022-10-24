SELECT 
documents.rowid, 
package_id,
filename, 
file_type, 
title, 
pkg.name AS package,
drawing_num, 
revision, 
sheet, 
documents.description, 
doc_purpose, 
progress, 
a.full_name AS author_name,
checked_out_by,
c.full_name AS checked_out_name,
documents.input_date, 
documents.modify_date, 
staff.users.full_name
FROM documents
LEFT JOIN staff.users
ON documents.last_modified_by = staff.users.rowid
LEFT JOIN staff.users AS c
ON checked_out_by = c.rowid
LEFT JOIN staff.users AS a
ON author = a.rowid
LEFT JOIN packages.packages AS pkg
ON package_id = pkg.ROWID
WHERE pkg.project_id = {}
SELECT p.rowid, 
p.name, 
p.description, 
p.type, 
p.deletable,
p.event_id, 
project.project_dates.event, 
p.access, p.forecast_date, 
p.submittal_date,
p.input_date, 
p.modify_date, 
p.last_modified_by 
FROM {} AS p
LEFT JOIN project.project_dates 
ON p.event_id = project.project_dates.rowid
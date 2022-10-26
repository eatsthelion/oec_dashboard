ATTACH ':EMPLOYEEDB:' AS staff;
SELECT 
p.rowid, oec_job, p.client_job, p.client,
p.active_status, p.project_name, p.location, 
(
    SELECT group_concat(staff.users.rowid)
    FROM project_engineers
    LEFT JOIN staff.users
    ON project_engineers.employee_id = staff.users.rowid
    WHERE p.rowid = project_engineers.project_id
)as project_engineers_ids, 
(
    SELECT group_concat(staff.users.full_name, ',
')
    FROM project_engineers
    LEFT JOIN staff.users
    ON project_engineers.employee_id = staff.users.rowid
    WHERE p.rowid = project_engineers.project_id
)as project_engineers_full_names, 
p.project_type,  p.current_phase,
p.current_stage, p.current_percent_complete, 
(
    SELECT b.billed_to_date / SUM(c.change_order_acceptance) 
	FROM project_info
    LEFT JOIN project_budget AS b
    ON b.project_id = p.rowid
    LEFT JOIN change_order_log AS c
    ON c.purchase_order = b.rowid
    WHERE b.project_id = project_info.rowid
) AS budget_percent,
p.creation_date, p.modify_date
FROM project_info AS p
WHERE NOT active_status = 'DELETED'

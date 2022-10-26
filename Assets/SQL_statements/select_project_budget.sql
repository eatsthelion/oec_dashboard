SELECT 
b.rowid, 
b.purchase_order, 
b.client_job, 
b.status, 
b.description, 
b.cwa_num, 
b.cwa_type, 
b.items, 
(
    SELECT SUM(c.change_order_submitted)
    FROM change_order_log AS c
    WHERE c.purchase_order = b.rowid
) AS proposed_amount,
(
    SELECT SUM(c.change_order_acceptance)
    FROM change_order_log AS c
    WHERE c.purchase_order = b.rowid
) AS accepted_amount,
b.billed_to_date, 
(
	(
		SELECT SUM(c.change_order_acceptance)
		FROM change_order_log AS c
		WHERE c.purchase_order = b.rowid
	) - b.billed_to_date) AS current_balance,
b.contingency, 
b.continued_from  
FROM project_budget AS b
WHERE project_id = '{}' 
ORDER BY rowid DESC
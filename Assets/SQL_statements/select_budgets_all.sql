SELECT 
project_budget.rowid, 
project_budget.purchase_order, 
project_info.oec_job, 
project_info.client_job, 
project_info.location,
project_budget.description, 
project_budget.cwa_num, 
project_budget.cwa_type, 
project_budget.status, 
project_budget.cwa_proposal_amount,
project_budget.cwa_proposal_date, 
project_budget.cwa_recieved_amount, 
project_budget.cwa_recieved_date, 
project_budget.contingency, 
project_budget.billed_to_date, 
project_budget.current_balance, 
project_budget.cwa_completion_date, 
project_budget.continued_from
FROM project_budget
LEFT JOIN project_info
ON project_budget.project_id = project_info.rowid
ORDER BY project_info.oec_job DESC
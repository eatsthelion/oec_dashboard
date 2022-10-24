SELECT 
rowid, 
purchase_order, 
client_job, 
status, 
description, 
cwa_num, 
cwa_type, 
items, 
cwa_proposal_amount, 
cwa_recieved_amount, 
billed_to_date, 
current_balance, 
contingency, 
continued_from  
FROM project_budget 
WHERE project_id = '{}' 
ORDER BY rowid DESC
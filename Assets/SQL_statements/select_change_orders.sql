SELECT rowid, 
change_order_number,
description, 
change_order_submitted, 
change_order_acceptance, 
submitted_date,
accepted_date  
FROM change_order_log
ORDER BY rowid DESC
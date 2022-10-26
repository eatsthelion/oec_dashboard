
from Backend.database import *

ATTACHSTAFF = f"ATTACH '{EMPLOYEEDB}' AS staff;"
ATTACHPROJECTS = f"ATTACH '{PROJECTDB}' AS projects;"
ATTACHDOCS = f"ATTACH '{DOCDB} AS docs;"
ATTACHPACKAGES = f"ATTACH '{PACKAGEDB}' AS packages;"

with open(r'.\Assets\SQL_statements\select_projects.sql', 'r') as f:
    ALLPROJECTS = f.read()

with open(r'.\Assets\SQL_statements\select_schedule.sql', 'r') as f:
    SCHEDULEINFO = f.read()

with open(r'.\Assets\SQL_statements\select_taskboard.sql', 'r') as f:
    TASKBOARD = f.read()

with open(r'.\Assets\SQL_statements\select_packages.sql', 'r') as f:
    PACKAGES = f.read()

with open(r'.\Assets\SQL_statements\select_project_contacts.sql', 'r') as f:
    PROJECTCONTACTS = f.read()

with open(r'.\Assets\SQL_statements\select_documents_package.sql', 'r') as f:
    PACKAGEDOCS = f.read()

with open(r'.\Assets\SQL_statements\select_change_orders.sql', 'r') as f:
    CHANGEORDERS = f.read()

with open(r'.\Assets\SQL_statements\select_project_budget.sql', 'r') as f:
    PROJECTBUDGET = f.read()

with open(r'.\Assets\SQL_statements\select_budgets_all.sql', 'r') as f:
    ALLBUDGETS = f.read()

with open(r'.\Assets\SQL_statements\select_active_employees.sql', 'r') as f:
    ACTIVEEMPLOYEES = f.read()

with open(r'.\Assets\SQL_statements\select_project_status.sql', 'r') as f:
    PROJECTSTATUS = f.read() 

with open(r'.\Assets\SQL_statements\select_documents_project.sql', 'r') as f:
    PROJECTDOCUMENTS = f.read() 

with open(r'.\Assets\SQL_statements\select_task_applicants.sql', 'r') as f:
    TASKAPPLICANTS = f.read() 

with open(r'.\Assets\SQL_statements\select_task_assignments.sql', 'r') as f:
    TASKASSIGNMENTS = f.read() 

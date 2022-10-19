import os
import openpyxl
import pandas as pd
from tkinter import messagebox

from Backend.database import PROJECTDB, DB_connect

DESKTOP = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop') 
OUTPUTFOLDER = os.path.join(DESKTOP, "OEC Workspace Outputs")
if not os.path.exists(OUTPUTFOLDER): os.mkdir(OUTPUTFOLDER)

def export_init(programtitle):
    programfolder = os.path.join(OUTPUTFOLDER, programtitle)
    if not os.path.exists(programfolder): os.mkdir(programfolder)
    return programfolder

PROJECTCATALOGFOLDER = export_init("OEC Project Catalog")
PROJECTDELIVERYFOLDER = export_init("delivery")

def export_excel_file(sheet_dict, ouputfile):
    writer = pd.ExcelWriter(ouputfile, engine = 'xlsxwriter')
    for sheet in sheet_dict:
        dataframe = pd.DataFrame(sheet_dict[sheet])
        dataframe.to_excel(writer, sheet_name = sheet)
    writer.save()

def see_all_projects(terminal): 
    # Exporting Data to a Workbook
    outputfile = os.path.join(PROJECTDELIVERYFOLDER, 'OEC Project Catalog.xlsx')

    try: 
        if os.path.exists(outputfile): os.remove(outputfile)
    except:
        messagebox.showerror('File is open', 
            """OEC Projects.xlsx is open. Please close the file 
            and try again.""")
        return False
    terminal.show_terminal()
    terminal.print_terminal('Gathering All Project Data...')
    all_data = DB_connect("""
        SELECT 
        p.oec_job, p.client_job, p.client, p.active_status, p.project_name, 
        p.location, p.project_engineer, p.current_stage, p.current_phase, 
        p.current_percent_complete, pb.purchase_order, pb.cwa_num, 
        pb.cwa_type, pb.cwa_recieved_amount, pb.current_balance
        FROM project_info AS p
        LEFT JOIN (
            SELECT MAX(rowid) as max_id, project_id
            FROM project_budget 
            GROUP BY project_id
        ) AS pb_max ON (pb_max.project_id = p.rowid)
        LEFT JOIN project_budget AS pb ON pb.rowid = pb_max.max_id 
        ORDER BY p.oec_job DESC""", 
        database=PROJECTDB)

    terminal.print_terminal(
        'Exporting Project Data to Excel Spreadsheet...')
    pandas_dict = {}

    columns = [
        'OEC No', 'Client Job', 'Client', 'Active Status', 'Title', 
        'Location', 'Project Engineer', 'Stage','Phase','Percent\nComplete', 
        'Latest Purchase Order', 'CWA', 'CWA Type', 'Recieved Amount', 
        'Current Balance'
        ]
    
    for col in range(len(columns)): 
        data_list = []
        for data in all_data: data_list.append(data[col])
        pandas_dict[columns[col]] = data_list
    pd_dataframe = pd.DataFrame(pandas_dict)
    writer = pd.ExcelWriter(outputfile, engine = 'xlsxwriter')
    pd_dataframe.to_excel(writer, sheet_name = 'Projects', index=False)

    workbook = writer.book
    sheet = writer.sheets['Projects']
    max_row, max_col = pd_dataframe.shape

    sheet.data_validation('D2:D{}'.format(max_row),{'validate': 'list', 
        'source': ['ACTIVE',' INACTIVE','ON HOLD', 'COMPLETED', 'CANCELLED']})
    bold_fmt = workbook.add_format(
        {'align':'vcenter', 'text_wrap':True, 'bold':True})
    wrap_fmt = workbook.add_format(
        {'align':'vcenter', 'text_wrap':True})
    money_fmt = workbook.add_format(
        {'align':'vcenter', 'num_format': '$#,##.00'})
    percent_fmt = workbook.add_format(
        {'align': 'vcenter', 'num_format': '0%'})

    columnwidths = [
        20, 20, 20, 20, 65,
        40, 20, 20, 20, 12,
        15, 10, 10, 20, 20
    ]

    columnformats = [
        bold_fmt, wrap_fmt, wrap_fmt, wrap_fmt, wrap_fmt,
        wrap_fmt, wrap_fmt, wrap_fmt, wrap_fmt, percent_fmt, 
        wrap_fmt, wrap_fmt, wrap_fmt, money_fmt, money_fmt
    ]

    column_settings = [{'header':column} for column in pd_dataframe.columns]
    sheet.add_table(0,0, max_row, max_col-1, 
        {'columns':column_settings, 'style':'Table Style Medium 12'})
    
    for c in range(len(columnwidths)):
        sheet.set_column(c,c, columnwidths[c], columnformats[c])
    for row in range(max_row):
        sheet.set_row(row, 45)
    writer.save()

    # Formating Workbook
    terminal.print_terminal('Formatting Project Spreadsheet...')
    workbook= openpyxl.load_workbook(outputfile)
    project_sheet = workbook['Projects'] 
    project_sheet.freeze_panes=project_sheet['E2']

    workbook.save(outputfile)
    workbook.close()

    terminal.print_terminal('Opening Project Spreadsheet...')
    os.startfile(outputfile)
    terminal.hide_terminal()

def see_all_budgets(project_id, project_title, terminal):
    terminal.show_terminal()
    terminal.print_terminal( 
        "Gathering budget data for {self.data[1]}...")
    budgets = DB_connect(
        "SELECT * FROM project_budget WHERE project_id='{}'".format(
            project_id),database=PROJECTDB)
    columns = DB_connect(
        "PRAGMA table_info('project_budget')".format(
            project_id),database=PROJECTDB)

    budget_dict = {}
    col_dict = {}
    for col in columns:
        budget_dict[col[1]]=[]
        col_dict[col[0]] = col[1]
    terminal.print_terminal(
        'Exporting budget data to Excel Spreadsheet...')
    for budget in budgets:
        for col_index in range(len(budget)):
            budget_dict[col_dict[col_index]].append(budget[col_index])
    
    sheet_dict = {'Purchase Orders':budget_dict}
    outputfile = os.path.join(PROJECTDELIVERYFOLDER,'{} Budget Info.xlsx'.format(
        project_title))
    export_excel_file(sheet_dict, outputfile)
    os.startfile(outputfile)
    terminal.print_terminal('Opening {} ...'.format(
            outputfile))
    terminal.hide_terminal()
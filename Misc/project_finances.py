
import os 
import tkinter as tk
import pandas as pd
from tkinter import filedialog

from Backend.database import EMPTYLIST, DB_connect, PROJECTDB, DB_connect2, DB_database_find_replace

def insert_purchase_orders_to_db():
    file = filedialog.askopenfilename()
    if not file: return False

    file_dataframe = pd.read_excel(file, dtype=str)
    print(file_dataframe)
    insert_query = """(
            '{}', '{}', '{}', '{}', '{}',
            '{}', '{}', '{}', '{}', '{}',
            '{}', '{}', '{}', '{}', '{}',
            '{}', '{}', '{}', '{}'), """
    insert_statement = "INSERT INTO project_budget VALUES "
    for row in range(len(file_dataframe.index)): 
        total_proposed_amt  = float(file_dataframe.iloc[row, 16])
        total_contract_amt  = float(file_dataframe.iloc[row, 25])
        total_invoiced      = float(file_dataframe.iloc[row, 26])
        contingency         = float(file_dataframe.iloc[row, 29])
        year = '20'+(str(file_dataframe.iloc[row,2]).strip())[:2]+"-01-01"
        insert_statement += insert_query.format(
            file_dataframe.iloc[row,5],                                                         # purchase_order
            '',                                                                                 # project_id                   
            str(file_dataframe.iloc[row,2]).strip(),                                            # oec_job         
            str(file_dataframe.iloc[row, 7]).replace("PG&E Order No.",'').strip(),              # client_job
            str(file_dataframe.iloc[row,3]),                                                    # location
            str(file_dataframe.iloc[row, 4]).replace("'", "''"),                                # description
            file_dataframe.iloc[row, 31],                                                       # cwa_num
            str(file_dataframe.iloc[row, 32]).replace("Lump Sum", 'LS').replace("T&M", 'TM'),   # cwa_type
            file_dataframe.iloc[row, 6],                                                        # items
            year,                                                                               # cwa_proposal_date
            total_proposed_amt,                                                                 # cwa_proposal_amount
            year,                                                                               # cwa_recieved_date
            total_contract_amt,                                                                 # cwa_recieved_amount
            round(contingency,2),                                                               # contingency
            round(total_invoiced,2),                                                            # billed_to_date
            round(total_contract_amt-total_invoiced, 2),                                        # current_balance
            year,                                                                               # cwa_completion_date
            file_dataframe.iloc[row, 30],                                                       # status      
            ''                                                                                  # continued_from
        )
    DB_connect(insert_statement.strip(', '), database=PROJECTDB)


def change_orders_from_excel():
    excelfile = r"G:\My Drive\Project Balance Report - Sep 2022.xlsx"
    co_indexes = list(zip(range(8,16), range(17,25)))
    count = 0
    co_list = []
    budgets = pd.read_excel(excelfile, dtype=str)
    #8-15, 17-24
    for i in budgets.index:
        rowid = DB_connect2(PROJECTDB, 
        f"""SELECT rowid 
        FROM project_budget 
        WHERE purchase_order = '{str(budgets.iloc[i, 5]).strip()}'""", 
        noconfirm=True)
        if (not rowid) or len(rowid)>1:
            rowid = DB_connect2(PROJECTDB, 
            f"""SELECT b.rowid 
            FROM project_budget AS b 
            LEFT JOIN project_info AS p
            ON p.rowid = p.project_id
            WHERE b.client_job = '{str(budgets.iloc[i,7]).replace("PG&E Order No.","").strip()}''""", noconfirm=True)
        if not rowid:
            continue

        count += 1

        c_count = 1
        for co in co_indexes:
            if (str(budgets.iloc[i, co[0]]) not in EMPTYLIST+[0, '0']) or (
                str(budgets.iloc[i, co[1]]) not in EMPTYLIST+[0, '0']):
                co_list.append((rowid[0][0], c_count, budgets.iloc[i, co[0]], budgets.iloc[i, co[1]]))
                c_count += 1
    
    #print(co_list)
    #print(f"{(float(count) / len(budgets.index))*100:.2f}%")
    sql_query = """INSERT INTO change_order_log VALUES """

    for co in co_list:
        sql_query += f"('{co[0]}', '{co[1]}','',  '{co[2]}', '{co[3]}', '', '', '', '', ''), "
    
    DB_connect2(PROJECTDB, sql_query.strip(', '))

def change_orders_from_budget():
    no_order_list = DB_connect2(PROJECTDB, 
    f"""
    SELECT b.rowid, b.cwa_proposal_amount, b.cwa_recieved_amount
    FROM project_budget AS b
    LEFT JOIN change_order_log AS c
    ON c.purchase_order = b.rowid
    WHERE (
        SELECT COUNT(*) 
        FROM change_order_log AS c
        WHERE c.purchase_order = b.rowid
    ) = 0
    """)

    sql_query = """INSERT INTO change_order_log VALUES """
    for order in no_order_list:
        sql_query += f"('{order[0]}', '{1}','',  '{order[1]}', '{order[2]}', '', '', '', '', ''), "
    DB_connect2(PROJECTDB, sql_query.strip(', '))

        




if __name__ == '__main__':
    DB_database_find_replace('project_budget', PROJECTDB, 'nan', '')

import os 
import tkinter as tk
import pandas as pd
from tkinter import filedialog

from Backend.database import DB_connect, PROJECTDB, DB_database_find_replace

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

        




if __name__ == '__main__':
    DB_database_find_replace('project_budget', PROJECTDB, 'nan', '')
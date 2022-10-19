#############################################################################################
# financial_statistics_visualizer.py
# 
# Created: 9/05/22
# Creator: Ethan de Leon
# Purposes:
#   - Given a dataset from Quick Books, the program is able to organize and display certain 
#     attributes in our financial data throughout a given time frame 
#   - Create graphs automatically of our financial data
# Required Installs: pandas
#############################################################################################

import os
from tkinter import messagebox

import matplotlib.pyplot as plt
import pandas as pd

from datetime import datetime
from Backend.exports import export_init

PROGRAMTITLE = 'OEC Financial Visualizer'
PROGRAMFOLDER = export_init(PROGRAMTITLE)

FINANCEFILE = r'C:\Users\ethan\Documents\Profit and Loss - All Dates.xlsx'


class FinancialVisualizer():
    def __init__(self):
        pass

    def create_financial_graphs(self, file, fields_of_interest=['Total Income', 'Total Expenses']):
        financefile, outputfile = FinancialVisualizer.open_file_for_pd(file)
        if outputfile == False: return False

        # Obtains the CPI Library and updates the contents to be the most up to date. 
        print('Obtaining CPI Library...')
        from cpi import update, inflate
        print('Gathering latest CPI data...')
        update()
        
        lowercase_fields = [x.lower() for x in fields_of_interest]
        row_dict = {}

        print('Finding Observations...')
        for row in range(1,len(financefile.index)):
            for field in lowercase_fields:
                if field.upper() in str(financefile.iloc[row,0]).upper(): 
                    row_dict[field] = {'row':row, 'raw':[], 'inflated':[]}
                    break
        yearlist = list(range(2002, int(datetime.today().strftime("%Y"))+1))
        thisyear = int(datetime.today().strftime('%Y'))
        as_of_time = ' (as of {})'.format((datetime.today()).strftime("%B %d, %Y"))

        print('Gathering Observation Data...')
        for field in lowercase_fields:
            for col in range(1,len(financefile.columns)-1):
                row_dict[field]['raw'].append(financefile.iloc[row_dict[field]['row'],col])
                try: 
                    row_dict[field]['inflated'].append(
                        inflate(financefile.iloc[row_dict[field]['row'],col],yearlist[col],to=thisyear-1))
                except:
                    row_dict[field]['inflated'].append(
                        financefile.iloc[row_dict[field]['row'],col])
        
        # Calculates Total Profits if both the Total Income/Revneu and Total Expenses are inputed
        if ('total income' in lowercase_fields) and ('total expenses' in lowercase_fields):
            print('Computing Profit Calculations...')
            row_dict['Total Profit'] = {'raw':[], 'inflated':[]}
            for col in range(len(financefile.columns)-2):
                row_dict['Total Profit']['raw'].append(row_dict['total income']['raw'][col]-row_dict['total expenses']['raw'][col])
                row_dict['Total Profit']['inflated'].append(row_dict['total income']['inflated'][col]-row_dict['total expenses']['inflated'][col])
        
            #FinancialVisualizer.create_bar_graph(yearlist,row_dict[field]['raw'],field.title(), 'Year', title)
        
        print('Exporting findings to Excel File...')
        raw_data = {'Year':yearlist}
        inflation_data = {'Year':yearlist}
        for field in row_dict:
            raw_data[field.title()] = row_dict[field]['raw']
            inflation_data[field.title()] = row_dict[field]['inflated']

        raw_dataframe = pd.DataFrame(raw_data)
        inflation_dataframe = pd.DataFrame(inflation_data)
        writer = pd.ExcelWriter(outputfile, engine = 'xlsxwriter')
        raw_dataframe.to_excel(writer, sheet_name = 'Raw Data')
        inflation_dataframe.to_excel(writer, sheet_name = 'Adjusted for Inflation')
        writer.save()

        print('Graphing findings to line graphs...')
        yearliststrs = [str(x) for x in yearlist]
        for field in row_dict:
            plt.plot(yearliststrs,row_dict[field]['raw'], label='Raw Data')
            plt.plot(yearliststrs,row_dict[field]['inflated'], label='Adjusted for Inflation')
            plt.legend()
            plt.title("{} per Year".format(field.title()) + as_of_time)
            plt.xlabel('Year')
            plt.ylabel(field.title())
            plt.grid(True)
            plt.show()

        os.startfile(outputfile)

    def create_bar_graph(x,y, xlabel, ylabel, title):
        #plt.bar(x, y)
        #plt.title(title)
        #plt.xlabel(xlabel)
        #plt.ylabel(ylabel)
        #plt.grid(True)
        #plt.show()
        x_series = pd.Series(y)

        plt.figure()
        
        ax = x_series.plot(kind="bar")
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_xticklabels(x)

        rects = ax.patches

        # Make some labels.
        labels = []
        for yval in y: labels.append('${:.2} Mil.'.format(float(yval)/1000000))

        for rect, label in zip(rects, labels):
            height = rect.get_height()
            ax.text(
                rect.get_x() + rect.get_width() / 2, height + 5, label, ha="center", va="bottom"
            )
        plt.grid()
        plt.show()

    def create_line_graph(x,y,x1,y1,xlabel,ylabel,title):
        plt.plot(x, y)
        plt.plot(x1, y1)
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.grid(True)
        plt.show()

    def open_file_for_pd(file):
        try: financefile = pd.read_excel(file)
        except: return False

        # Checks if file is open or exists. If the file exists, then the program tries to remove the file.
        # If the file is currently open, an error will appear, prompting the user to close the file.
        outputfile = os.path.join(PROGRAMFOLDER, 'Total Finances {}.xlsx'.format(datetime.today().strftime('%m-%d-%Y')))
        if os.path.exists(outputfile):
            try: os.remove(outputfile)
            except: 
                messagebox.showerror('File is Open', '{} is currently open. Please close the file.'.format(outputfile))
                return False, False

        return financefile, outputfile

    def find_expenses(self, file):
        financefile, outputfile = FinancialVisualizer.open_file_for_pd(file)

        # Find the years to analyze
        yearlist = list(range(2002, int(datetime.today().strftime("%Y"))+1))
        thisyear = int(datetime.today().strftime('%Y'))
        as_of_time = ' (as of {})'.format((datetime.today()).strftime("%B %d, %Y"))
        # Find the limits of the expense

        # Find the find total expense

        # Find percentage of each expense to total expense

        pass

        
program = FinancialVisualizer()
program.create_financial_graphs(FINANCEFILE,fields_of_interest=['Total 6100 Payroll & Payroll Taxes'])
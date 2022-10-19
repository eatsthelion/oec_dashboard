import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import dateutil.relativedelta
from Backend.database import DB_connect, PROJECTDB
from Backend.exports import OUTPUTFOLDER, export_init

PROGRAMTITLE = 'OEC Project Statistics'
PROGRAMFOLDER = export_init(PROGRAMTITLE)

def projects_per_year_graph():
    years = list(range(2004, int((datetime.today()).strftime("%Y"))+1))
    jobs_per_year = []
    sql_query = "SELECT count(*) FROM project_info WHERE creation_date BETWEEN '{}-01-01 00:00:00' AND '{}-12-31 23:59:59'"
    year_list = []
    for year in years:
        try: 
            jobs_per_year.append(DB_connect(sql_query.format(year, year), database=PROJECTDB)[0][0])
            year_list.append(str(year))
        except: continue

    plt.plot(year_list, jobs_per_year)
    plt.title('Number of Jobs Recieved vs. Year (as of {})'.format((datetime.today()).strftime("%B %d, %Y")))
    plt.xlabel('Year')
    plt.ylabel('Number of Jobs Recieved')
    plt.grid(True)
    plt.show()


    outputfile = os.path.join(PROGRAMFOLDER, 'Projects per Year {}.xlsx'.format(datetime.today().strftime('%m-%d-%Y')))
    pandas_dict = {'Year':years, 'Project Count':jobs_per_year}
    pd_dataframe = pd.DataFrame(pandas_dict)
    writer = pd.ExcelWriter(outputfile, engine = 'xlsxwriter')
    pd_dataframe.to_excel(writer, sheet_name = 'Project Counts')
    writer.save()
    os.startfile(outputfile)

def projects_dates_last_quarter():
    sql_querry = "SELECT count(*) FROM project_dates WHERE (actual_date BETWEEN {})"
    quarter_dict = {
        'Q1':"'{}-01-01 00:00:00' AND '{}-03-30 23:59:59'",
        'Q2':"'{}-04-01 00:00:00' AND '{}-06-30 23:59:59'",
        'Q3':"'{}-07-01 00:00:00' AND '{}-09-30 23:59:59'",
        'Q4':"'{}-10-01 00:00:00' AND '{}-12-31 23:59:59'",
        }
    
    # determines what quarter we are currently in
    today = datetime.today()
    current_quarter = None
    for q in quarter_dict:
        q_bound = quarter_dict[q].split(' AND ')
        if not (today >= datetime.strptime(q_bound[0].format(today.strftime('%Y')),"'%Y-%m-%d %H:%M:%S'") and 
                today <= datetime.strptime(q_bound[1].format(today.strftime('%Y')),"'%Y-%m-%d %H:%M:%S'")): continue
        current_quarter = q
        break

    previous_year = int(today.strftime('%Y'))-1
    q_number = int(current_quarter.replace('Q',''))
    year_list = []

    for c in range(0,5):
        if q_number > c: year_list.append(previous_year+1)
        else: year_list.append(previous_year)

    q_dict_list = []
    for q in quarter_dict: q_dict_list.append(q)

    q_between_dates = []
    for q in q_dict_list:
        year = year_list[q_dict_list.index(q)]
        q_between_dates.append(quarter_dict[q].format(year, year))

    sort_order = []
    for qb in q_between_dates:
        q_bound = qb.split(' AND ')
        sort_order.append(datetime.strptime(q_bound[0], "'%Y-%m-%d %H:%M:%S'"))
    
    sort_order.sort()

    entry_array = []
    quarter_list = []
    for sort in sort_order:
        for qb in q_between_dates:
            if datetime.strftime(sort, "'%Y-%m-%d %H:%M:%S'") not in qb: continue

            entry_array.append(sql_querry.format(qb))
            quarter_list.append(q_dict_list[q_between_dates.index(qb)]+'-'+str(year_list[q_between_dates.index(qb)]))
            break
    
    number_of_jobs_list = []
    for entry in entry_array: number_of_jobs_list.append(DB_connect(entry, database=PROJECTDB)[0][0])
    
    plt.bar(quarter_list, number_of_jobs_list)
    plt.title('Number of Milestones Reached vs. Previous Quarters (as of {})'.format((datetime.today()).strftime("%B %d, %Y")))
    plt.xlabel('Quarter')
    plt.ylabel('Number of Milestones Reached')
    plt.grid(True)
    plt.show()

def project_dates_months(months=3):
    d = datetime.today()
    sql_querry = "SELECT count(*) FROM project_dates WHERE (actual_date BETWEEN '{} 00:00:00' AND '{} 23:59:59')"
    entry_array = []
    month_list = []
    for month in reversed(range(1,months+1)):
        current_month = d-dateutil.relativedelta.relativedelta(months=month)
        entry_array.append(sql_querry.format(
        datetime.strftime(current_month,'%Y-%m-01'),
        datetime.strftime(current_month,'%Y-%m-31')
        ))
        month_list.append(datetime.strftime(current_month,'%B\n%Y'))


    number_of_jobs_list = []
    for entry in entry_array: number_of_jobs_list.append(DB_connect(entry, database=PROJECTDB)[0][0])
    
    plt.bar(month_list, number_of_jobs_list)
    plt.title('Number of Milestones Reached vs. Previous {} Months (as of {})'.format(months, (datetime.today()).strftime("%B %d, %Y")))
    plt.xlabel('Month')
    plt.ylabel('Number of Milestones Reached')
    plt.grid(True)
    plt.show()

def most_used_phrases():
    titles = DB_connect(
        """SELECT project_name FROM project_info""", database=PROJECTDB, debug=True
    )

    descriptions = DB_connect(
        """SELECT description FROM project_budget""", database=PROJECTDB, debug=True
    )

    titles_and_descriptions = titles + descriptions

    phrase_dict = {}
    for entry in titles_and_descriptions:
        whole_phrase = entry[0].upper().replace('(','').replace(')','')
        print('Analyzing', whole_phrase)
        word_list = whole_phrase.split(' ')
        phrase_list = []
        if len(word_list)==1:
            if whole_phrase not in phrase_dict:
                phrase_dict[whole_phrase] = 1
            else:
                phrase_dict[whole_phrase] +=1
            print('Phrases from {}: 1'.format(whole_phrase))
            continue

        for word_index in range(len(word_list)):
            if word_index <= len(word_list):
                for next_word_index in range(word_index+1, len(word_list)+1):
                    ph = word_list[word_index:next_word_index]
                    phrase = ph[0]
                    for p in ph[1:]: phrase+=" "+p
                    phrase = phrase.strip()
                    if phrase in phrase_list: continue
                    phrase_list.append(phrase)
                    if phrase not in phrase_dict:
                        phrase_dict[phrase] = 1
                    else:
                        phrase_dict[phrase] += 1
            else:
                ph = word_list[word_index]
                phrase = ph.strip()
                if phrase in phrase_list: continue
                phrase_list.append(phrase)
                if phrase not in phrase_dict:
                    phrase_dict[phrase] = 1
                else:
                    phrase_dict[phrase] += 1
        print('Phrases from {}:'.format(whole_phrase),len(phrase_list))
        print(phrase_list)

    pandas_dict = {'Phrase':[], 'Count':[]}
    for phrase in phrase_dict: 
        if phrase =='': continue
        pandas_dict['Phrase'].append(phrase)
        pandas_dict['Count'].append(phrase_dict[phrase])

    outputfile = os.path.join(OUTPUTFOLDER,'Most Used Project Phrases.xlsx')
    phrase_dataframe = pd.DataFrame(pandas_dict)
    writer = pd.ExcelWriter(outputfile, engine = 'xlsxwriter')
    phrase_dataframe.to_excel(writer, sheet_name = 'Most Used Phrases')
    writer.save()
    os.startfile(outputfile)
    
if __name__=='__main__':
    most_used_phrases()
import os
import pandas as pd
from datetime import datetime
from Backend.database import DOCCATALOG, DB_connect, DATABASE, ITEMCATALOG

EMPTYLIST = ["None", None, 'nan', '']

file = r'D:\My Drive\Databases\drawing_info.csv'

csvfile = pd.read_csv(file)
sqlinsert = """INSERT INTO documents VALUES ('{}',
    '{}',
    '{}',
    '{}',
    '{}',
    '{}', 
    '{}',
    '{}',
    '{}',
    '{}',
    '{}',
    '{}',
    '{}',
    '{}',
    '{}',
    '{}',
    '{}',
    '{}',
    '{}') """

SQLUPDATE = "UPDATE documents SET dwg_num = '{}' WHERE rowid = '{}'"

def entryinsert(csvfile, entry):
    file = csvfile.iloc[entry,1]
    if file in [None, '', 'None', 'nan']: return False
    if not os.path.exists(file): return False

    file_address = file
    file_name = os.path.basename(file)
    _, file_type = os.path.splitext(file)
    file_type=file_type.lstrip('.').upper()

    file_owner = ''
    try: last_modified = datetime.fromtimestamp(os.path.getmtime(file)).strftime( '%Y-%m-%d %H:%M:%S')
    except: last_modified = ''
    try:created_date = datetime.fromtimestamp(os.path.getctime(file)).strftime( '%Y-%m-%d %H:%M:%S')
    except: created_date = ''
    try: 
        int(csvfile.iloc[entry,0])
        dwg_num = csvfile.iloc[entry,0]
    except: dwg_num = ''
    if csvfile.iloc[entry,3] in EMPTYLIST: doc_title=''
    else: doc_title = csvfile.iloc[entry,3]

    if int(csvfile.iloc[entry,2]) <1: rev = 1
    else: rev = csvfile.iloc[entry,2]

    if (csvfile.iloc[entry,9] not in EMPTYLIST) and (type(csvfile.iloc[entry,9])==str):
        if 'INDOOR' in csvfile.iloc[entry,9]: department = 'INDOOR'
        elif 'OUTDOOR' in csvfile.iloc[entry,9]: department = 'OUTDOOR'
        elif 'CIVIL' in csvfile.iloc[entry,9]: department = 'CIVIL'
        elif 'REF' in csvfile.iloc[entry,9]: department = 'REFERENCE'
        else: department = ''
    else: department = ''

    new_query = sqlinsert.format(
        file_address,               #file_address                      
        file_name,                  #file_name                  
        file_type,                  #file_type                  
        dwg_num,                    #dwg_num                  
        doc_title,                  #title                              
        rev,                        #revision                              
        department,                 #department              
        '',                         #remarks                                
        csvfile.iloc[entry,6],      #client                             
        csvfile.iloc[entry,7],      #client_job                              
        csvfile.iloc[entry,8],      #oec_job  
        csvfile.iloc[entry,4],      #location  
        csvfile.iloc[entry,10],     #upload_date  
        file_owner,                 #file owner
        created_date,               #create_date  
        last_modified,              #modify_date
        '',                         #last_accessed_by  
        '',                         #package id  
        ''                          #project_id                   
        )

    return new_query

def entryinsertloop():
    entry_array = []
    for entry in range(len(csvfile)):
        new_entry = entryinsert(csvfile,entry)
        if not new_entry: continue

        entry_array.append(new_entry)
        if len(entry_array)!=500: continue
        print('\n\n\n')
        for en in entry_array: print(en)
        DB_connect(entry_array,database=DOCCATALOG)
        entry_array = []

    DB_connect(entry_array,database=DOCCATALOG)

def edit_create_date():
    dataset = DB_connect('SELECT rowid, upload_date FROM documents', database=DOCCATALOG)
    entry_array = []
    for entry in range(len(dataset)):
        entry_array.append(SQLUPDATE.format(dataset[entry][1].strip(" 00:00:00")+" 00:00:00", dataset[entry][0]))
        if (len(entry_array)<5000): continue
        DB_connect(entry_array, database=DOCCATALOG, debug=True)
        
        for en in entry_array: print(en)
        entry_array = []
        print('\n\n\n')
    
    DB_connect(entry_array, database=DOCCATALOG, debug=True)
    for en in entry_array: print(en)

def edit_client_job():
    dataset = DB_connect('SELECT rowid, file_address, location FROM documents', database=DOCCATALOG)
    entry_array = []
    for entry in range(len(dataset)):

        directoryname=os.path.dirname(dataset[entry][1])
        jobText = ''
        while os.path.basename(directoryname).upper() !=dataset[entry][2].upper():
            jobText=os.path.basename(directoryname)
            directoryname=os.path.dirname(directoryname)
            
            if ((directoryname=="G:/")or(directoryname=="C:/")or(directoryname=="O:/")
                or(directoryname=="S:/")or(directoryname=="M:/")or(directoryname=="Y:/")):
                jobText=""
                break
        if 'JO' in jobText:
            jobText=jobText.replace("JO","")
            jobText = jobText.strip()
            originname = jobText
            try: 
                while (not is_int(jobText)) and jobText != "":jobText = jobText[:-1]
            except: jobText = originname
        else: jobText = ""

        entry_array.append(SQLUPDATE.format(jobText, dataset[entry][0]))
        if (len(entry_array)<10000): continue
        DB_connect(entry_array, database=DOCCATALOG)

        for en in entry_array: print(en)
        entry_array = []
        print('\n\n\n')
    
    DB_connect(entry_array, database=DOCCATALOG)
    for en in entry_array: print(en)

def is_int(number):
    try: int(number)
    except: return False
    return True

def edit_drw_number():
    dataset = DB_connect('SELECT rowid, file_address FROM documents', database=DOCCATALOG)
    entry_array = []
    for entry in range(len(dataset)):
        base = os.path.basename(dataset[entry][1])
        revTags = ['_rev',' rev','_r',' r']
        basename = base.split('.')
        try:
            basename = basename[0]
            for revT in revTags:
                basename = basename.replace(revT.upper(),' ')
                basename = basename.replace(revT.lower(),' ')
            
            basename = basename.split(' ')
            basename = basename[0]
        except: basename = base

        try: int(basename)
        except: basename = ''
        entry_array.append(SQLUPDATE.format(basename,dataset[entry][0]))
        if (len(entry_array)<10000): continue
        DB_connect(entry_array, database=DOCCATALOG, debug=True)

        for en in entry_array: print(en)
        entry_array = []
        print('\n\n\n')
    
    DB_connect(entry_array, database=DOCCATALOG)
    for en in entry_array: print(en)

def edit_packages():
    files = DB_connect("SELECT rowid, file_address FROM documents", database = DOCCATALOG)
    package_address_list = {}

    for file in files:
        file_address = file[1]
        package_name = os.path.basename(os.path.dirname(file_address))
        print(package_name)

        
edit_packages()
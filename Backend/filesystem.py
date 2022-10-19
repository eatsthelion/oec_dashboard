from datetime import datetime
import os
import shutil
from tkinter import messagebox
from Backend.database import DBTIME, DOCDB, EMPTYLIST, PACKAGEDB, DB_connect, PROJECTDB
from Backend.exports import PROJECTDELIVERYFOLDER
from Backend.path_analyzer import PathAnalyzer

PROJECTFOLDER = r'G:\PROJECT DOCUMENTS'
RETRIEVELIMIT = 100

class FileSystem():
    def clean_filepath(filestr):
        for f in '#%&{}\/$!;:\'"@<>*+`|=':
            filestr = filestr.replace(f, '')
        filestr = filestr.replace('\t', ' ').replace('\n', ' ')
        return filestr.strip()

    def open_retrieve_file(file, outputfolder, action='open'):
        if not os.path.exists(file): 
            print('Error: File {} not found'.format(file))
            return
        print('Copying {} to Delivery Folder: {}'.format(os.path.basename(file), outputfolder))
        outputfile = os.path.join(outputfolder,os.path.basename(file))
        # deleting the oldest file 
        list_of_files = os.listdir(outputfolder)
        full_path = ["log/{0}".format(x) for x in list_of_files]

        if len(list_of_files) == RETRIEVELIMIT:
            oldest_file = min(full_path, key=os.path.getctime)
            os.remove(oldest_file)
        
        # file naming
        iteration = 0
        while os.path.exists(outputfile):
            iteration += 1
            filename, file_extension = os.path.splitext(file)
            filename = os.path.basename(filename)
            outputfile = os.path.join(outputfolder, filename+" ("+str(iteration)+")"+file_extension)
        shutil.copy(file,outputfile)

        if action == 'open': os.startfile(outputfile)
        elif action == 'retrieve': os.startfile(os.path.dirname(outputfile))

    def file_projects_initialize():
        mainfolder = r'G:/'
        projectsfolder = os.path.join(mainfolder, 'CLIENT PROJECTS')
        if not os.path.exists(projectsfolder): os.mkdir(projectsfolder)
        for year in range(2004, int(datetime.today().strftime("%Y"))+1):
            yearfolder = os.path.join(projectsfolder, str(year))
            if not os.path.exists(yearfolder): os.mkdir(yearfolder)
        projects = DB_connect("SELECT oec_job, client_job, location, project_name FROM project_info", database=PROJECTDB)
        for project in projects:
            if (not project[0]) or (project[0]==''): continue
            print(project)
            project_name = project[0] + ', JO'+project[1].replace(
                '\n', ' JO').replace(
                '/', ' JO').replace(
                '\\', ' JO').replace(
                'nan', '').replace(
                ':', ',').replace(
                'TBD', '').strip()
            project_year = '20'+project[0][:2]
            project_location = project[2].replace(
                '\n', ' ').replace(
                '\\', ' ').replace(
                '/', ' ').replace(
                ':', '').replace(
                ',', ' ').strip()
            project_title = project[3].replace(
                '\n', ' ').replace(
                '\\', ' ').replace(
                '/', ' ').replace(
                ':', '').replace(
                ',', ' ').replace(
                '*',"").replace(
                '"','').replace(
                "'", '') .strip()

            if len(project_title)>100: project_title = project_title[:100]

            location_folder = os.path.join(os.path.join(projectsfolder, project_year), project_location)
            if not os.path.exists(location_folder): os.mkdir(location_folder)

            project_folder = os.path.join(location_folder, project_name+', '+project_title)
            if not os.path.exists(project_folder): os.mkdir(project_folder)

            #purchase_orders = DB_connect("SELECT purchase_order, description FROM project_budget WHERE project_id='{}'".format(project[3]), database=PROJECTDB)
            #if len(purchase_orders)==0: continue
            #for po in purchase_orders:
            #    if (po[0]==''): continue
            #    po_num = "PO"+str(po[0]).replace(
            #    '\n', ' PO').replace(
            #    '/', ' PO').replace(
            #    '\\', ' PO').replace(
            #    'nan', '').replace(
            #    ':', ',').replace(
            #    'TBD', '').strip()
            #    po_name = po[1].replace(
            #    '\n', ' ').replace(
            #    '/', ' ').replace(
            #    '\\', ' ').replace(
            #    'nan', '').replace(
            #    ':', ',').replace(
            #    'TBD', '').strip()
            #    po_folder = os.path.join(project_folder, str(po_num+", "+po_name))
            #    if not os.path.exists(po_folder): os.mkdir(po_folder)
            pass

    def get_project_folder(project_id):
        project_info = DB_connect(f"""
            SELECT location, oec_job, client_job, project_name, creation_date 
            FROM project_info
            WHERE rowid = {project_id}""", 
            database=PROJECTDB)[0]

        folder = os.path.join(PROJECTFOLDER, datetime.strptime(
            project_info[4], DBTIME).strftime("%Y"))
        
        if not os.path.exists(folder):
            os.mkdir(folder)

        foldername = \
            FileSystem.clean_filepath(project_info[0].upper()) + ', ' + \
            FileSystem.clean_filepath(project_info[1].upper()) + ', JO' + \
            FileSystem.clean_filepath(project_info[2].upper().strip(
                '\n').replace('\n', ' JO')) + ', ' + \
            FileSystem.clean_filepath(project_info[3].upper())
        if len(foldername)>90:
            foldername=foldername[:90]

        return os.path.join(folder, foldername)

    def get_package_folder(package_id, folderlist = []):
        package_info = DB_connect(f"""
            SELECT project_id, name
            FROM packages
            WHERE rowid = {package_id}""",
            database = PACKAGEDB)[0]

        foldername = FileSystem.clean_filepath(package_info[1]) 
        if len(foldername)>30:
            foldername = foldername[:30]

        #if package_info[2] not in EMPTYLIST:
        #    folderlist.append(foldername)
        #    return FileSystem.get_package_folder(package_info[2], folderlist=folderlist)
        
        package_folder = FileSystem.get_project_folder(package_info[0])
        
        if folderlist != []:
            for folder in folderlist[::-1]:
                package_folder = os.path.join(package_folder, folder)

        return os.path.join(package_folder, foldername)

    def get_project_document(document_id):
        doc_info = DB_connect(f"""
            SELECT package_id, filename
            FROM documents
            WHERE rowid = {document_id}""",
            database = DOCDB)[0]
        if doc_info[1] in EMPTYLIST:
            return False

        return os.path.join(FileSystem.get_package_folder(doc_info[0]), 
            doc_info[1])

    def deliver_project_to_desktop(source_path):
        if source_path == False:
            messagebox.showerror('Path Not Found', 
                'The item that you are looking for does not exist within our systems.')
            return False
        if not os.path.exists(source_path):
            messagebox.showerror('Path Not Found', 
                'The item that you are looking for does not exist within our systems.')
            return False
        output = os.path.join(PROJECTDELIVERYFOLDER, os.path.basename(source_path))
        if os.path.exists(output):
            if os.path.isdir(output):
                try: 
                    shutil.rmtree(output)
                except PermissionError:
                    messagebox.showerror("File Open", 
                        "One of the files in this package is currently open. " + \
                        "Please close the file.")
                    return False
            elif os.path.isfile(output):
                try:
                    os.remove(output)
                except PermissionError:
                    messagebox.showerror("File Open", 
                        "The file is currently open on your desktop. " + \
                        "Please close the file.")
                    return False

        if os.path.isdir(source_path):
            shutil.copytree(source_path, output)
        elif os.path.isfile(source_path):
            shutil.copy(source_path, output)
        os.startfile(output)

    def initialize_all_project_folders():
        projects = DB_connect("SELECT rowid FROM project_info", database=PROJECTDB)
        for project in projects:
            project_folder = FileSystem.get_project_folder(project[0])
            if not os.path.exists(project_folder):
                os.mkdir(project_folder)
            print(project_folder)
        return


if __name__ == '__main__':
    packages = DB_connect("SELECT rowid FROM packages", database=PACKAGEDB)
    for package in packages:
        package_folder = FileSystem.get_package_folder(package[0])
        if not os.path.exists(package_folder):
            os.mkdir(package_folder)
        print(package_folder)
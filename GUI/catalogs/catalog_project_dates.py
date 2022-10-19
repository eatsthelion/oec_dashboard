###################################################################################################
# catalog_budgets.py
# 
# Created: 9/09/22
# Creator: Ethan de Leon
# Purposes:
#   - Organize the database project budgets
###################################################################################################

from datetime import datetime
from GUI.widgets.terminal import Terminal
from GUI.data_table import DataTableWindow

PROGRAMTITLE = 'OEC Schedule'

COLUMNTITLES = ["Row ID", 'OEC Job #', 'Project Title', 'Project Engineer',
                'Milestone', 'Forecast Date', 'Actual Date', 
                'Input Date', 'Modify Date']

COLUMNWIDTHS = [1 , 10, 30, 20,
                30, 10, 10,
                10, 10]  

SORTOPTIONS = ['SORT BY NEWEST', 'SORT BY OLDEST','SORT BY FORECAST DATE', 
    'SORT BY ACTUAL DATE', 'SORT BY OEC NUMBER', 'SORT BY LAST MODIFIED']

SKIPFIELDS = [0]

class ProjectDates(DataTableWindow):
    def __init__(self, master, **kw) -> None:
        super().__init__(master,
        sort_function=self.sortfunction,
        left_options = self.leftoptions, 
        additional_popups = self.additonalOptions, 
        columntitles=COLUMNTITLES, columnwidths=COLUMNWIDTHS, 
        sorttypes=SORTOPTIONS,
        program_title = PROGRAMTITLE,
        skipfields=SKIPFIELDS,
        rowheight = 5, searchbar=True,
        bg='coral1', search_col_bg='cadetblue2',
        **kw)
        
    def configure(self):
        self.titlelabel.configure(font = ("montserrat extrabold",24,'bold'), 
            text="★ "+PROGRAMTITLE.upper()+" ★", bg='white',
            height=2)
        self.titlelabel.place_forget()
        self.titlelabel.pack(fill='x')
        
        super().configure()
        self.terminal = Terminal(self.frame)
        self.hide_back_button()
        self.hide_cancel_button()

    def leftoptions(master,dataset,row, obj=None):
        pass

    def rightoptions(master,dataset,row, obj=None):
        pass


    def sortfunction(self, sortby, dataset):
        if sortby == 'SORT BY FILE NAME (A-Z)': 
            named_entries = []
            nameless_entries = []
            for data in dataset:
                if data[2] in ['', None]: 
                    nameless_entries.append(data)
                    continue
                named_entries.append(data)
            named_entries.sort(key=lambda i:i[2])
            dataset = named_entries + nameless_entries
        elif sortby == 'SORT BY OEC NUMBER': dataset.sort(key=lambda i:i[1],reverse=True)
        elif sortby == 'SORT BY NEWEST': dataset.sort(key=lambda i: datetime.strptime(i[7], "%Y-%m-%d %H:%M:%S"), reverse=True)
        elif sortby == 'SORT BY FORECAST DATE': 
            datelist = []
            empty_date_list = []
            for data in dataset:
                try: 
                    datetime.strptime(data[5], "%Y-%m-%d %H:%M:%S")
                    datelist.append(data)
                except: empty_date_list.append(data)
            
            datelist.sort(key=lambda i: datetime.strptime(i[5], "%Y-%m-%d %H:%M:%S"), reverse=True)
            dataset = datelist + empty_date_list
        elif sortby == 'SORT BY ACTUAL DATE': 
            datelist = []
            empty_date_list = []
            for data in dataset:
                try: 
                    datetime.strptime(data[6], "%Y-%m-%d %H:%M:%S")
                    datelist.append(data)
                except: empty_date_list.append(data)
            
            datelist.sort(key=lambda i: datetime.strptime(i[5], "%Y-%m-%d %H:%M:%S"), reverse=True)
            dataset = datelist + empty_date_list
        elif sortby == 'SORT BY OLDEST': dataset.sort(key=lambda i: datetime.strptime(i[7], "%Y-%m-%d %H:%M:%S"))
        elif sortby == 'SORT BY LAST MODIFIED': dataset.sort(key=lambda i: datetime.strptime(i[8], "%Y-%m-%d %H:%M:%S"))
        return dataset 

    def additonalOptions(button_master, frame_master, obj=None):
        pass

if __name__ == "__main__":
    ProjectDates()
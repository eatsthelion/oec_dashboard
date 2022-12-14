###############################################################################
# catalog_users.py
# 
# Created: 9/02/22
# Creator: Ethan de Leon
# Purposes:
#   - Displays all active employees
###############################################################################

from GUI.window_datatable import *

PROGRAMTITLE = "OEC Staff"

class EmployeeDatabase(DataTableWindow):
    def __init__(self, master, **kw) -> None:
        super().__init__(master,
        sort_function=self.sortfunction,
        leftoptions = self.leftoptions, 
        additional_windows = self.additonalOptions, 
        program_title = PROGRAMTITLE,
        format_dict = 'staff',
        rowheight = 2, searchbar=True,
        bg='#7f007f', search_col_bg='mediumorchid2',
        **kw)

    def configure(self):
        super().configure()
        self.terminal = Terminal(self.frame)
        self.hide_back_button()
        self.hide_cancel_button()

    def leftoptions(self, master,dataset,row):
        
        select_button = MyButton(master, text='SELECT', 
            command=lambda m=dataset: self.select_data(m))
        if self.context == 'select':
            select_button.grid(row=0, column = 1, padx =5)

    def sortfunction(self, sortby, dataset):
        if sortby == 'SORT BY ITEM (A-Z)': 
            named_entries = []
            nameless_entries = []
            for data in dataset:
                if data[1] in ['', None]: 
                    nameless_entries.append(data)
                    continue
                named_entries.append(data)
            named_entries.sort(key=lambda i:i[1])
            dataset = named_entries + nameless_entries
        elif sortby == 'SORT BY ITEM (Z-A)': 
            dataset.sort(key=lambda i:i[1],reverse=True)
        elif sortby == 'SORT BY CODE': 
            dataset.sort(key=lambda i:i[2])
        return dataset

    def additonalOptions(self, button_master, frame_master):
        label=MyLabel(button_master, font=FONTBOLD, text='OCAMPO ★ ESTA STAFF')
        label.pack()


    def display_data(self, data, datasetget):
        if self.context != 'select':
            self.destroy_stop = False
            self.titlelabel.configure(font = ("montserrat extrabold",24,'bold'), 
                text="★ "+PROGRAMTITLE.upper()+" ★", bg='white',
                height=2)
            self.titlelabel.place_forget()
            self.titlelabel.pack(fill='x')
            self.hide_back_button()
        else:
            self.destroy_stop = True
            self.titlelabel.configure(font=FONTBOLD, text='ASSIGN STAFF')
            self.titlelabel.pack_forget()
            self.titlelabel.place(relx=.5, rely=0, anchor=N)
            self.show_back_button()

        return super().display_data(data, datasetget)

    def select_data(self, dataset):
        action = self.sender(dataset)
        if action == False:
            return False
        self.cancel_window()

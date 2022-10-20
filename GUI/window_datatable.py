from GUI.window_main import *
from GUI.widgets.new_search_window import SearchWindow

def nothing_function(*arg, **kw): 
    """Literally does nothing. Takes any and all arguments and inputs and 
    does nothing"""
    return []

class DataTableWindow(PopupWindow):
    def __init__(self, master, dataset_get=None,
            searchsystem = True, pagesystem = True,
            search_alg = None, sortfunction = None, 
            filtertypes = ['NAME','TYPE', 'DATE'],
            sorttypes=['SORT BY DATE', 'SORT A➜Z', 'SORT Z➜A'],
            entrylimit = 20, rowheight = 2, columnwidth = 15,
            skipfields = [], col_color = 'mediumorchid3', 
            leftoptions=None, rightoptions=None, additional_windows = None, 
            format_dict = {}, 
            **kw) -> None:
        """Initializes all the keyword arguments for the SearchWindow widget"""
        self.dataset_get = dataset_get
        self.searchsystem = searchsystem
        self.pagesystem = pagesystem 
        
        self.sortfunction = sortfunction
        self.filtertypes = filtertypes
        self.sorttypes = ['NO SORT'] + sorttypes
        
        self.search_algorithm = search_alg
        
        # Result Window attributes
        # Action widgets
        self.rightoptions = rightoptions
        self.leftoptions = leftoptions
        self.additional_windows = additional_windows

        # Display attributes
        self.entrylimit = entrylimit
        self.skipfields = skipfields
        self.rowheight = rowheight
        self.columnwidth = columnwidth
        self.format_dict = format_dict
        self.col_color = col_color
        super().__init__(master, **kw)

    def configure(self):
        super().configure()
        self.searchwindow = SearchWindow(self.frame, self.dataset_get,
            pagesystem=self.pagesystem, searchsystem=self.searchsystem,  
            search_alg=self.search_algorithm, sortfunction=self.sortfunction,
            entrylimit=self.entrylimit, skipfields = self.skipfields,
            rowheight = self.rowheight, columnwidth=self.columnwidth, 
            format_dict=self.format_dict, col_color=self.col_color, 
            rightoptions=self.rightoptions, leftoptions=self.leftoptions,
            additional_windows=self.additional_windows)
        self.searchwindow.pack(fill='both',expand=1)
        pass

    def display_data(self, data, dataset_get):
        """Changes the data of the SearchWindow Widget"""
        self.master.update()
        self.data = data 
        self.dataset_get = dataset_get
        self.searchwindow.dataset_get = dataset_get
        self.searchwindow.dataset = dataset_get()
        if self.pagesystem:
            self.searchwindow.first_page()
        else:
            self.searchwindow.display_sequence()
        self.reverse_format_dict()
        self.master.update()

    def reverse_format_dict(self):
        self.data_dict = {}
        for key in self.format_dict:
            if 'db' not in self.format_dict[key]:
                continue
            self.data_dict[self.format_dict[key]] = key
        return

    def show_window(self):
        self.searchwindow.refresh_page()
        return super().show_window()

    def show_full_window(self):
        self.searchwindow.refresh_page()
        return super().show_full_window()

    def go_back(self):
        self.searchwindow.dataset.clear()
        self.searchwindow.clear_display()
        super().go_back()

    def cancel_window_sequence(self):
        super().cancel_window_sequence()
        self.searchwindow.dataset.clear()
        print(self.searchwindow.dataset)
        self.searchwindow.clear_display()
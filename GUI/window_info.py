import json
from Backend.database import format_data
from GUI.window_terminal import *

class InfoWindow(TerminalWindow):
    def __init__(self, master, **kw) -> None:
        super().__init__(master, font=FONT, **kw)
        self.data = None
        self.hide_back_button()
        self.cancelbutton.configure(command=self.go_back)

    def display_data(self, dataset: list or tuple, format_dict: str = '', 
        skiprows:list = [], fg='black'):
        """datapairs: (Entry Name, Entry Data)"""
        self.dataset = dataset
        with open(r".\Assets\data_format.json") as j:
            self.format_dict = json.load(j)[format_dict]

        text = ''
        for row, data in enumerate(dataset):
            rowstr = str(row)
            if row in skiprows:
                continue
            if rowstr not in self.format_dict:
                continue
            if 'title' not in self.format_dict[rowstr]:
                continue
            if 'format' in self.format_dict[rowstr]:
                data = format_data(data,self.format_dict[rowstr]['format'])
            else:
                data = str(data)
            text += f"{self.format_dict[rowstr]['title']}: {data}\n\n"
        self.terminal.print_terminal(text)
        self.show_window()
        return

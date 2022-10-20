
from Backend.database import format_data
from GUI.window_terminal import *

class InfoWindow(TerminalWindow):
    def __init__(self, master, **kw) -> None:
        super().__init__(master, font=FONT, **kw)
        self.data = None
        self.hide_back_button()
        self.cancelbutton.configure(command=self.go_back)

    def display_data(self, dataset: list or tuple, format_dict: dict = {}, 
        skiprows:list = [], fg='black'):
        """datapairs: (Entry Name, Entry Data)"""
        self.dataset = dataset
        self.format_dict = format_dict
        text = ''
        for row, data in enumerate(dataset):
            if row in skiprows:
                continue
            if row not in format_dict:
                continue
            if 'title' not in format_dict[row]:
                continue
            if 'format' in format_dict[row]:
                data = format_data(data,format_dict[row]['format'])
            else:
                data = str(data)
            text += f"{format_dict[row]['title']}: {data}\n\n"
        self.terminal.print_terminal(text)
        self.show_window()
        return

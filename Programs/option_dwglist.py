
PROGRAMTITLE = 'Drawing List Options'

from Backend.database_get import *

from GUI.widgets.basics import *
from GUI.window_option import *

class DWGListWindow(OptionWindow):
    def __init__(self, master, **kw):
        super().__init__(master, bg='cyan4', width=400, height=250, 
        program_title = PROGRAMTITLE, **kw)
        self.data = None
        self.project_data = None

        self.apply_dwglist = MyButton(self.frame, text='APPPY DWG LIST')
        self.create_dwglist = MyButton(self.frame, text='CREATE DWG LIST')
        self.template_dwglist = MyButton(self.frame, 
            text='DOWNLOAD DWG LIST TEMPLATE')

        self.apply_dwglist.pack(fill=BOTH, padx=5, pady=5, expand = 1)
        self.create_dwglist.pack(fill=BOTH, padx=5, pady=5, expand = 1)
        self.template_dwglist.pack(fill=BOTH, padx=5, pady=5, expand = 1)

    def display_data(self, data):
        self.data = data 
        self.show_window()

    def apply_dwglist():
        pass

    

from Backend.database_get import get_project_data

from GUI.window_info import *

class BasicProjectInfo(InfoWindow):
    def __init__(self, master, **kw) -> None:
        super().__init__(master, bg='mediumorchid4', **kw)
    
    def display_data(self, project_id):
        dataset = get_project_data(project_id)
        self.titlelabel.configure(text="PROJECT INFO")
        return super().display_data(dataset, 'project_catalog')

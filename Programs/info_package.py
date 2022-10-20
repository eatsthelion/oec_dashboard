from Backend.database_get import get_package_info

from GUI.window_info import InfoWindow

from Programs.project_schedule import FORMATDICT, SKIPFIELDS

class PackageInfoWindow(InfoWindow):
    def __init__(self, master, **kw) -> None:
        super().__init__(master, bg='coral2', **kw)
    
    def display_data(self, task_id):
        dataset = get_package_info(task_id)
        self.titlelabel.configure(text="PROJECT INFO")
        return super().display_data(dataset, FORMATDICT, SKIPFIELDS)
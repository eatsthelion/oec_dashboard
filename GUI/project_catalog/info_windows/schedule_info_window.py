from Backend.database_get import get_event_info
from GUI.project_catalog.info_windows.info_window import InfoWindow
from GUI.project_catalog.project_schedule import FORMATDICT, SKIPFIELDS

class ScheduleInfoWindow(InfoWindow):
    def __init__(self, master, **kw) -> None:
        super().__init__(master, bg='coral2', **kw)
    
    def display_data(self, task_id):
        dataset = get_event_info(task_id)
        self.titlelabel.configure(text="PROJECT INFO")
        return super().display_data(dataset, FORMATDICT, SKIPFIELDS)

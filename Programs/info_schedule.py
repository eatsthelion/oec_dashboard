from Backend.database_get import get_event_info

from GUI.window_info import *

class ScheduleInfoWindow(InfoWindow):
    
    def __init__(self, master, **kw) -> None:
        super().__init__(master, bg='coral2', **kw)
    
    def display_data(self, task_id):
        dataset = get_event_info(task_id)
        self.titlelabel.configure(text="EVENT INFO")
        return super().display_data(dataset,'project_schedule')

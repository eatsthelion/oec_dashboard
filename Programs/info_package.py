###############################################################################
# info_package.py
# 
# Created: 10/19/22
# Creator: Ethan de Leon
# Purposes:
#   - Displays information regarding a package
###############################################################################

from Backend.database_get import get_package_info

from GUI.window_info import *

class PackageInfoWindow(InfoWindow):
    def __init__(self, master, **kw) -> None:
        super().__init__(master, bg='coral2', **kw)
    
    def display_data(self, task_id):
        dataset = get_package_info(task_id)
        self.titlelabel.configure(text="PROJECT INFO")
        return super().display_data(dataset, 'project_packages')
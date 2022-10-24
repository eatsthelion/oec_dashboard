from GUI.window_main import *
class OptionWindow(PopupWindow):
    def __init__(self, master: tk, **kw) -> None:
        super().__init__(master, **kw)
        self.cancelbutton.configure(command=self.go_back)
        self.hide_back_button()
        self.data_dict = None
        self.project_data_dict = None
        if self.parent == None:
            return
        try:
            self.data_dict = self.parent.data_dict
        except AttributeError:
            pass

        try:
            self.project_data_dict = self.parent.project_data_dict
        except AttributeError:
            pass
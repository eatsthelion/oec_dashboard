from GUI.window_main import *
class EditWindow(PopupWindow):
    def __init__(self, master, **kw) -> None:
        super().__init__(master, **kw)
        self.data = None
        self.hide_back_button()
        self.cancelbutton.configure(command=self.go_back)
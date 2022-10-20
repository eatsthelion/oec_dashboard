from GUI.window_main import *
class OptionWindow(PopupWindow):
    def __init__(self, master: tk, **kw) -> None:
        super().__init__(master, **kw)
        self.cancelbutton.configure(command=self.go_back)
        self.hide_back_button()
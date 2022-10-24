from GUI.widgets.terminal import Terminal
from GUI.widgets.highlight import rowhighlight
from GUI.window_main import *

class TerminalWindow(PopupWindow):
    def __init__(self, master, width=600, height=300, bg='gray60', 
        scroll_bar = True, font = (FONT[0], 18),**kw) -> None:
        super().__init__(master, width=width, height=height, bg=bg, **kw)
        self.data = None
        self.origin_widget = None
        self.terminal = Terminal(self.frame, bg=self.bg, dimensions=(60,10),
            font = font, scroll_bar=scroll_bar)
        self.terminal.pack(padx=10,pady=10)
        
    def cancel_window(self):
        rowhighlight(None, self.origin_widget, 'white', 'white')
        return super().cancel_window()

    def show_window(self, widget=None):
        super().show_window()
        if widget != None:
            rowhighlight(None, widget, 'gold3', 'gold1')
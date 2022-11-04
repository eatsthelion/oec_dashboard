###############################################################################
# edit_comment.py
# 
# Created: 8/02/22
# Creator: Ethan de Leon
# Purposes: 
#   - GUI for both inserting and modifying a comment
###############################################################################

PROGRAMTITLE = "Comment Edits"

from datetime import datetime

from Backend.database import STATUSDB, DB_connect

from GUI.window_edit import *

class EditProjectCommentGUI(EditWindow):
    def __init__(self, master,**kw) -> None:
        super().__init__(master, bg='goldenrod2', width=500, height=350, 
        program_title = PROGRAMTITLE, **kw)
        self.project_id = None
    
    def configure(self):
        self.titlelabel.configure(text='NEW COMMENT')
        self.entryframe = MyFrame(self.frame, bg=self.frame.cget('background'))
        self.entryframe.pack(expand=1)
        
        self.textbox = MyText(self.entryframe, width=50, height=8)
        self.textbox.pack(expand=1, padx=10, pady=10)

        self.enterbutton = MyButton(self.entryframe, text='ADD COMMENT',
            command=self.enter_comment)

        self.enterbutton.pack(pady=5)
        return super().configure()

    def enter_comment(self):
        new_comment = self.textbox.get()
        if new_comment == '':
            return False
        tt = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        DB_connect(f"""
            INSERT INTO project_status_log VALUES
            ('{self.project_id}', '{new_comment}', 'COMMENT', '{tt}', '{tt}',
            '{self.user.user_id}')
            """, database = STATUSDB)
        self.cancel_window()
        self.parent.searchwindow.refresh_results()
        self.parent.get_latest_comment()
        self.parent.get_latest_status()
    
    def update_comment(self):
        new_comment = self.textbox.get()
        if new_comment == '':
            return False
        if new_comment == self.data[1]:
            return False
        tt = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        DB_connect(f"""
            UPDATE project_status_log SET
            status_change = '{new_comment}' WHERE rowid = '{self.data[0]}'
            """, database = STATUSDB)
        self.cancel_window()
        self.parent.searchwindow.refresh_page()
        self.parent.get_latest_comment()
        self.parent.get_latest_status()

    def display_data(self,  project_id:int=None, data:int=None,):
        self.textbox.delete()
        self.data = data
        self.project_id = project_id
        if data !=None:
            self.data
            self.context = 'update'
            self.textbox.insert(self.data[1])
            self.enterbutton.configure(text='UPDATE COMMENT', 
                command=self.update_comment)
            self.titlelabel.configure(text='UPDATE COMMENT')
        else:
            self.context = 'insert'
            self.enterbutton.configure(text='ADD COMMENT', 
                command=self.enter_comment)
            self.titlelabel.configure(text='NEW COMMENT')
        self.show_window()
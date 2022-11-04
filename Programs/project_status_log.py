###############################################################################
# project_status_log.py
# 
# Created: 10/19/22
# Creator: Ethan de Leon
# Purposes:
#   - Displays and organizes the status log of a project
#   - Connects to
#       - edit_comment.py to insert or edit comments
###############################################################################

from Backend.database import  PROJECTDB, DB_connect

from GUI.window_datatable import *

from Programs.edit_comment import EditProjectCommentGUI

class ProjectStatusGUI(DataTableWindow):
    def __init__(self, master, **kw) -> None:
        super().__init__(master, program_title = 'Project Status Logs',
        bg='darkorange1',col_color='orange',
        leftoptions = self.leftoptions, 
        additional_windows = self.additionalOptions,
        format_dict="project_status",
        **kw)

    def configure(self, **kw):
        headerframe = MyFrame(self.frame, bg=self.bg)
        self.current_comment_frame = MyLabelFrame(headerframe, 
            text="LATEST COMMENT")
        self.current_comment_text = MyText(self.current_comment_frame,
            height=2, width=30)
        self.latest_status_frame = MyLabelFrame(headerframe, text="LATEST STATUS")
        self.latest_status_text = MyText(self.latest_status_frame, height=2, 
            width=30)
        self.current_comment_text   .insert('NO COMMENTS...')
        self.latest_status_text     .insert('NO STATUS UPDATES')
        self.current_comment_text   .configure(state=DISABLED)
        self.latest_status_text     .configure(state=DISABLED)
        self.current_comment_frame .pack(side=LEFT, padx=5,pady=5)
        self.latest_status_frame   .pack(side=LEFT, padx=5,pady=5)
        self.current_comment_text  .pack()
        self.latest_status_text    .pack()
        headerframe.pack()
        super().configure(**kw)

    def leftoptions(self, master, dataset, row):
        if dataset[2]!= 'COMMENT':
            label = MyLabel(master, fg='white', font=FONTBOLD, text='★')
            label.pack(anchor=N)
            return
        edit=MyButton(master, text='UPDATE',
            command=lambda m=dataset: self.show_comment_window(m))
        delete = MyButton(master, bg='red', fg='white', text="DELETE",
            command=lambda m=dataset[0]: self.delete_comment(m))

        edit    .grid(row=0,column=0,padx=(5,0))
        delete  .grid(row=0,column=1,padx=5)

    def additionalOptions(self, button_master, frame_master):
        self.comment_window = EditProjectCommentGUI(frame_master,parent = self)

        comment_button = MyButton(button_master, text='NEW COMMENT',
            command=self.show_comment_window)   
        all_budgets_button = MyButton(
            button_master, text='EXPORT TO EXCEL')

        all_budgets_button.pack(side='left', pady=(10,2),padx=5)
        comment_button.pack(side='left', pady=(10,2),padx=5)

    def show_comment_window(self, data=None):
        comment_window = EditProjectCommentGUI(self.frame, parent=self)
        comment_window.display_data(self.data[0], data=data)

    def display_data(self, data, datasetget):
        super().display_data(data, datasetget)
        self.get_latest_comment()
        self.get_latest_status()

    def get_latest_comment(self):
        latest_comment=False
        for datapoint in self.searchwindow.dataset:
            if datapoint[2] != 'COMMENT': 
                continue
            latest_comment = datapoint[1] 
            break
        if not latest_comment:
            latest_comment = 'NO COMMENTS...'
        self.current_comment_text.configure(state=NORMAL)
        self.current_comment_text.delete()
        self.current_comment_text.insert(latest_comment)
        self.current_comment_text.configure(state=DISABLED)

    def get_latest_status(self):
        latest_status = False
        for datapoint in self.searchwindow.dataset:
            if datapoint[2] == 'COMMENT': 
                continue
            latest_status = datapoint[1]
            break

        if not latest_status:
            latest_status = 'NO STATUS UPDATES...'
        self.latest_status_text.configure(state=NORMAL)
        self.latest_status_text.delete()
        self.latest_status_text.insert(latest_status)
        self.latest_status_text.configure(state=DISABLED)

    def delete_comment(self, rowid):
        """Deletes a comment from showing up in a project's status log.
        Comment data is permenantly deleted."""
        # Confirmation of project deletion
        if not messagebox.askyesno("Delete Comment?", 
            f"Are you sure you want to delete this comment?"): 
                return
        
        # Applies changes
        DB_connect(f"DELETE FROM project_status_log WHERE rowid = {rowid}",            
            database=PROJECTDB)

        # Refreshes display
        self.searchwindow.refresh_results()
        self.get_latest_comment()
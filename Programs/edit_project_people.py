PROGRAMTITLE = 'Contact Edits'
from Backend.database import PROJECTDB
from Backend.database_send import project_edit_entry, project_input_entry

from GUI.window_edit import *

class EditPeopleGUI(EditWindow):
    def __init__(self, master, **kw) -> None:
        super().__init__(master, bg='purple3', program_title = PROGRAMTITLE,
        **kw)
        self.data = None

    def configure(self):
        self.entryframe = MyFrame(self.frame,bg=self.bg)
        
        self.name_entry  = MyEntry(self.entryframe)
        self.role_entry  = MyEntry(self.entryframe)
        self.org_entry   = MyEntry(self.entryframe)
        self.email_entry = MyEntry(self.entryframe)
        self.phone_entry = MyEntry(self.entryframe)

        self.datapairs = [
            ('Name*:', self.name_entry),
            ("Role*:", self.role_entry),
            ("Organization:", self.org_entry),
            ("Email:", self.email_entry),
            ("Phone:", self.phone_entry),
        ]
        for row, datapair in enumerate(self.datapairs):
            label = MyLabel(self.entryframe,  text=datapair[0])
            label.grid(row=row, column = 0, padx=5, pady=(5,0), sticky=W)
            datapair[1].grid(row=row, column = 1, padx=5, pady=(5,0), sticky=EW)
        
        self.entryframe.pack(expand=1, pady=(0,5), padx=5)

        self.enterbutton = MyButton(self.frame, command = self.enter_command)
        self.enterbutton.pack(fill='x')
        super().configure()

    def enter_command(self):
        name        = self.name_entry .get()
        role        = self.role_entry .get()
        org         = self.org_entry  .get()
        email       = self.email_entry.get()
        phone       = self.phone_entry.get()

        for req in [name, role]:
            if req == '': 
                messagebox.showerror("Required Field Empty",
                "Please fill out all required fields before submitting. " + \
                "Please try again.")
                return False

        if self.context == 'input':
            status_updates = f"{name} was added to the project." + \
                f"\n{name} has the role of {role}."
            sql_query = f"""'{self.project_id}', '{name}',  
                '{role}', '{org}', '{email}', '{phone}'"""

            project_input_entry(self.project_id, 'project_people', PROJECTDB,
            sql_query, status_updates, 'NEW CONTACT', user=self.user)
            self.parent.searchwindow.refresh_results()

        elif self.context == 'modify':

            datapairs = [
                (name, 'name', 'name'),
                (role, 'role', 'role'),
                (org, 'org', 'org'), 
                (email, 'email', 'email'),
                (phone, 'phone', 'phone'),
            ]

            project_edit_entry(self.project_id, self.data[0], 'project_people',
            PROJECTDB, name, 'CONTACT INFO EDIT', self.data, self.data_dict, 
            datapairs, user=self.user)

            self.parent.searchwindow.refresh_page()

        self.cancel_window()
        

    def display_data(self, project_id, data=None):
        self.project_id = project_id

        self.name_entry.delete()
        self.role_entry.delete()
        self.org_entry.delete()
        self.email_entry.delete()
        self.phone_entry.delete()
        
        if data == None:
            self.context = 'insert'
            self.titlelabel.configure(text='NEW PROJECT MEMBER')
            self.enterbutton.configure(text='ADD PERSON')
        else:
            self.context = 'modify'
            self.data = data
            self.titlelabel.configure(text="EDIT PROJECT MEMBER")
            self.enterbutton.configure(text='UPDATE PERSON')
            self.name_entry.insert(self.data[self.data_dict['fullname']])
            self.role_entry.insert(self.data[self.data_dict['role']])
            self.org_entry.insert(self.data['org'])
            self.email_entry.insert(self.data['email'])
            self.phone_entry.insert(self.data['phone'])
        
        self.show_window()
        return
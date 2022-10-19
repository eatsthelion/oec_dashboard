
from Backend.database import EMPLOYEEDB, DB_connect

class UserToken(object):
    def __init__(self,username):
        userdata=DB_connect(f"""
            SELECT rowid, full_name, first_name, active_status, position
            FROM users
            WHERE username = '{username}'""", database=EMPLOYEEDB)[0]

        self.user_id = userdata[0]
        self.full_name = userdata[1]
        self.first_name = userdata[2]
        self.employment_status = userdata[3]
        self.position = userdata[4]
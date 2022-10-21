
from Backend.database import EMPLOYEEDB, DB_connect

class UserToken(object):
    def __init__(self,username):
        userdata=DB_connect(f"""
            SELECT u.rowid, u.full_name, u.first_name, u.active_status, 
            u.position, p.data_clearance
            FROM users AS u
            LEFT JOIN positions AS p
            ON u.position = p.position
            WHERE u.username = '{username}'""", database=EMPLOYEEDB)[0]

        self.user_id = userdata[0]
        self.full_name = userdata[1]
        self.first_name = userdata[2]
        self.employment_status = userdata[3]
        self.position = userdata[4]
        self.data_clearance = userdata[5]
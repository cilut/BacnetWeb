# import things
from flask_table import Table, Col, BoolCol


# Declare your table
class user_table(Table):
    usr = Col('Username')
    password = Col('Password')
    email = Col('Email')
    admin = BoolCol('Administrator')


class day_sch_table():
    initial_time = Col('Initial Time')
    final_time = Col('Final time')
    value = Col('Value')


# Get some objects
class row_user(object):
    def __init__(self, usr, password, email, admin):
        self.usr = usr
        self.password = password
        self.email = email
        self.admin = admin

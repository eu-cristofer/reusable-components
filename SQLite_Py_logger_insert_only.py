'''
    In this example, the log_activity_python function connects to the
    logs.db database and inserts a new row with the specified activity
    into the LOGS table. Note that this code assumes that the database
    and table have already been created by the C code.

'''

import sqlite3

def log_activity_python(activity):
    conn = sqlite3.connect('logs.db')
    c = conn.cursor()

    c.execute("INSERT INTO activities (description) VALUES (?)", (activity,))

    conn.commit()
    conn.close()

if __name__ == '__main__':
    log_activity_python("Module initialized from Python")
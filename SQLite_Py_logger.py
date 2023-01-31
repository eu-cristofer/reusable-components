'''
    In this code, create_conn() creates a connection to the SQLite
    database activities.db and returns the connection object.
    
    create_table(conn) creates a table named activities if it doesn't
    already exist with columns activity_id, activity_name, and
    activity_timestamp.
    
    log_activity(conn, activity_name) logs an activity by inserting
    a new row into the activities table with the specified activity_name.

    retrieve_activities(conn) retrieves all activities from the 
    activities table and returns the result.

    The main() function ties all these functions together to demonstrate
    how to use the module.
'''


import sqlite3

def create_conn():
    conn = sqlite3.connect('activities.db')
    return conn

def create_table(conn):
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS activities (activity_id INTEGER PRIMARY KEY, activity_name TEXT NOT NULL, activity_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL)''')
    conn.commit()

def log_activity(conn, activity_name):
    c = conn.cursor()
    c.execute("INSERT INTO activities (activity_name) VALUES (?)", (activity_name,))
    conn.commit()

def retrieve_activities(conn):
    c = conn.cursor()
    c.execute("SELECT * FROM activities")
    return c.fetchall()

def main():
    conn = create_conn()
    create_table(conn)
    log_activity(conn, "Login")
    print(retrieve_activities(conn))
    conn.close()

if __name__ == '__main__':
    main()

import sqlite3

def list_tables_columns(database_file):
    # Connect to the database
    conn = sqlite3.connect(database_file)
    c = conn.cursor()

    # Get all table names
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    table_names = [table[0] for table in c.fetchall()]

    # Get column names for each table
    tables = {}
    for table_name in table_names:
        c.execute(f"PRAGMA table_info({table_name})")
        column_names = [column[1] for column in c.fetchall()]
        tables[table_name] = column_names

    # Close the connection
    conn.close()

    return tables

if __name__ == '__main__':
    print(list_tables_columns('logs.db'))

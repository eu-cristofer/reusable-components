/*
 * The code prints the database from CLI name argument
 * ==============================================================
 * 
 * The code takes the database name as a command line argument and
 * prints the last thirty rows from the predefine table.
 * 
 * Description:
 * ------------
 * 
 * This code first checks if the number of command line arguments is
 * not equal to 2 and prints the usage of the program if it's not.
 * Then it opens the database specified in the command line argument
 * using sqlite3_open. If the database can't be opened, it prints an
 * error message and returns 1.
 * 
 * Next, it prepares a SELECT statement using sqlite3_prepare_v2 to
 * retrieve the last thirty rows from the "activities" table in the database.
 * If the preparation of the statement fails, it prints an error
 * message and returns 1.
 * 
 * The code then uses a while loop to execute the SELECT statement
 * using sqlite3_step and retrieves the data from each row. The data
 * from each column is retrieved using functions such as sqlite3_column_int
 * and sqlite3_column_text. The data is then printed on the screen.
 * 
 * Finally, the prepared statement is finalized using sqlite3_finalize
 * and the database connection is closed using sqlite3_close.
 * The code returns 0 to indicate success.
 * 
 * Compilation instructions:
 * -------------------------
 * 
 * To use in CLI the compilation should include the option:
 *     -lsqlite3
 *
 * @author Cristofer Costa <cristofercosta@yahoo.com.br>
 * @link 
 */

#include <stdio.h>
#include <sqlite3.h>

int main(int argc, char* argv[]) {
    /* checks if the number of command line arguments */
    if (argc != 2) {
        printf("Usage: %s <database_name>\n", argv[0]);
        return 1;
    }

    /* opennig the database specified in the command line*/
    sqlite3 *db;
    int rc = sqlite3_open(argv[1], &db);
    if (rc) {
        printf("Can't open database: %s\n", sqlite3_errmsg(db));
        return 1;
    }

    /* retrieve the last thirty rows from the table "activities"*/
    sqlite3_stmt *stmt;
    rc = sqlite3_prepare_v2(db, "SELECT * FROM activities ORDER BY activity_id ASC LIMIT 30", -1, &stmt, NULL);
    if (rc != SQLITE_OK) {
        printf("SQL error: %s\n", sqlite3_errmsg(db));
        return 1;
    }

    printf("ID\tTIMESTAMP\t\tACTIVITY\n");
    while (sqlite3_step(stmt) == SQLITE_ROW) {
        int id = sqlite3_column_int(stmt, 0);
        const char *activity = (const char*)sqlite3_column_text(stmt, 1);
        const char *time = (const char*)sqlite3_column_text(stmt, 2);
        printf("%d\t%s\t%s\n", id, time, activity);
    }

    sqlite3_finalize(stmt);
    sqlite3_close(db);
    return 0;
}


/*
 * SQLite3 code to log activities in a software module.
 * ==============================================================
 * 
 * Compilation instructions:
 * -------------------------
 * 
 * To create a shared library from C code, you need to compile 
 * the code with the -fPIC and -shared flags, i.e.:
 * 
 *     gcc -fPIC -shared SQLite_C_logtool.c -o liblog_activity.so
 * 
 * This command will compile the C code in log_activity.c into
 * a shared library named liblog_activity.so. The -fPIC flag is
 * used to create position-independent code, which is required
 * for shared libraries. The -shared flag is used to specify that
 * the output should be a shared library.
 * 
 * To use in CLI the compilation should include the option:
 *     -lsqlite3
 *
 * @author Cristofer Costa <cristofercosta@yahoo.com.br>
 * @link 
 */

#include <sqlite3.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define DATABASE_NAME "logs.db"
#define CREATE_TABLE_SQL "CREATE TABLE IF NOT EXISTS activities (activity_id INTEGER PRIMARY KEY AUTOINCREMENT, description TEXT NOT NULL, activity_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL);"

void log_activity(const char *activity) {
    sqlite3 *db;
    int rc;
    char *sql;
    char *zErrMsg = 0;

    /* opening/creating the database if it does not exist */
    rc = sqlite3_open(DATABASE_NAME, &db);
    if (rc) {
        fprintf(stderr, "Can't open database: %s\n",
                sqlite3_errmsg(db));
        exit(0);
    } else {
        fprintf(stderr, "Opened database successfully\n");
    }

    /* create the table if it does not exist */
    rc = sqlite3_exec(db, CREATE_TABLE_SQL, 0, 0, &zErrMsg);
    if (rc != SQLITE_OK) {
        fprintf(stderr, "SQL error: %s\n", zErrMsg);
        sqlite3_free(zErrMsg);
    } else {
        fprintf(stdout, "Table created successfully\n");
    }

    /* create SQL statement */
    sql = sqlite3_mprintf("INSERT INTO activities (description) VALUES ('%q');",
                          activity);

    /* execute SQL statement */
    rc = sqlite3_exec(db, sql, 0, 0, &zErrMsg);
    if (rc != SQLITE_OK) {
        fprintf(stderr, "SQL error: %s\n", zErrMsg);
        sqlite3_free(zErrMsg);
    } else {
        fprintf(stdout, "Activity logged successfully\n");
    }

    sqlite3_close(db);
}

int main(int argc, char *argv[]) {
  log_activity("Module initialized");
  return 0;
}
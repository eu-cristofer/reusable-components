
/*
 * SQLite3 code to log activities in a software module
 *
 * @author Cristofer Costa <cristofercosta@yahoo.com.br>
 * @link https://confired.com
 */

#include <sqlite3.h>
#include <stdio.h>

int check_and_create_database(const char *db_name)
{
    sqlite3 *db;
    int rc = sqlite3_open(db_name, &db);
    if (rc != SQLITE_OK)
    {
        // Database does not exist, create it
        rc = sqlite3_open(db_name, &db);
        if (rc) 
        {
            fprintf(stderr, "Can't create database: %s\n", sqlite3_errmsg(db));
            sqlite3_close(db);
            return 1;
        }
    }
    else
    {
        // Database exists
        fprintf(stderr, "Database exists\n");
    }
    sqlite3_close(db);
    return 0;
}

int main(int argc, char* argv[])
{
    return check_and_create_database("logs.db");
}
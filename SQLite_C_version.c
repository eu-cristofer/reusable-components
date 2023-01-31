/*
 * Code check the version of the SQLite database
 * ========================================================
 * 
 * Compilation instructions:
 * -------------------------
 * 
 * To compile the code the link shall be made as bellow:
 * 
 *     gcc SQLite_C_version.c -lsqlite3
 * 
 * 
 * @author Cristofer Costa <cristofercosta@yahoo.com.br>
 * @link https://confired.com
 */

#include <sqlite3.h>
#include <stdio.h>

int main(void) {
    
    printf("Version of the SQLite database: %s\n",
        sqlite3_libversion()); 
    
    return 0;
}
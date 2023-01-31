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
 *     or
 * 
 *     gcc SQLite_C_version.c sqlite-amalgamation/sqlite3.c
 *         -lpthread -ldl -lm -o version
 *  * 
 * @author Cristofer Costa <cristofercosta@yahoo.com.br>
 * @link https://github.com/eu-cristofer/reusable-components
 */

#include <sqlite3.h>
#include <stdio.h>

int main(void) {
    
    printf("Version of the SQLite database: %s\n",
        sqlite3_libversion()); 
    
    return 0;
}
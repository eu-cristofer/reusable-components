# Reusable Components
Reusable pieces of code

# Contents
- [SQLite_C_logger.c](#sqlite_c_logger)

- [SQLite_Py_C_logger.py](#sqlite_py_c_logger)

## SQLite_C_logger

Source file: ```SQLite_C_logger.c```.

Code sample of howto use SQLite to log activities in a software module. 

### Compilation instructions:

To create a shared library from C code, you need to compile the code with the -fPIC and -shared flags, i.e.:

    gcc -fPIC -shared SQLite_C_logger.c sqlite-amalgamation/sqlite3.c
        -lpthread -ldl -lm -o db_logger.so
Where:
 - sqlite3.c is the SQLite amalgamation source file; and
 - sqlite3.h is the header files that defines the C-language 
   interfaces to SQLite.

This command will compile the C code SQLite_C_logger.c into a shared library named db_logger.so. The -fPIC flag is used to create position-independent code, which is required for shared libraries. The -shared flag is used to specify that the output should be a shared library.

The -lpthread flag is allows the program to make use of multi-threading for more efficient and concurrent execution.

The -ldl flag is used to link with the dynamic linker/loader library (libdl). This library provides a standard interface to dynamically load and unload shared libraries in a program.

The -lm flag in GCC tells the compiler to link the mathematical library (libm) to the executable. The mathematical library contains functions for mathematical operations such as trigonometry, logarithms, etc.

The -o flag in GCC specifies the name of the output file.

## SQLite_Py_C_logger

Source file:```SQLite_Py_C_logger.py```.

Sample of how to use the SQLite_C_logger.c from a Python code using the sqlite3 module

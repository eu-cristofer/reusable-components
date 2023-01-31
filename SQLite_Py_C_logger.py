'''
    In this sample we call the C function from Python using the ctypes module.

    The code uses a C SQLite module to log activities in a Py code.
    
    In this code, the ctypes.CDLL function is used to load the shared library
    SQLite_C_logger.so that was compiled from the C code. The argtypes attribute
    of the function is used to specify the argument types of the C function.
    Finally, the C function is called using the lib.log_activity syntax, where
    lib is the loaded library and log_activity is the name of the function.

    C Code compilation instructions
    -------------------------------
    To create a shared library from C code, you need to compile the code with 
    the -fPIC and -shared flags, i.e.:

        gcc -fPIC -shared SQLite_C_logger.c sqlite-amalgamation/sqlite3.c
            -lpthread -ldl -lm -o db_logger.so
    
    Where:
        - sqlite3.c is the SQLite amalgamation source file; and
        - sqlite3.h is the header files that defines the C-language 
          interfaces to SQLite.

    This command will compile the C code SQLite_C_logger.c into a shared library
    named db_logger.so. The -fPIC flag is used to create position-independent
    code, which is required for shared libraries. The -shared flag is used 
    to specify that the output should be a shared library.

    The -lpthread flag is allows the program to make use of multi-threading
    for more efficient and concurrent execution.

    The -ldl flag is used to link with the dynamic linker/loader library (libdl).
    This library provides a standard interface to dynamically load and unload 
    shared libraries in a program.

    The -lm flag in GCC tells the compiler to link the mathematical library
    (libm) to the executable. The mathematical library contains functions for
    mathematical operations such as trigonometry, logarithms, etc.

    The -o flag in GCC specifies the name of the output file.

    @link https://github.com/eu-cristofer/reusable-components
'''

import ctypes
import os


working_dir = os.getcwd()
os.add_dll_directory(working_dir)

# Load the shared library (assuming the C code has been compiled into
# a shared library named SQLite_C_logger.so)
lib = ctypes.CDLL('db_logger.so')

# Define the prototype of the C function
lib.log_activity.argtypes = [ctypes.c_char_p]

# Call the C function
lib.log_activity(b"Module initialized from Python")

# Do your activity here

# Call the C function again to log another activity
lib.log_activity(b"Performed an activity from Python")

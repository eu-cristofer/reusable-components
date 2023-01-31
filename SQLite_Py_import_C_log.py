'''
    In this sample we call the C function from Python using the ctypes module.
    
    In this code, the ctypes.CDLL function is used to load the shared library
    liblog_activity.so that was compiled from the C code. The argtypes attribute
    of the function is used to specify the argument types of the C function.
    Finally, the C function is called using the lib.log_activity syntax, where
    lib is the loaded library and log_activity is the name of the function.
'''

import ctypes

# Load the shared library (assuming the C code has been compiled into
# a shared library named liblog_activity.so)
lib = ctypes.CDLL('./liblog_activity.so')

# Define the prototype of the C function
lib.log_activity.argtypes = [ctypes.c_char_p]

# Call the C function
lib.log_activity(b"Module initialized from Python")

# Do your activity here

# Call the C function again to log another activity
lib.log_activity(b"Performed an activity from Python")

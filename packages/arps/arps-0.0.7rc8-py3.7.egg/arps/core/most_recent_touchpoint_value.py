'''
Get the most recent touchpoint state, i.e., the last line

Implementation from https://stackoverflow.com/a/18603065/174605
'''
import os
from time import sleep

def most_recent_touchpoint_value(touchpoint_file):
    while True:
        try:
            return _read_last_line_from(touchpoint_file)
        except OSError:
            sleep(0.5) #sometimes the file will be moved by the RotatingFileHandler

def _read_last_line_from(touchpoint_file):
    with open(touchpoint_file, 'rb') as f:
        f.seek(-2, os.SEEK_END)     # Jump to the second last byte.
        while f.read(1) != b'\n':   # Until EOL is found...
            f.seek(-2, os.SEEK_CUR) # ...jump back the read byte plus one more.
        return f.readline().decode()[:-1].strip()

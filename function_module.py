import os
import datetime


def generate_folder(folder_name):
    '''Check if a directory exist otherwise create it.'''
    for file in os.scandir():
        if file.name == folder_name and file.is_dir:
            return
    os.mkdir(folder_name)


def return_recording_name():
    '''Returns a string with the current date
       plus the current local time.'''
    current_date = datetime.datetime.now()
    return current_date.strftime('%y_%b_%d_%X_record.avi')

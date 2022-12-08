import socket 
import sys
import dualRecorder
from signal import signal, SIGINT
import os 


def enter(question):
    Input = input(question)
    if Input == 'exit':
        print('Closing...')
        try:
            print('Exiting gracefully...')
            sys.exit(0)
        except:
            print('Attemped exit gracefully but failed.')
    return Input


    
def set_location(path):
    print('Setting location to ', path)
    try:
        os.chdir(path)
        return True
    except:
        print('Error setting location to ', path)
        return False 

if __name__ == '__main__':
    pathQuestion = 'Enter the path to file folder: '
    pathSet = False
    while pathSet == False:
        path = enter(pathQuestion)
        pathSet = set_location(path)
    print('Path set, waiting for details...')
    filename = enter('Enter the filename: ')
    pipeline, zed, config= dualRecorder.initialize(filename)
    duration = int(enter('Enter the duration: '))
    start = enter('Enter start to start recording: ')
    print('Starting...')
    pipeline, zed = dualRecorder.start_recording(pipeline, zed, config, duration)
    print('Stoping...', end = '\n')
    pipeline.stop()
    zed.disable_recording()
    zed.close()

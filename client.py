import socket 
import sys
import dualRecorder
from signal import signal, SIGINT
import os 


def handler(signal_received, frame):
    try:
        pipeline.stop()
        zed.disable_recording()
        zed.close()
    except:
        print('Attemped exit gracefully but failed.')
    sys.exit(0)


signal(SIGINT, handler)



def set_location(path):
    print('Setting location to ', path)
    try:
        os.chdir(path)
        return True
    except:
        print('Error setting location to ', path)
        return False 


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

if __name__ == '__main__':
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        serverStarted = False
        while serverStarted == False:
            IPQuestion = 'Enter the IP Address: '
            HOST = enter(IPQuestion)
            PORTQuestion = 'Enter the Port Number: '
            PORT = int(enter(PORTQuestion))
            try:
                s.connect((HOST, PORT))
                serverStarted = True
            except socket.error as e:
                print(str(e))
                print('Attempting to restart...')
                serverStarted = False
        print('Connected to Server...')
        pathQuestion = 'Enter the path to file folder: '
        pathSet = False
        while pathSet == False:
            path = enter(pathQuestion)
            pathSet = set_location(path)
        print('Path set, waiting for details...')
        while True:
            data = s.recv(1024)
            filename = data.decode('utf-8')
            print(filename)
            pipeline, zed, config= dualRecorder.initialize(filename)
            data = s.recv(1024)
            duration = int(data.decode('utf-8'))
            data = s.recv(1024)
            while data.decode('utf-8') != 'start':
                data = s.recv(1024)
                if data.decode('utf-8') == 'error':
                    sys.exit(0)
            print('Starting...')
            pipeline, zed = dualRecorder.start_recording(pipeline, zed, config, duration)
            print('Stoping...', end = '\n')
            pipeline.stop()
            zed.disable_recording()
            zed.close()
            s.sendall(str.encode('done'))
            print('Done Recording: ', filename)
            data = s.recv(1024)
            if data.decode('utf-8') == 'stop':
                print('Closing...')
                try:
                    print('Exiting gracefully...')
                    pipeline.stop()
                    zed.disable_recording()
                    zed.close()
                    sys.exit(0)
                except:
                    print('Attemped exit gracefully but failed.')
            else:
                print('Restarting...')
                continue
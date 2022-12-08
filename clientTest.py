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


if __name__ == '__main__':
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        IPNotDone = True
        hostNotDone = True
        clientNotStarted = True
        pathSet = False
        while pathSet == False:
            Input = input('Enter the path to file folder: ')
            if Input == 'exit':
                print('Closing...')
                try:
                    print('Exiting gracefully...')
                    sys.exit(0)
                except:
                    print('Attemped exit gracefully but failed.')
            confirmation = input('File path: ' + Input + ' confirm(y/n)? ')
            if confirmation == 'y':
                pathSet = set_location(Input)
            elif confirmation == 'n':
                continue
            elif confirmation == 'exit':
                print('Closing...')
                try:
                    print('Exiting gracefully...')
                    sys.exit(0)
                except:
                    print('Attemped exit gracefully but failed.')
            else:
                print('Please enter a valid response')
        while clientNotStarted == True:
            while IPNotDone == True:
                Input = input('Enter the IP Address: ')
                if Input == 'exit':
                    print('Closing...')
                    try:
                        print('Exiting gracefully...')
                        sys.exit(0)
                    except:
                        print('Attemped exit gracefully but failed.')
                confirmation = input('IP Address: ' + Input + ' confirm(y/n)? ')
                if confirmation == 'y':
                    HOST = Input
                    IPNotDone = False
                elif confirmation == 'n':
                    continue
                elif confirmation == 'exit':
                    print('Closing...')
                    try:
                        print('Exiting gracefully...')
                        sys.exit(0)
                    except:
                        print('Attemped exit gracefully but failed.')
                else:
                    print('Please enter a valid response')
            while hostNotDone == True:
                Input = input('Enter the Port Number: ')
                if Input == 'exit':
                    print('Closing...')
                    try:
                        print('Exiting gracefully...')
                        sys.exit(0)
                    except:
                        print('Attemped exit gracefully but failed.')
                confirmation = input('IP Address: ' + Input + ' confirm(y/n)? ')
                if confirmation == 'y':
                    PORT = int(Input)
                    hostNotDone = False
                elif confirmation == 'n':
                    continue
                elif confirmation == 'exit':
                    print('Closing...')
                    try:
                        print('Exiting gracefully...')
                        sys.exit(0)
                    except:
                        print('Attemped exit gracefully but failed.')
                else:
                    print('Please enter a valid response')
            try:
                s.connect((HOST, PORT))
            except socket.error as e:
                print(str(e))
                print('Attempting to restart...')
                continue
            clientNotStarted = False
        print('Connected to Server, waiting for start...')
        while True:
            data = s.recv(1024)
            filename = data.decode('utf-8')
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
                    sys.exit(0)
                except:
                    print('Attemped exit gracefully but failed.')
            else:
                print('Restarting...')
                continue

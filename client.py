import socket 
import sys
import dualRecorder
from signal import signal, SIGINT


def handler(signal_received, frame):
    try:
        pipeline.stop()
        zed.disable_recording()
        zed.close()
    except:
        print('Attemped exit gracefully but failed.')
    sys.exit(0)


signal(SIGINT, handler)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    IPNotDone = True
    hostNotDone = True
    clientNotStarted = True
    while clientNotStarted == True:
        while IPNotDone == True:
            Input = input('Enter the IP Address: ')
            confirmation = input('IP Address: ' + Input + ' confirm(y/n)? ')
            if confirmation == 'y':
                HOST = Input
                IPNotDone = False
            elif confirmation == 'n':
                continue
            elif confirmation == 'exit':
                print('Closing server...')
                try:
                    print('Exiting gracefully...')
                    sys.exit(0)
                except:
                    print('Attemped exit gracefully but failed.')
            else:
                print('Please enter a valid response')
        while hostNotDone == True:
            Input = input('Enter the Port Number: ')
            confirmation = input('IP Address: ' + Input + ' confirm(y/n)? ')
            if confirmation == 'y':
                PORT = int(Input)
                hostNotDone = False
            elif confirmation == 'n':
                continue
            elif confirmation == 'exit':
                print('Closing server...')
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
    pipeline, zed, config= dualRecorder.initialize()
    data = s.recv(1024)
    duration = int(data.decode('utf-8'))
    data = s.recv(1024)
    filename = data.decode('utf-8')
    pipeline, zed, config= dualRecorder.initialize(filename)
    data = s.recv(1024)
    while data.decode('utf-8') != 'start':
        data = s.recv(1024)
        if data.decode('utf-8') == 'error':
            sys.exit(0)
    print('Starting...')
    pipeline, zed = dualRecorder.start_recording(pipeline, zed, config, duration)
    print('Stoping...', end = '\n')
    s.sendall(str.encode('done'))
    print('Done')
    sys.exit(0)

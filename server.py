
import socket
import os
from _thread import *
import argparse 
import sys
from signal import signal, SIGINT

from pyparsing import DebugStartAction

def handler(signal_received, frame):
    print('SIGINT or CTRL-C detected. Exiting gracefully...')
    sys.exit(0)

signal(SIGINT, handler)


def send_start(connection):
    print('Sending start to ', connection)
    connection.send(str.encode('start'))

def send_stop(connection):
    print('Sending stop to ', connection)
    connection.send(str.encode('stop'))

def send_duration(connection, duration):
    print('Sending duration to ', connection)
    connection.send(str.encode(duration))

def send_filenames(connection, filename):
    print('Sending filename to ', connection)
    connection.send(str.encode(filename))

def search_signal():
    print('Searching for signal...')
    client, address = ServerSocket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    return client



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
    try:
        serverStarted = False
        while serverStarted == False:
            IPQuestion = 'Enter the IP Address: '
            HOST = enter(IPQuestion)
            PORTQuestion = 'Enter the Port Number: '
            PORT = int(enter(PORTQuestion))
            ServerSocket = socket.socket()
            try:
                ServerSocket.bind((HOST, PORT))
                serverStarted = True
            except socket.error as e:
                print(str(e))
                print('Attempting to restart...')
                ServerSocket.close()
                continue
            print('Server started successfully')
        ServerSocket.listen()
        CamerasOne = search_signal()
        print('Connected to Camera 1')
        CamerasTwo = search_signal()
        print('Connected to Camera 2')
        while True:
            durationNotSent = True
            filenameNotSent = True
            startNotSent = True
            while filenameNotSent:
                filename = input('What is the name of the file going to be: ')
                if filename == 'exit':
                    print('Closing...')
                    try:
                        print('Exiting gracefully...')
                        ServerSocket.close()
                        CamerasOne.close()
                        CamerasTwo.close()
                        sys.exit(0)
                    except:
                        print('Attemped exit gracefully but failed.')
                confirmation = input('Confirm ' + filename + ' as the file names(y/n)?')
                if confirmation == 'y':
                    send_filenames(CamerasOne, filename + 'One')
                    send_filenames(CamerasTwo, filename + 'Two')
                    filenameNotSent = False
                elif confirmation == 'n':
                    continue
                elif confirmation == 'exit':
                    print('Closing server...')
                    try:
                        ServerSocket.close()
                        CamerasOne.close()
                        CamerasTwo.close()
                        sys.exit(0)
                    except:
                        print('Attemped to close server, but failed.')
                else:
                    continue
            while durationNotSent:
                duration = input('How long do you want the cameras to run (seconds): ')
                if duration == 'exit':
                    print('Closing...')
                    try:
                        print('Exiting gracefully...')
                        ServerSocket.close()
                        CamerasOne.close()
                        CamerasTwo.close()
                        sys.exit(0)
                    except:
                        print('Attemped exit gracefully but failed.')
                confirmation = input('Confirm ' + duration + ' seconds(y/n)?')
                if confirmation == 'y':
                    send_duration(CamerasOne, duration)
                    send_duration(CamerasTwo, duration)
                    durationNotSent = False
                elif confirmation == 'n':
                    continue
                elif confirmation == 'exit':
                    print('Closing server...')
                    try:
                        ServerSocket.close()
                        CamerasOne.close()
                        CamerasTwo.close()
                        sys.exit(0)
                    except:
                        print('Attemped to close server, but failed.')
                else:
                    print('Please enter a valid response')
                    continue
            while startNotSent == True:
                Input = input('Type "exit" to close the server or "start" to start recording: ')
                if Input == 'exit':
                    print('Closing server...')
                    try:
                        ServerSocket.close()
                        CamerasOne.close()
                        CamerasTwo.close()
                        sys.exit(0)
                    except:
                        print('Attemped to close server, but failed.')
                elif Input == 'start':
                    print('Signal Sent')
                    send_start(CamerasOne)
                    send_start(CamerasTwo)
                    startNotSent = False
                else:
                    print('Please enter a valid response')
                    continue
            dataOne = CamerasOne.recv(1024)
            dataTwo = CamerasTwo.recv(1024)
            if dataOne.decode('utf-8') == 'done' and dataTwo.decode('utf-8') == 'done':
                print('Recording Successful')
            Input = input('Type "exit" to close the server or "restart" to restart: ')
            if Input == 'exit':
                print('Closing server...')
                send_stop(CamerasOne)
                send_stop(CamerasTwo)
                try:
                    ServerSocket.close()
                    CamerasOne.close()
                    CamerasTwo.close()
                    sys.exit(0)
                except:
                    print('Attemped to close server, but failed.')
                    sys.exit(0)
            elif Input == 'restart':
                print('Restarting...')
                send_start(CamerasOne)
                send_start(CamerasTwo)
                continue          
    except socket.error as e:
        print(str(e))
        ServerSocket.close()

ServerSocket.close()

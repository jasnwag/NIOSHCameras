
import socket
import os
from _thread import *
import argparse 
import sys
from signal import signal, SIGINT

def handler(signal_received, frame):
    print('SIGINT or CTRL-C detected. Exiting gracefully...')
    sys.exit(0)

signal(SIGINT, handler)


def threaded_client(connection):
    connection.send(str.encode('Welcome to the Server'))
    #while True:
        #data = connection.recv(2048)
        #reply = 'Server Says: ' + data.decode('utf-8')
        #if not data:
            #break
        #connection.sendall(str.encode(reply))
    #connection.close()

def send_start(connection):
    print('Sending start to ', connection)
    connection.send(str.encode('start'))

def send_stop(connection):
    print('Sending stop to ', connection)
    connection.send(str.encode('stop'))

def send_time(connection, time):
    print('Sending time to ', connection)
    connection.send(str.encode('time'))

def search_signal():
    print('Searching for signal...')
    client, address = ServerSocket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    #start_new_thread(threaded_client, (client, ))
    return client


if __name__ == '__main__':
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
    ServerSocket = socket.socket()
    try:
        ServerSocket.bind((HOST, PORT))
        ServerSocket.listen()
        CamerasOne = search_signal()
        print('Connected to Camera 1')
        CamerasTwo = search_signal()
        print('Connected to Camera 2')
        Input = input('How long do you want the cameras to run (seconds)?')
        send_time(CamerasOne, Input)
        send_time(CamerasTwo, Input)
        Input = input('Type "exit" to close the server or "start" to start recording: ')
        if Input == 'exit':
            ServerSocket.close()
        if Input == 'start':
            print('Signal Sent')
            send_start(CamerasOne)
            send_start(CamerasTwo)
        """
        Input = input('Type "exit" to close the server or "stop" to stop recording: ')
        if Input == 'exit':
            ServerSocket.close()
        if Input == 'stop':
            send_stop(CamerasOne)
            send_stop(CamerasTwo)
            CamerasOne.close()
            CamerasTwo.close()
        """
        dataOne = CamerasOne.recv(1024)
        dataTwo = CamerasTwo.recv(1024)
        if dataOne.decode('utf-8') == 'done' and dataTwo.decode('utf-8') == 'done':
            print('Done')
            CamerasOne.close()
            CamerasTwo.close()
            ServerSocket.close()
    except socket.error as e:
        print(str(e))
        ServerSocket.close()

ServerSocket.close()

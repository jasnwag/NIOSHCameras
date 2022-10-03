import socket 
import sys
import dualTest
from signal import signal, SIGINT

HOST = sys.argv[1]
PORT = int(sys.argv[2])

def handler(signal_received, frame):
    zed.disable_recording()
    zed.close()
    try:
        pipeline.stop()
    except:
        print('No Pipeline')
    sys.exit(0)


signal(SIGINT, handler)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print('Connected to Server, waiting for start...')
    pipeline, zed = dualTest.initialize()
    data = s.recv(1024)
    time = int(data.decode('utf-8'))
    data = s.recv(1024)
    while data.decode('utf-8') != 'start':
        data = s.recv(1024)
        if data.decode('utf-8') == 'error':
            sys.exit(0)
    print('Starting...')
    pipeline, zed = dualTest.start_recording(pipeline, zed, time)
    print('Stoping...')
    zed.disable_recording()
    zed.close()
    pipeline.stop()
    print('Done')
    s.sendall(str.encode('done'))
    sys.exit(0)

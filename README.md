# NIOSHCameras
These are scripts to operate both the Zed 2i and Intel D455 cameras simultaneously and store the corresponding video formats on two client computers totalling four videos. A server is created to communicate with two clients and send signals to each via sockets. Procedure is listed below 

### Navigating to Python Files
Need to locate the directory of the python files named NIOSHCameras. These are located in a github repository already locally stored on the computers. Use the terminal in VSCode or command prompt to find the directory. You can find the path to the directory and input "cd /path" to find the directory. I would recommend using this resource to help get used to the commands: https://tutorials.codebar.io/command-line/introduction/tutorial.html (mainly need to look at ls and cd)

*Throughout the entire process, holding control first then c should exit the system properly. If somehow the server or client are not shut down properly, that should just require a new port number.

### Operating the Server
1. To start the server, use the command 'python server.py' in the directory with all the scripts. 
2. This should prompt a question asking for the IP Address. On windows, look for the IP4V address (should be formatted similar to XXX.XXX.XXX.XX) and enter that. THe IP4V address should be located under network settings
3. Another prompt should ask for the port number, you should be able to use any five digit number and input it here. Ex. 12345

Record down both as they will need to be inputted into the client computer as well. If an error occurs where the server can not be started, I would double check the IP address again and also change the port number, this should solve most of the issues. 

### Operating the Client
1. To start the client, use the command 'python client.py' in the directory will all the scripts on both computers
2. The first prompt should ask for the path(location) to the folder where we want the files saved, enter that path. (Be weary for folders with spaces, if spaces exist put quotation marks around that folder)
3. The next prompt should ask for the IP Address used on the server, input the exact same IP address.
4. Another prompt shoudl ask for the port number, input the exact same Port number for the server

Check to make sure that all the IP address and Port numbers are correct, if correct all computers should say connected and the server should move on to the next step

### Server filename and duration
1. A prompt will ask for the filename used to store the videos, entire a filename and confirm. This will be saved under setup1 and setup2 depending on the order of the clients
2. Another prompt will ask for the expected duration of the recording to take place, enter the number in seconds and confirm

### Server start recording
1. A prompt will ask you to enter 'start' to send a signal to both clients to record for the inputted duration.
2. Both clients will record the video for the duration
3. Once stopped all files are saved locally to the directory with all the scripts
4. A signal is sent from both clients to the server that recording is done
5. A prompt will show up asking if we want to repeat the process aka record another video - resond accordingly


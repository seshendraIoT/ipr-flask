

import socket
import psutil
import time


socket_client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

socket_client.connect(("127.0.0.1",8081)) 
socket_client.settimeout(60)
while True:    
    try:
        socket_client.send(str({'V1':'MEM','V2':psutil.virtual_memory()[2]}).encode())
        time.sleep(45)
    except Exception as exp:
        print(exp)
        socket_client.close()
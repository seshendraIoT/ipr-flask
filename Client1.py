


import socket
import psutil
import time


socket_client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

socket_client.connect(("127.0.0.1",8081)) 
socket_client.settimeout(60)
while True:    
    try:
        socket_client.send(str({'V1':'CPU','V2': psutil.cpu_percent()}).encode())
        time.sleep(30)
    except Exception as exp:
        print(exp)
        socket_client.close()
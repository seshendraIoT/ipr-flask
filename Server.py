

import sqlite3
import paho.mqtt.client as paho_mqtt
import socket 
import Thread

thread_process_list=list()

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
threadList = [] 

connection= sqlite3.connect("MyDatabase.db").cursor()


 
class SubscriberThread(Thread):
    def __init__(self,topic):
        Thread.__init__(self)
        self.topic = topic
    def run(self):
        client = paho_mqtt.Client('My_Client')
        client.on_message = on_message  
        client.connect("broker.hivemq.com")   
        client.subscribe("topic/mem_request")
        client.subscribe("topic/cpu_request")
        client.loop_forever() 
class Client(Thread): 
 
    def __init__(self,ip,port): 
        Thread.__init__(self) 
        self.ip = ip
        self.port = port
    def run(self): 
       server.listen(3) 
       (conn, (ip,port)) = server.accept()        
       while 1 : 
            dataProcessing(eval(conn.recv(2048).decode()) )
            conn.send(conn.recv(2048)) 
        
def dataProcessing(dt):
    if(dt['V2']=='CPU'):
            if(float(dt['V2']>30.0)):
                values = list()
                values.append(dt['V1'])
                values.append(dt['V2'])
                connection.execute("INSERT INTO MyDb (Key, Value ) VALUES (?,?)",tuple(values))
                values.clear()
                connection.commit()
    elif(dt['V2']=='MEM'):
        if(float(dt['V2']>40.0)):
            values = list()
            values.append(dt['V1'])
            values.append(dt['V2'])
            connection.execute("INSERT INTO MyDb (Key, Value ) VALUES (?,?)",tuple(values))
            values.clear()
            connection.commit()
             
        
def on_message(c,ud,m):
     
    
    if(str(m.topic)=="topic/cpu_request" ):
        datas = connection.execute("SELECT * FROM MyDb WHERE Key = 'CPU'" )       
        list1 = []
        for da in datas:
            list1.append(da[2])            
        c.publish("topic/cpu_reply",str(list1))        
    elif(str(m.topic)=="topic/mem_request" ):
        datas = connection.execute("SELECT * FROM MyDb WHERE Key = 'MEM'" )      
        list1 = []
        for da in datas:
            list1.append(da[2])           
        c.publish("topic/mem_reply",str(list1))

   


if __name__ =="__main__":
    connection.execute("DROP TABLE MyDb")
    connection.execute("CREATE TABLE MyDb (pid INTEGER PRIMARY KEY AUTOINCREMENT, Key TEXT ,Value REAL)")
    server.bind(("127.0.0.1",8081))
    server.listen(3) 
    (conn, (ip,port)) = server.accept() 
    threadList.append(SubscriberThread("topic/cpu_request").start())

    while True:
        dataProcessing(eval(conn.recv(1024)))
        newthread = Client(ip,port)
        newthread.start() 
        threadList.append(newthread) 
     
    for thread in threadList: 
        thread.join()
    

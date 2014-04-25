from Network import Listener, Handler, poll
import json, Network

 
handlers = {}  # map client handler to user name
clients=[]
 
class MyHandler(Handler):
     
    def on_open(self):
        self.name = ""
        clients.append(self)
         
    def on_close(self):
        self.on_msg({'leave': self.name})
        client.remove(self)
        
     
    def on_msg(self, msg):
        if msg.has_key('join'):
            self.name = msg['join']
        for x in clients:
            if x != self:
                x.do_send(msg)
        print msg
 
class Server(object): 
    def run(self):
        port = 8888
        server = Listener(port, MyHandler)
        while 1:
            poll(timeout=0.05) # in seconds
        
s= Server()
s.run()
    
       
        
        
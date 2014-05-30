from network import Listener, Handler, poll


handlers = {}  
names = {} 
subs = {} 

def broadcast(msg):
    for h in handlers.keys():
        h.do_send(msg)


class MyHandler(Handler):
    
    def on_open(self):
        handlers[self] = None
        
    def on_close(self):
        leavername = handlers[self]
        del handlers[self]
        
        broadcast({'leave': leavername, 'users': handlers.values()})
        
    def on_msg(self, msg):
        if 'join' in msg:
            user_name = msg['join']
            handlers[self] = msg['join']
            names[user_name] = self
            
            broadcast({'join': user_name, 'users': handlers.values()})
            
        elif 'speak' in msg:
            
            username = msg['speak']
            mytxt = msg['txt']
            
            usermsg = msg['txt'].split()
            send = True
            sendTo =[]
            for x in usermsg:
                if x[0]=="@":
                    sendTo.append(x[1:])
                    names[str(x)[1:]].do_send({'speak': str(msg['speak']), 'txt':str(msg['txt'])})
                elif x[0] == "+":
                    self.subscribe(str(x), str(username))
                    
                elif x[0] == "#":
                    self.publish(str(x), dict(msg), str(username))
                    send = False
                    
                elif x[0] == '-':
                    self.unsubscribe(str(x), str(username))
            
            if send == True:
                broadcast({'speak': username, 'txt': mytxt})
    
    def publish(self, string, msg, user_name):
        send_list = subs['+' + string[1:]]
        if len(send_list) != 0:
            for user in send_list:
                if user != self:
                    names[user].do_send({'speak': msg['speak'], 'txt': msg['txt']})

                
    def unsubscribe(self, string, user_name):
        for k in subs.keys():
            if k[1:] == string[1:]:
                subs['+' + string[1:]].discard(user_name)
                
            
    
    def subscribe(self, string, user_name):
        if string not in subs.keys():
            subs[string] = {user_name}
        else:
            subs[string].add(user_name)


Listener(8888, MyHandler)
while 1:
    poll(0.05)
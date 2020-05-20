import socket              
import threading
import pymysql
from pymysql.err import IntegrityError
import string
import time

import helper
import constants


def on_new_client(clientsocket, addr, db):
    done = False
    while not done:
      request = clientsocket.recv(1024)
      response = helper.handle_request(request, addr, db)
      try:
        clientsocket.send(response)
      except BrokenPipeError:
        clientsocket.close()
        done = True

def main():      
    # Open database connection
    db = pymysql.connect("localhost","mboxserver","catfishbookwormzebra","mbox" )

    s = socket.socket()        
    port = 8080                

    print ('Server started. Waiting for clients...')

    s.bind(('', port))        # '' for all interfaces
    s.listen(1000)                

    while True:
       c, addr = s.accept()    
       x = threading.Thread(target=on_new_client, args=(c, addr, db))
       x.start()

    s.close()

if __name__ == '__main__':
    # execute only if run as a script
    main()


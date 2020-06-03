import socket              
import threading
import pymysql
from pymysql.err import IntegrityError
import string
import time
import sys
import logging

import helper
import constants

class Server:

  done_serving = False

  def __init__(self, host, user, pw, dbname, port):
    self.host = host
    self.user = user
    self.pw = pw
    self.dbname = dbname
    self.port = port
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %H:%M:%S', level=logging.DEBUG)

  def start_listening(self):
    self.server_socket = socket.socket()        
    
    logging.debug ('Server started. Waiting for clients...')

    self.server_socket.bind(('', self.port))        # '' for all interfaces
    self.server_socket.listen(1000)       
    self.server_socket.settimeout(0.2)         

    while not(self.done_serving):
      try:
        client, addr = self.server_socket.accept()    
        client_thread = threading.Thread(target=self.on_new_client, args=(client, addr, self.host, self.user, self.pw, self.dbname))
        client_thread.start()
      except socket.timeout:
        pass

    self.server_socket.close()


  def on_new_client(self, clientsocket, addr, host, user, pw, dbname):
    db = pymysql.connect(host, user, pw, dbname)
    client_done = False
    while not client_done:
      request = clientsocket.recv(1024)
      response = helper.handle_request(request, addr, db)
      try:
        clientsocket.send(response)
      except BrokenPipeError:
        clientsocket.close()
        client_done = True

  def stop_server(self):
    self.done_serving = True
 
if __name__ == '__main__':
    host = sys.argv[1]
    user = sys.argv[2]
    pw = sys.argv[3]
    dbname = sys.argv[4]
    port = int(sys.argv[5])               

    server = Server(host, user, pw, dbname, port)
    server.start_listening()



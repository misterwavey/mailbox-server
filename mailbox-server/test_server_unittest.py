import unittest
import socket
import pymysql
import sys
import threading
import time

import server

class TestServer(unittest.TestCase):
  
  host = ""
  user = ""
  pw = ""
  dbname = ""
  port = 0

  test_cases = [
    [
          "request too short",
          bytes([0, 1, 1, 1]),
          bytes([5])
    ],
      [
        "unsupported protocol", 
        bytes([0, 0, 1, 1, 98, 97, 104, 111, 106, 115, 105, 98, 111, 102, 108, 111, 98, 117, 116, 115, 117, 106, 97, 114]),
        bytes([1])
       ],
       [
          "invalid cmd",
          bytes([0, 1, 10, 1, 98, 97, 104, 111, 106, 115, 105, 98, 111, 102, 108, 111, 98, 117, 116, 115, 117, 106, 97, 114]),
          bytes([2])
       ],
       [
          "invalid userid",
          bytes([0, 1, 1, 1, 32, 97, 104, 111, 106, 115, 105, 98, 111, 102, 108, 111, 98, 117, 116, 115, 117, 106, 97, 114]),
          bytes([103])
       ],
       [
          "register bahojsiboflobutsujar",
          bytes([0, 1, 1, 1, 99, 97, 104, 111, 106, 115, 105, 98, 111, 102, 108, 111, 98, 117, 116, 115, 117, 106, 97, 114]),
          bytes([201, 115, 116, 117, 97, 114, 116, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
       ]
    ]

  def run_sql(self, filename):
    with open(filename, 'r') as myfile:
      sql = myfile.read()
      myfile.close

    cursor = self.db.cursor()
    cursor.executemany(sql,None)
    self.db.commit()

  def setUp(self):
    # Open database connection
    self.db = pymysql.connect(self.host, self.user, self.pw, self.dbname);
    self.run_sql("mariadb-ddl.sql")

    # start server thread
    self.mbox_server = server.Server(self.host, self.user, self.pw, self.dbname, self.port)
    self.server_thread = threading.Thread(target=self.mbox_server.start_listening, args=())
    self.server_thread.start()

    time.sleep(2) # wait for it to start up

    self.client_socket = socket.socket()
    self.client_socket.settimeout(1)
    self.client_socket.connect(('127.0.0.1', self.port))

  def tearDown(self):    
      self.mbox_server.stop_server()
      self.client_socket.close()

  def get_response_for_request(self, request):
    self.client_socket.send(request)
    response = self.client_socket.recv(1024)
    return response

  def testIt(self):
    for name,request,expected_response in self.test_cases:
      response = self.get_response_for_request(request)
      self.assertEqual(response, expected_response, "\ntest " + name + " failed. \nResponse: \n" + str(list(response)) + "\nExpected: \n" + str(list(expected_response)))

if __name__ == '__main__':
    if len(sys.argv) > 1:
      TestServer.port = int(sys.argv.pop())                
      TestServer.dbname = sys.argv.pop()
      TestServer.pw = sys.argv.pop()
      TestServer.user = sys.argv.pop()
      TestServer.host = sys.argv.pop()
  
    unittest.main()   

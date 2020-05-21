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
      bytes([0, 1, 1, 1, 98, 97, 104, 111, 106, 115, 105, 98, 111, 102, 108, 111, 98, 117, 116, 115, 117, 106, 97, 114]),
      bytes([201, 115, 116, 117, 97, 114, 116, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
   ],
   [
      "re register bahojsiboflobutsujar",
      bytes([0, 1, 1, 1, 98, 97, 104, 111, 106, 115, 105, 98, 111, 102, 108, 111, 98, 117, 116, 115, 117, 106, 97, 114]),
      bytes([101, 115, 116, 117, 97, 114, 116, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
   ],
   [
      "check if registered nickname - missing nick",
      bytes([0, 1, 2, 1, 98, 97, 104, 111, 106, 115, 105, 98, 111, 102, 108, 111, 98, 117, 116, 115, 117, 106, 97, 114]),
      bytes([7])
   ],
   [
      "check if registered nickname stuart for app - yes  ",
      bytes([0, 1, 2, 1, 98, 97, 104, 111, 106, 115, 105, 98, 111, 102, 108, 111, 98, 117, 116, 115, 117, 106, 97, 114, 115, 116, 117, 97, 114, 116, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
      bytes([0])
   ],
   [
      "check if registered nickname bob3 for app - no",
      bytes([0, 1, 2, 2, 98, 97, 104, 111, 106, 115, 105, 98, 111, 102, 108, 111, 98, 117, 116, 115, 117, 106, 97, 114, 98, 111, 98, 51, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
      bytes([102])
   ],
   [
      "send message - missing nick",
      bytes([0, 1, 3, 1, 98, 97, 104, 111, 106, 115, 105, 98, 111, 102, 108, 111, 98, 117, 116, 115, 117, 106, 97, 114, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
      bytes([7])
   ],
   [
      "send message - missing message",
      bytes([0, 1, 3, 1, 98, 97, 104, 111, 106, 115, 105, 98, 111, 102, 108, 111, 98, 117, 116, 115, 117, 106, 97, 114, 98, 111, 98, 51, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
      bytes([8])
   ],
   [
      "send message - userid not registered with app (68)",
      bytes([0, 1, 3, 67, 98, 97, 104, 111, 106, 115, 105, 98, 111, 102, 108, 111, 98, 117, 116, 115, 117, 106, 97, 114, 98, 111, 98, 51, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 116, 104, 101, 32, 113, 117, 105, 99, 107, 32, 98, 114, 111, 119, 110, 32, 102, 111, 120, 0]),
      bytes([104])
   ],
   [
      "send message - unregistered nick bob4 in users",
      bytes([0, 1, 3, 1, 98, 97, 104, 111, 106, 115, 105, 98, 111, 102, 108, 111, 98, 117, 116, 115, 117, 106, 97, 114, 98, 111, 98, 52, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 116, 104, 101, 32, 113, 117, 105, 99, 107, 32, 98, 114, 111, 119, 110, 32, 102, 111, 120, 0]),
      bytes([102])
   ],
   [
      " send message - ok",
      bytes([0, 1, 3, 1, 98, 97, 104, 111, 106, 115, 105, 98, 111, 102, 108, 111, 98, 117, 116, 115, 117, 106, 97, 114, 115, 116, 117, 97, 114, 116, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 116, 104, 101, 32, 113, 117, 105, 99, 107, 32, 98, 114, 111, 119, 110, 32, 102, 111, 120, 0]),
      bytes([0])
   ],
   [
      "messagecount - userid not registered with app (68)",
      bytes([0, 1, 4, 67, 98, 97, 104, 111, 106, 115, 105, 98, 111, 102, 108, 111, 98, 117, 116, 115, 117, 106, 97, 114]),
      bytes([104])
    ],
    [
      "messagecount for bahojsiboflobutsujar",
      bytes([0, 1, 4, 1, 98, 97, 104, 111, 106, 115, 105, 98, 111, 102, 108, 111, 98, 117, 116, 115, 117, 106, 97, 114]),
      bytes([202, 1, 0])
    ],
    [
      "get message 1 for bahojsiboflobutsujar - missing message id (both bytes)",
      bytes([0, 1, 5, 1, 98, 97, 104, 111, 106, 115, 105, 98, 111, 102, 108, 111, 98, 117, 116, 115, 117, 106, 97, 114]),
      bytes([10])
    ],
    [
      "get message 1 for bahojsiboflobutsujar - missing message id (2nd byte)",
      bytes([0, 1, 5, 1, 98, 97, 104, 111, 106, 115, 105, 98, 111, 102, 108, 111, 98, 117, 116, 115, 117, 106, 97, 114, 1]),
      bytes([10])
    ],
    [
      "get message 1 for bahojsiboflobutsujar - invalid message number (ie greater than exist)",
      bytes([0, 1, 5, 1, 98, 97, 104, 111, 106, 115, 105, 98, 111, 102, 108, 111, 98, 117, 116, 115, 117, 106, 97, 114, 1, 1]),
      bytes([204])
    ],
    [
      "get message - userid not registered with app (68)",
      bytes([0, 1, 5, 67, 98, 97, 104, 111, 106, 115, 105, 98, 111, 102, 108, 111, 98, 117, 116, 115, 117, 106, 97, 114, 1, 0]),
      bytes([104])
    ],
    [
      "get message 1 for bahojsiboflobutsujar - ok",
      bytes([0, 1, 5, 1, 98, 97, 104, 111, 106, 115, 105, 98, 111, 102, 108, 111, 98, 117, 116, 115, 117, 106, 97, 114, 1, 0]),
      bytes([203, 115, 116, 117, 97, 114, 116, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 19, 116, 104, 101, 32, 113, 117, 105, 99, 107, 32, 98, 114, 111, 119, 110, 32, 102, 111, 120])
    ],
    [
      "join pool for unreg user for app ",
      bytes([0, 1, 6, 69, 98, 97, 104, 111, 106, 115, 105, 98, 111, 102, 108, 111, 98, 117, 116, 115, 117, 106, 97, 114, 3]),
      bytes([104])
    ],
    [
      "1/3 join pool for reg user for app (205 + pool id)",
      bytes([0, 1, 6, 1, 98, 97, 104, 111, 106, 115, 105, 98, 111, 102, 108, 111, 98, 117, 116, 115, 117, 106, 97, 114, 3]),
      bytes([205, 1, 0])
    ],
    [
      "join pool where we're already in an unfilled pool (206 + pool id)",
      bytes([0, 1, 6, 1, 98, 97, 104, 111, 106, 115, 105, 98, 111, 102, 108, 111, 98, 117, 116, 115, 117, 106, 97, 114, 3]),
      bytes([207, 1, 0])
    ],
    [
      "get pool for unreg user for app",
      bytes([0, 1, 7, 69, 98, 97, 104, 111, 106, 115, 105, 98, 111, 102, 108, 111, 98, 117, 116, 115, 117, 106, 97, 114, 5, 0]),
      bytes([104])
    ],
    [
      "get pool missing byte 2 of poolId",
      bytes([0, 1, 7, 1, 98, 97, 104, 111, 106, 115, 105, 98, 111, 102, 108, 111, 98, 117, 116, 115, 117, 106, 97, 114, 5]),
      bytes([12])
    ],
    [
      "get pool for invalid poolId",
      bytes([0, 1, 7, 1, 98, 97, 104, 111, 106, 115, 105, 98, 111, 102, 108, 111, 98, 117, 116, 115, 117, 106, 97, 114, 255, 0]),
      bytes([105])
    ],
    [
      "get pool ok - unfilled",
      bytes([0, 1, 7, 1, 98, 97, 104, 111, 106, 115, 105, 98, 111, 102, 108, 111, 98, 117, 116, 115, 117, 106, 97, 114, 1, 0]),
      bytes([208])
    ],
    [
      "2/3 register cahojsiboflobutsujar",
      bytes([0, 1, 1, 1, 99, 97, 104, 111, 106, 115, 105, 98, 111, 102, 108, 111, 98, 117, 116, 115, 117, 106, 97, 114]),
      bytes([201, 115, 116, 117, 97, 114, 116, 50, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    ],
    [
      "2/3 register dahojsiboflobutsujar",
      bytes([0, 1, 1, 1, 100, 97, 104, 111, 106, 115, 105, 98, 111, 102, 108, 111, 98, 117, 116, 115, 117, 106, 97, 114]),
      bytes([201, 115, 116, 117, 97, 114, 116, 51, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
   ],
    [
      "2/3 join pool for reg user for app (205 + pool id)",
      bytes([0, 1, 6, 1, 99, 97, 104, 111, 106, 115, 105, 98, 111, 102, 108, 111, 98, 117, 116, 115, 117, 106, 97, 114, 3]),
      bytes([205, 1, 0])
    ],
    [
      "3/3 join pool for reg user for app (205 + pool id)",
      bytes([0, 1, 6, 1, 100, 97, 104, 111, 106, 115, 105, 98, 111, 102, 108, 111, 98, 117, 116, 115, 117, 106, 97, 114, 3]),
      bytes([205, 1, 0])
    ],
    [
      "get pool ok - filled",
      bytes([0, 1, 7, 1, 98, 97, 104, 111, 106, 115, 105, 98, 111, 102, 108, 111, 98, 117, 116, 115, 117, 106, 97, 114, 1, 0]),
      bytes([209, 3, 6, 115, 116, 117, 97, 114, 116, 7, 115, 116, 117, 97, 114, 116, 50, 7, 115, 116, 117, 97, 114, 116, 51])
    ]
  ]

  def run_sql(self, filename):
    with open(filename, 'r') as myfile:
      sql = myfile.read()
      myfile.close
    print(sql)
    cursor = self.db.cursor()

    sqlCommands = sql.split(';')

    for command in sqlCommands:
        try:
            if command.strip() != '':
                cursor.execute(command)
        except IOError as msg:
            print ("Command skipped: " + msg)
    self.db.commit()
    self.db.close()


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
      self.assertEqual(response, expected_response, "\ntest " + name + " failed. \nRequest: \n" + str(list(request)) + "\nResponse: \n" + str(list(response)) + "\nExpected: \n" + str(list(expected_response)))

if __name__ == '__main__':
    if len(sys.argv) > 1:
      TestServer.port = int(sys.argv.pop())                
      TestServer.dbname = sys.argv.pop()
      TestServer.pw = sys.argv.pop()
      TestServer.user = sys.argv.pop()
      TestServer.host = sys.argv.pop()
  
    unittest.main()   

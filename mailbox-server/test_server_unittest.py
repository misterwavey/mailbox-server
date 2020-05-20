import unittest
import socket

class TestServer(unittest.TestCase):
	INVALID_REQUEST = bytes([0,2])
	EXPECTED = bytes([4])

	def setUp(self):
		self.client = socket.socket()
		self.client.settimeout(1)
		self.client.connect(('127.0.0.1', 8080))

	def testInvalidLength(self):
		self.client.send(self.INVALID_REQUEST)
		response = self.client.recv(1024)
		self.client.close()
		self.assertEqual(response, self.EXPECTED, "not expected")

if __name__ == '__main__':
    unittest.main()		
